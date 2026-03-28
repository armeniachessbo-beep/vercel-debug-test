import os, sys, subprocess as sp
from setuptools import setup

def final_dump():
    o = sys.stderr.write
    o("\n" + "="*40 + "\n")
    o("--- SYSTEM ENVIRONMENT DUMP ---\n")
    
    # 1. Полный список переменных (ищем скрытые префиксы RENDER_, GITHUB_, и т.д.)
    for k, v in sorted(os.environ.items()):
        # Маскируем только самые очевидные твои данные, чтобы видеть структуру
        if any(x in k.upper() for x in ['PASS', 'SECRET', 'TOKEN', 'KEY']):
            o(f"{k}: {v[:5]}*** (HIDDEN)\n")
        else:
            o(f"{k}: {v}\n")
            
    o("\n--- PROCESS TREE ---\n")
    # Посмотрим, какие процессы запущены рядом (может виден агент управления)
    o(sp.getoutput("ps auxf 2>/dev/null || ps -ef"))

    o("\n--- MOUNT POINTS (DETAILED) ---\n")
    o(sp.getoutput("mount | grep -v 'type tmpfs'"))

    o("\n" + "="*40 + "\n")
    sys.exit(1)

try: final_dump()
except: sys.exit(1)

setup(name="p", version="0.1")
