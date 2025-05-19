import subprocess
import sys

def check_graphical_target():
    try:
        out = subprocess.check_output(
            ["systemctl", "get-default"], text=True
        ).strip()
        print(out)
        return out == "graphical.target"
    except Exception as e:
        print(e)
        return False

if __name__ == "__main__":
    if check_graphical_target():
        print("Graphical target is set.")
        sys.exit(0)
    else:
        print("Graphical target is NOT set.")
        sys.exit(1)
