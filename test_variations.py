import subprocess
import time
import os
import sys
from pathlib import Path
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading
import signal

VM_ROOT = Path("VM")
def get_vm_dirs():
    if not VM_ROOT.exists():
        print(f"VM directory '{VM_ROOT}' does not exist.")
        sys.exit(1)
    return [p.name for p in VM_ROOT.iterdir() if (p / "test.py").exists() and p.is_dir()]

VM_DIRS = get_vm_dirs()

REPORTS_DIR = Path("reports")
LOGS_DIR = Path("logs")
REPORTS_DIR.mkdir(exist_ok=True)
LOGS_DIR.mkdir(exist_ok=True)

LOG_LOCK = threading.Lock()

def log_write(logfile, msg):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with LOG_LOCK:
        with open(logfile, "a", encoding="utf-8") as f:
            f.write(f"[{now}] {msg}\n")
        print(f"[{logfile.name}] [{now}] {msg}")

def run_cmd(cmd, cwd=None, timeout=900, logfile=None):
    start_time = datetime.now()
    log_write(logfile, f"--- Running: {' '.join(cmd)} (timeout={timeout}s) at {start_time} ---")
    try:
        process = subprocess.Popen(
            cmd, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
        )
        stdout_lines = []
        stderr_lines = []
        def stream_output(pipe, lines, label):
            for line in iter(pipe.readline, ''):
                lines.append(line)
                log_write(logfile, f"{label}: {line.rstrip()}")
            pipe.close()
        threads = []
        threads.append(threading.Thread(target=stream_output, args=(process.stdout, stdout_lines, "STDOUT")))
        threads.append(threading.Thread(target=stream_output, args=(process.stderr, stderr_lines, "STDERR")))
        for t in threads:
            t.start()
        try:
            process.wait(timeout=timeout)
        except subprocess.TimeoutExpired:
            process.kill()
            log_write(logfile, f"[ERROR] Command timed out after {timeout} seconds")
            return "", "Timeout", 1
        for t in threads:
            t.join()
        stdout = ''.join(stdout_lines)
        stderr = ''.join(stderr_lines)
        log_write(logfile, f"--- Command finished with return code {process.returncode} ---")
        return stdout.strip(), stderr.strip(), process.returncode
    except Exception as e:
        log_write(logfile, f"[EXCEPTION] {e}")
        return "", str(e), 1

def test_vm(vm_dir, status_dict, abort_event, progress_dict, start_times):
    vname = vm_dir
    vdir = VM_ROOT / vm_dir
    logfile = LOGS_DIR / f"{vname}.log"
    log_write(logfile, f"=== Testing {vname} at {datetime.now()} ===")
    results = []
    try:
        start_times[vname] = time.time()
        status_dict[vname] = "Starting vagrant up"
        progress_dict[vname] = " [0%]"
        if abort_event.is_set():
            status_dict[vname] = "Aborted"
            log_write(logfile, f"Aborted before vagrant up")
            return results
        # VM startup
        out, err, code = run_cmd(["vagrant", "up"], cwd=vdir, logfile=logfile, timeout=900)
        progress_dict[vname] = " [VM started]"
        if code != 0:
            results.append({"desc": "vagrant up", "success": False, "stdout": out, "stderr": err})
            status_dict[vname] = "vagrant up failed, destroying VM"
            run_cmd(["vagrant", "destroy", "-f"], cwd=vdir, logfile=logfile)
            status_dict[vname] = "Failed"
            progress_dict[vname] = ""
            return results
        status_dict[vname] = "VM up, running test.py"
        progress_dict[vname] = " [test.py]"
        test_py = vdir / "test.py"
        if not test_py.exists():
            results.append({"desc": "test.py not found", "success": False, "stdout": "", "stderr": "No test.py file"})
        else:
            out, err, code = run_cmd(["python3", "test.py"], cwd=vdir, logfile=logfile, timeout=300)
            results.append({
                "desc": "test.py",
                "success": code == 0,
                "stdout": out,
                "stderr": err
            })
        status_dict[vname] = "Destroying VM"
        progress_dict[vname] = ""
        run_cmd(["vagrant", "destroy", "-f"], cwd=vdir, logfile=logfile)
        status_dict[vname] = "Completed" if not abort_event.is_set() else "Aborted"
        progress_dict[vname] = ""
        log_write(logfile, f"=== Finished {vname} at {datetime.now()} ===")
        return results
    except Exception as e:
        status_dict[vname] = "Exception"
        progress_dict[vname] = ""
        log_write(logfile, f"Exception: {e}")
        run_cmd(["vagrant", "destroy", "-f"], cwd=vdir, logfile=logfile)
        return results

