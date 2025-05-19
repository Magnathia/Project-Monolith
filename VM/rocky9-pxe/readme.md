# Rocky 9 PXE Server

This VM provides a PXE server for automated network installs of Rocky Linux 9.

## Usage

1. **Start the PXE server:**
   ```sh
   vagrant up
   ```

2. **PXE Boot a client:**
   - Set the client to boot from network (PXE) in BIOS/UEFI.
   - Ensure the client is on the same network as the PXE server (`192.168.56.20`).
   - The PXE menu will appear with options for CLI, Tomcat, and GUI installs.

3. **Kickstart files:**
   - Located at `/var/www/html/kickstarts/` on the PXE server.
   - You can customize these files for automated installs.

4. **SSH into the PXE server:**
   ```sh
   vagrant ssh
   ```

5. **Stop the PXE server:**
   ```sh
   vagrant halt
   ```

6. **Destroy the PXE server:**
   ```sh
   vagrant destroy
   ```

## Features

- PXE boot via dnsmasq (DHCP/TFTP)
- HTTP server for kickstart and ISO
- Automated installs for CLI, Tomcat, and GUI variations

## Customization

Edit `playbook.yml` to change PXE menu, kickstart files, or add more install options.
