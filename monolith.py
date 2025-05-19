import argparse
import subprocess
import sys
from pathlib import Path

VM_ROOT = Path("VM")
def get_vm_dirs():
    if not VM_ROOT.exists():
        print(f"VM directory '{VM_ROOT}' does not exist.")
        sys.exit(1)
    return [p.name for p in VM_ROOT.iterdir() if (p / "test.py").exists() and p.is_dir()]

def run_test(variation):
    vm_dir = VM_ROOT / variation
    test_py = vm_dir / "test.py"
    if not test_py.exists():
        print(f"No test.py found in {vm_dir}")
        sys.exit(1)
    print(f"Running test for {variation}...")
    result = subprocess.run(["python3", "test.py"], cwd=test_py.parent)
    sys.exit(result.returncode)

def run_all():
    failed = []
    vm_dirs = get_vm_dirs()
    for variation in vm_dirs:
        test_py = VM_ROOT / variation / "test.py"
        if not test_py.exists():
            print(f"[{variation}] No test.py found.")
            failed.append(variation)
            continue
        print(f"[{variation}] Running test...")
        result = subprocess.run(["python3", "test.py"], cwd=test_py.parent)
        if result.returncode != 0:
            print(f"[{variation}] FAIL")
            failed.append(variation)
        else:
            print(f"[{variation}] PASS")
    if failed:
        print("Some tests failed:", ", ".join(failed))
        sys.exit(1)
    else:
        print("All tests passed.")
        sys.exit(0)

def main():
    parser = argparse.ArgumentParser(
        description="Monolith CLI for Rocky 9 VM automation and testing."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    test_parser = subparsers.add_parser("test", help="Run VM tests")
    test_parser.add_argument("variation", help="VM variation name or 'all'")

    args = parser.parse_args()

    if args.command == "test":
        if args.variation == "all":
            run_all()
        else:
            vm_dirs = get_vm_dirs()
            if args.variation not in vm_dirs:
                print(f"Unknown variation: {args.variation}")
                print("Available variations:", ", ".join(vm_dirs))
                sys.exit(1)
            run_test(args.variation)

if __name__ == "__main__":
    main()