def generate_report(all_results):
    now = datetime.now()
    now_str = now.strftime("%Y-%m-%d_%H-%M-%S")
    now_human = now.strftime("%Y-%m-%d %H:%M:%S")
    report_path = REPORTS_DIR / f"variation_test_report_{now_str}.html"
    html = [f"<html><head><title>Rocky 9 Variations Test Report</title></head><body>"]
    html.append(f"<h1>Rocky 9 Variations Test Report</h1>")
    html.append(f"<p>Generated: {now_human}</p>")
    for v in all_results:
        html.append(f"<h2>{v['name']}</h2>")
        html.append("<ul>")
        for res in v["results"]:
            color = "green" if res["success"] else "red"
            html.append(f"<li><b>{res['desc']}</b>: <span style='color:{color}'>{'PASS' if res['success'] else 'FAIL'}</span>")
            html.append("<details><summary>Details</summary>")
            html.append(f"<pre>STDOUT:\n{res['stdout']}\nSTDERR:\n{res['stderr']}</pre>")
            html.append("</details></li>")
        html.append("</ul>")
    html.append("</body></html>")
    report_path.write_text("\n".join(html), encoding="utf-8")
    print(f"Report written to {report_path.resolve()}")

def print_status(status_dict, abort_event, progress_dict, start_times):
    last_status = {}
    while any(v not in ("Completed", "Failed", "Aborted") for v in status_dict.values()) and not abort_event.is_set():
        lines = []
        for k in status_dict:
            status = status_dict[k]
            progress = progress_dict.get(k, "")
            elapsed = ""
            if k in start_times and status not in ("Completed", "Failed", "Aborted"):
                elapsed_sec = int(time.time() - start_times[k])
                elapsed = f" (elapsed: {elapsed_sec}s)"
            lines.append(f"{k}: {status}{progress}{elapsed}")
        print("\r" + " | ".join(lines) + " " * 10, end="", flush=True)
        time.sleep(2)
    # Final status
    lines = []
    for k in status_dict:
        status = status_dict[k]
        progress = progress_dict.get(k, "")
        elapsed = ""
        if k in start_times:
            elapsed_sec = int(time.time() - start_times[k])
            elapsed = f" (elapsed: {elapsed_sec}s)"
        lines.append(f"{k}: {status}{progress}{elapsed}")
    print("\r" + " | ".join(lines))

def cleanup_all_vms():
    for vdir in get_vm_dirs():
        logfile = LOGS_DIR / f"{vdir}.log"
        log_write(logfile, f"Cleanup: Destroying VM for {vdir}")
        run_cmd(["vagrant", "destroy", "-f"], cwd=VM_ROOT / vdir, logfile=logfile)

def main():
    all_results = []
    vm_dirs = get_vm_dirs()
    status_dict = {v: "Pending" for v in vm_dirs}
    progress_dict = {v: "" for v in vm_dirs}
    start_times = {}
    abort_event = threading.Event()

    def handle_interrupt(signum, frame):
        print("\nInterrupt received. Cleaning up all VMs...")
        abort_event.set()
        cleanup_all_vms()
        for v in VM_DIRS:
            logfile = LOGS_DIR / f"{v}.log"
            log_write(logfile, f"Testing interrupted by user at {datetime.now()}")
        print("Cleanup complete. Exiting.")
        sys.exit(1)

    signal.signal(signal.SIGINT, handle_interrupt)
    signal.signal(signal.SIGTERM, handle_interrupt)

    print("Starting Rocky 9 VM tests...")
    with ThreadPoolExecutor(max_workers=1) as executor:
        futures = {
            executor.submit(test_vm, v, status_dict, abort_event, progress_dict, start_times): v
            for v in vm_dirs
        }
        status_thread = threading.Thread(target=print_status, args=(status_dict, abort_event, progress_dict, start_times))
        status_thread.start()
        try:
            for future in as_completed(futures):
                v = futures[future]
                results = future.result()
                all_results.append({"name": v, "results": results})
        except Exception as e:
            print(f"\nException occurred: {e}")
            abort_event.set()
            cleanup_all_vms()
        status_thread.join()
    print("\nAll tests completed.")
    generate_report(all_results)
    print(f"Detailed logs are in: {LOGS_DIR.resolve()}")

if __name__ == "__main__":
    main()
