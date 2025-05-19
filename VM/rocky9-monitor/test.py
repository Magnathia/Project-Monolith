import subprocess
import sys

def check_docker():
    try:
        out = subprocess.check_output(
            ["systemctl", "is-active", "docker"], text=True
        ).strip()
        print("Docker status:", out)
        return out == "active"
    except Exception as e:
        print(e)
        return False

def check_zabbix_container():
    try:
        out = subprocess.check_output(
            ["docker", "ps", "--filter", "name=zabbix", "--format", "{{.Status}}"], text=True
        ).strip()
        print("Zabbix container status:", out)
        return bool(out)
    except Exception as e:
        print(e)
        return False

if __name__ == "__main__":
    ok = check_docker() and check_zabbix_container()
    sys.exit(0 if ok else 1)
