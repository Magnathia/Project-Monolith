# Rocky 9 Full GUI (Minimal Bloat)

This VM provides a Rocky Linux 9 desktop environment with minimal bloat.

## Usage

1. **Start the VM:**
   ```sh
   vagrant up
   ```

2. **Access the GUI:**
   - Use VirtualBox or Hyper-V console to view the desktop.
   - Default login: `vagrant` / `vagrant`

3. **SSH into the VM (for CLI):**
   ```sh
   vagrant ssh
   ```

4. **Stop the VM:**
   ```sh
   vagrant halt
   ```

5. **Destroy the VM:**
   ```sh
   vagrant destroy
   ```

## Features

- Rocky Linux 9 with GNOME desktop (`@server-with-gui`)
- Bloatware groups removed (multimedia, office, admin tools, guest agents)
- Latest Python 3 and pip
- Graphical target set as default

> **Note:** The minimum recommended disk size for this VM is **150GB**.  
> This ensures there is enough space for all GUI packages and future updates.

## Customization

Edit `playbook.yml` to add or remove desktop applications or system settings.
