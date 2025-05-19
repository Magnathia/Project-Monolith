import os
from pathlib import Path
import urllib.request
import hashlib

CACHE_DIR = Path("cache")
CACHE_DIR.mkdir(exist_ok=True)

# Rocky Linux 9.5 minimal ISO for PXE (latest)
ISO_URL = "https://download.rockylinux.org/pub/rocky/9.5/isos/x86_64/Rocky-9-latest-x86_64-minimal.iso"
ISO_FILENAME = "Rocky-9.5-x86_64-minimal.iso"
ISO_PATH = CACHE_DIR / ISO_FILENAME

# EPEL release RPM for Rocky 9
EPEL_URL = "https://dl.fedoraproject.org/pub/epel/epel-release-latest-9.noarch.rpm"
EPEL_FILENAME = "epel-release-latest-9.noarch.rpm"
EPEL_PATH = CACHE_DIR / EPEL_FILENAME

# Docker CE repo RPM (for Rocky/CentOS 9)
DOCKER_CE_REPO_URL = "https://download.docker.com/linux/centos/docker-ce.repo"
DOCKER_CE_REPO_FILENAME = "docker-ce.repo"
DOCKER_CE_REPO_PATH = CACHE_DIR / DOCKER_CE_REPO_FILENAME

# Common container images (as tarballs, for advanced caching, not pulled by default)
# Example: Prometheus, Grafana, ntopng, Zabbix, AWX, GitLab CE
# These are not downloaded by default in playbooks, but you can pre-pull and save them with:
#   docker pull <image>; docker save -o <cache>/<name>.tar <image>
CONTAINER_IMAGES = [
    # {"name": "prometheus.tar", "image": "prom/prometheus:latest"},
    # {"name": "grafana.tar", "image": "grafana/grafana:latest"},
    # {"name": "ntopng.tar", "image": "ntop/ntopng:stable"},
    # {"name": "zabbix-appliance.tar", "image": "zabbix/zabbix-appliance:alpine-6.4-latest"},
    # {"name": "awx.tar", "image": "ansible/awx:21.14.0"},
    # {"name": "gitlab-ce.tar", "image": "gitlab/gitlab-ce:latest"},
]

TO_CACHE = [
    {"url": ISO_URL, "path": ISO_PATH},
    {"url": EPEL_URL, "path": EPEL_PATH},
    {"url": DOCKER_CE_REPO_URL, "path": DOCKER_CE_REPO_PATH},
    # Add more files here as needed, e.g. RPMs, tarballs, etc.
]

def get_remote_file_size(url):
    try:
        with urllib.request.urlopen(url) as response:
            return int(response.headers.get("Content-Length", 0))
    except Exception:
        return 0

def verify_file_size(dest, expected_size):
    if not dest.exists():
        return False
    actual_size = dest.stat().st_size
    if expected_size and actual_size != expected_size:
        print(f"[ERROR] {dest.name} size mismatch after download (expected: {expected_size}, got: {actual_size})")
        return False
    return True

def file_needs_update(url, dest):
    # If file does not exist, needs update
    if not dest.exists():
        return True
    # If remote file size differs, update
    remote_size = get_remote_file_size(url)
    local_size = dest.stat().st_size
    if remote_size and remote_size != local_size:
        print(f"[INFO] {dest.name} size mismatch (local: {local_size}, remote: {remote_size}), updating.")
        return True
    return False

def download_file(url, dest):
    remote_size = get_remote_file_size(url)
    if not file_needs_update(url, dest):
        print(f"[SKIP] {dest.name} is up to date in cache.")
        return
    print(f"[DOWNLOADING] {dest.name} ...")
    try:
        with urllib.request.urlopen(url) as response, open(dest, "wb") as out_file:
            out_file.write(response.read())
        if verify_file_size(dest, remote_size):
            print(f"[DONE] {dest.name}")
        else:
            print(f"[FAILED] {dest.name} download incomplete or corrupted.")
            if dest.exists():
                dest.unlink()
    except Exception as e:
        print(f"[ERROR] Failed to download {url}: {e}")

def main():
    print(f"Populating cache in: {CACHE_DIR.resolve()}")
    for item in TO_CACHE:
        download_file(item["url"], item["path"])
    # Container images: print instructions for manual caching
    if CONTAINER_IMAGES:
        print("\nTo cache container images, use:")
        for img in CONTAINER_IMAGES:
            print(f"  docker pull {img['image']}; docker save -o {CACHE_DIR / img['name']} {img['image']}")
    print("Cache population complete.")

if __name__ == "__main__":
    main()
