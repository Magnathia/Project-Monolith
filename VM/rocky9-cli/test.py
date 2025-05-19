import subprocess
import sys

def check_python():
    try:
        out = subprocess.check_output(["python3", "--version"], text=True).strip()
        print(out)
        return out.startswith("Python 3")
    except Exception as e:
        print(e)
        return False

if __name__ == "__main__":
    if check_python():
        print("Python 3 is present.")
        sys.exit(0)
    else:
        print("Python 3 is missing.")
        sys.exit(1)
