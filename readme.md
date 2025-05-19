# Rocky 9 VM Automation Project

## Overview

This project automates the deployment and configuration of several Rocky Linux 9 virtual machines for various roles (CLI, GUI, Tomcat, PXE, Monitoring/Management). It's intent is to lower the barrier of entry for industry standard best practices and encourage a more controlled, safer environment for people to operate. This is intended for Home Labs, Businesses, Science, Schools, anywhere that services are offered. Development and support on this project from its author should be considered "Whimsical" at best as this is a passion project born of ADHD and Autism.

## Prerequisites

- [Vagrant](https://www.vagrantup.com/) (with `vagrant-disksize` plugin)
- [VirtualBox](https://www.virtualbox.org/)
- [Ansible](https://www.ansible.com/) (used via `ansible_local` provisioner)
- Internet access for package and container downloads

## VM Variations

- **rocky9-cli**: Minimal CLI-only Rocky Linux 9
- **rocky9-gui**: Full GUI (with dynamic disk/partition resize)
- **rocky9-tomcat**: CLI + Apache Tomcat
- **rocky9-pxe**: PXE boot server (requires `syslinux-tftpboot` and EPEL)
- **rocky9-monitor**: Monitoring stack (Dockerized Prometheus, Grafana, ntopng, Zabbix, AWX, GitLab)

## Directory Structure

- `VM/` — All VM variations (each with its own Vagrantfile, playbook, test.py, etc.)
- `logs/` — All logs from test runs
- `reports/` — All HTML reports from test runs

## Usage

1. Clone this repository.
2. Run the test script to deploy and test all variations:
   ```
   python test_variations.py
   ```
3. Individual VMs can be managed in their respective directories under `VM/` using Vagrant:
   ```
   cd VM/rocky9-gui
   vagrant up
   vagrant destroy -f
   ```

## PXE VM Notes

- The PXE VM requires the `syslinux-tftpboot` package, which is available from EPEL.
- The playbook dynamically searches for `pxelinux.0` in:
  - `/usr/share/syslinux/pxelinux.0`
  - `/usr/share/syslinux-tftpboot/pxelinux.0`
  - `/var/lib/tftpboot/pxelinux.0`
- If the file is not found, ensure EPEL is enabled and the package is installed:
  ```
  sudo dnf install epel-release
  sudo dnf install syslinux-tftpboot
  ```
- No template is needed for `pxelinux.0`; it is a binary provided by the package.

## Monitoring VM Notes

- The Zabbix container now uses the valid image:
  ```
  zabbix/zabbix-appliance:alpine-4.0-latest
  ```
- If you need a different version, check available tags on Docker Hub.

## Reports

- After each deployment, an HTML report is generated for each VM in the `reports` directory.
- Reports include all Ansible facts and configuration details for the VM.

## Troubleshooting

- If you encounter disk space issues, ensure the VM disk size is set appropriately in the `Vagrantfile` and that the playbook's dynamic resize step is present.
- For PXE issues, verify that `pxelinux.0` exists after package install.
- For Zabbix container issues, ensure the image tag exists on Docker Hub and the VM has internet access.

## Monolith CLI

A command-line tool `monolith.py` is provided for running VM tests.

### Usage

- All VM directories are now under the `VM/` folder.
- Run all VM tests:
  ```
  python monolith.py test all
  ```

- Run a single VM test (e.g., for the GUI variation):
  ```
  python monolith.py test rocky9-gui
  ```

- To see available variations, check the `VM/` directory.

### Example

```
python monolith.py test all
python monolith.py test rocky9-pxe
```

## Logs and Reports

- All logs are written to the `logs/` directory.
- All HTML reports are written to the `reports/` directory.

## License

MIT License
