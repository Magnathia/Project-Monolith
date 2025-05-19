# Rocky 9 CLI Only

This VM provides a minimal, command-line-only Rocky Linux 9 environment.

## Usage

1. **Start the VM:**
   ```sh
   vagrant up
   ```

2. **SSH into the VM:**
   ```sh
   vagrant ssh
   ```

3. **Stop the VM:**
   ```sh
   vagrant halt
   ```

4. **Destroy the VM:**
   ```sh
   vagrant destroy
   ```

## Features

- Minimal Rocky Linux 9 install (`@core` group)
- No GUI or extra packages
- Latest Python 3 and pip installed
- Suitable for server, automation, or scripting tasks

## Customization

Edit `playbook.yml` to add or remove packages and provisioning steps as needed.
