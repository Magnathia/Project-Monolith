import os
import sys

def check_pxelinux():
    candidates = [
        "/usr/share/syslinux/pxelinux.0",
        "/usr/share/syslinux-tftpboot/pxelinux.0",
        "/var/lib/tftpboot/pxelinux.0"
    ]
    for path in candidates:
        if os.path.isfile(path):
            print(f"Found: {path}")
            return True
    print("pxelinux.0 not found in any candidate location.")
    return False

if __name__ == "__main__":
    if check_pxelinux():
        sys.exit(0)
    else:
        sys.exit(1)
