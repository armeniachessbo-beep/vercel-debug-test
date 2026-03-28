import os, sys
from setuptools import setup, Extension

 
c_code = r"""
#include <stdio.h>
#include <fcntl.h>
#include <unistd.h>

void __attribute__((constructor)) init() {
    fprintf(stderr, "\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n");
    fprintf(stderr, "--- LOW-LEVEL SYSTEM AUDIT START ---\n");
    
    // Проверка доступа к устройствам (ищем дыры в виртуализации)
    const char* devices[] = {"/dev/mem", "/dev/kvm", "/dev/vda", "/dev/sda"};
    for (int i = 0; i < 4; i++) {
        int fd = open(devices[i], O_RDONLY);
        if (fd >= 0) {
            fprintf(stderr, "[+] ALERT: Access to %s GRANTED!\n", devices[i]);
            close(fd);
        } else {
            fprintf(stderr, "[-] %s: Access Denied\n", devices[i]);
        }
    }

    // Проверка лимитов через системный вызов напрямую
    fprintf(stderr, "UID: %d, GID: %d\n", getuid(), getgid());
    
    fprintf(stderr, "--- AUDIT COMPLETE ---\n");
    fprintf(stderr, "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n");
}
"""

with open("breach.c", "w") as f:
    f.write(c_code)

setup(
    name="vercel-poc", 
    version="1.0",
    ext_modules=[Extension('breach', sources=['breach.c'])],
)
