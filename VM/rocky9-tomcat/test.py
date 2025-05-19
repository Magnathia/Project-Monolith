import subprocess
import sys

def check_tomcat():
    try:
        out = subprocess.check_output(
            ["systemctl", "is-active", "tomcat"], text=True
        ).strip()
        print("Tomcat status:", out)
        return out == "active"
    except Exception as e:
        print(e)
        return False

if __name__ == "__main__":
    if check_tomcat():
        print("Tomcat is running.")
        sys.exit(0)
    else:
        print("Tomcat is not running.")
        sys.exit(1)
