# Rocky 9 with Apache Tomcat

This VM provides a minimal Rocky Linux 9 environment with Apache Tomcat installed.

## Usage

1. **Start the VM:**
   ```sh
   vagrant up
   ```

2. **SSH into the VM:**
   ```sh
   vagrant ssh
   ```

3. **Access Tomcat:**
   - Open your browser to [http://192.168.56.12:8080](http://192.168.56.12:8080) (default Tomcat port).
   - If you need to access Tomcat from the host, ensure port forwarding or use the private network IP.

4. **Stop the VM:**
   ```sh
   vagrant halt
   ```

5. **Destroy the VM:**
   ```sh
   vagrant destroy
   ```

## Features

- Minimal Rocky Linux 9 install
- Apache Tomcat (systemd-managed)
- Java 11 OpenJDK
- Latest Python 3 and pip

## Customization

Edit `playbook.yml` to add webapps, change Tomcat configuration, or install additional packages.
