# Rocky 9 Monitoring & Management Stack

This VM provides a full monitoring and management stack, all containerized via Docker:

- **Prometheus** (metrics collection)
- **Grafana** (metrics dashboards)
- **ntopng** (network traffic analysis)
- **Zabbix** (security scanning & monitoring)
- **Ansible AWX** (web-based Ansible management)
- **GitLab CE** (self-hosted Git repositories & CI/CD)

## Usage

1. **Start the VM:**
   ```sh
   vagrant up
   ```

2. **SSH into the VM:**
   ```sh
   vagrant ssh
   ```

3. **Access the web interfaces from your host browser:**

   - **Prometheus:** [http://192.168.56.30:9090](http://192.168.56.30:9090)
   - **Grafana:** [http://192.168.56.30:3000](http://192.168.56.30:3000)
     - Default login: `admin` / `admin`
   - **ntopng:** [http://192.168.56.30:3001](http://192.168.56.30:3001)
     - Default login: `admin` / `admin`
   - **Zabbix:** [http://192.168.56.30:8080](http://192.168.56.30:8080)
     - Default login: `Admin` / `zabbix`
   - **Ansible AWX:** [http://192.168.56.30:8081](http://192.168.56.30:8081)
     - Default login: `admin` / `password`
   - **GitLab CE:** [http://192.168.56.30:8929](http://192.168.56.30:8929)
     - Default login: `root` / `gitlabroot` (set on first login)

4. **Stop the VM:**
   ```sh
   vagrant halt
   ```

5. **Destroy the VM:**
   ```sh
   vagrant destroy
   ```

## Default Credentials & Security Keys

| Service      | Username | Password      | Notes                        |
|--------------|----------|--------------|------------------------------|
| Grafana      | admin    | admin        | Change after first login     |
| ntopng       | admin    | admin        |                              |
| Zabbix       | Admin    | zabbix       |                              |
| AWX          | admin    | password     |                              |
| GitLab CE    | root     | gitlabroot   | Set on first login           |
| AWX Secret   | -        | awxsecret    | Used for Django SECRET_KEY   |
| AWX DB User  | awx      | awxpass      | Internal DB for AWX          |
| Zabbix DB    | zabbix   | zabbix/zabbixroot | Internal DB for Zabbix  |

**Warning:** These are default, insecure credentials for initial setup and demo purposes.  
**You must change all passwords and secrets before deploying in production.**

## Hardening Recommendations

- **Change all default passwords** immediately after first login for each service.
- **Restrict network access** to management interfaces using firewall rules or VPN.
- **Enable HTTPS** for all web interfaces (reverse proxy or container config).
- **Configure 2FA** where supported (e.g., GitLab, Grafana).
- **Rotate and securely store all secrets and keys**.
- **Limit Docker exposure**: Only expose necessary ports, and consider using Docker networks for internal communication.
- **Regularly update containers** to patch vulnerabilities.
- **Review and restrict user permissions** in each tool.
- **Monitor logs** for unauthorized access attempts.

## Playbook Structure

Each major component is provisioned by its own playbook:

- `playbook.docker.yml` – Installs Docker and prerequisites
- `playbook.prometheus.yml` – Deploys Prometheus
- `playbook.grafana.yml` – Deploys Grafana
- `playbook.ntopng.yml` – Deploys ntopng
- `playbook.zabbix.yml` – Deploys Zabbix
- `playbook.awx.yml` – Deploys Ansible AWX
- `playbook.gitlab.yml` – Deploys GitLab CE

You can customize or run these playbooks individually as needed.

## Tool Usage Details

### Prometheus & Grafana

#### Prometheus

- **Purpose:** Collects and stores metrics from configured targets.
- **Access:** [http://192.168.56.30:9090](http://192.168.56.30:9090)
- **Configuration:** Edit `/etc/prometheus/prometheus.yml` inside the container (use `docker exec`).
- **Add targets:** Add scrape configs for your hosts/services.

#### Grafana

- **Purpose:** Visualizes metrics from Prometheus and other sources.
- **Access:** [http://192.168.56.30:3000](http://192.168.56.30:3000)
- **Login:** `admin` / `admin` (change password on first login)

#### Workflow Tutorial

1. **Add Prometheus as a data source in Grafana:**
   - Log in to Grafana.
   - Go to **Configuration > Data Sources > Add data source**.
   - Select **Prometheus**.
   - Set URL to `http://192.168.56.30:9090` and click **Save & Test**.

2. **Import a dashboard:**
   - Go to **Create > Import**.
   - Enter a dashboard ID from [Grafana.com](https://grafana.com/grafana/dashboards/) (e.g., 1860 for Node Exporter).
   - Select your Prometheus data source and click **Import**.

3. **Add metrics targets to Prometheus:**
   - SSH into the VM: `vagrant ssh`
   - Find the Prometheus container: `docker ps`
   - Edit the config:
     ```sh
     docker exec -it prometheus vi /etc/prometheus/prometheus.yml
     ```
   - Add your targets under `scrape_configs`.
   - Reload Prometheus config (or restart the container).

4. **View metrics and dashboards:**
   - Use Prometheus UI to query metrics.
   - Use Grafana dashboards for visualization.

---

### Zabbix

- **Purpose:** Monitoring, alerting, and security scanning.
- **Access:** [http://192.168.56.30:8080](http://192.168.56.30:8080)
- **Login:** `Admin` / `zabbix`

#### Workflow Tutorial

1. **Log in to Zabbix web UI.**
2. **Add a new host:**
   - Go to **Configuration > Hosts > Create host**.
   - Enter hostname and IP address.
   - Assign a group (e.g., Linux servers).
   - Add an interface (Agent or SNMP).
3. **Link templates:**
   - In the host config, go to **Templates** tab.
   - Link a template (e.g., `Template OS Linux`).
4. **Deploy Zabbix agent on the target host (if needed):**
   - On the target: `sudo dnf install zabbix-agent`
   - Edit `/etc/zabbix/zabbix_agentd.conf` to set `Server=192.168.56.30`
   - Start agent: `sudo systemctl enable --now zabbix-agent`
5. **Check data collection:**
   - Go to **Monitoring > Hosts** and check for green availability icons.
6. **Set up triggers and actions:**
   - Go to **Configuration > Hosts > Triggers** to add alerts.
   - Go to **Configuration > Actions** to set up notifications (email, etc.).

---

### ntopng

- **Purpose:** Real-time network traffic analysis and monitoring.
- **Access:** [http://192.168.56.30:3001](http://192.168.56.30:3001)
- **Login:** `admin` / `admin`

#### Workflow Tutorial

1. **Log in to ntopng web UI.**
2. **View traffic dashboard:**
   - See top talkers, flows, protocols, and traffic graphs.
3. **Analyze hosts and flows:**
   - Go to **Hosts** to see per-host traffic.
   - Go to **Flows** for detailed connection info.
4. **Set up alerts:**
   - Go to **Alerts** to view or configure traffic/event alerts.
5. **Export data:**
   - Use **Reports** or export CSV/JSON for further analysis.

---

### Ansible AWX

- **Purpose:** Web UI for managing Ansible playbooks, inventories, and jobs.
- **Access:** [http://192.168.56.30:8081](http://192.168.56.30:8081)
- **Login:** `admin` / `password` (set at first run or via container env)

#### Workflow Tutorial

1. **Log in to AWX web UI.**
2. **Create an organization (optional):**
   - Go to **Organizations > Add**.
3. **Add credentials:**
   - Go to **Credentials > Add**.
   - Choose type (e.g., SSH, Vault, etc.) and fill in details.
4. **Add an inventory:**
   - Go to **Inventories > Add**.
   - Add hosts/groups (by IP or hostname).
5. **Add a project:**
   - Go to **Projects > Add**.
   - Set SCM type (e.g., Git) and provide repo URL for playbooks.
6. **Create a job template:**
   - Go to **Templates > Add > Job Template**.
   - Select inventory, project, playbook, and credentials.
7. **Launch a job:**
   - Click the rocket icon on your job template.
   - Monitor job output in real time.
8. **View job history and results:**
   - Go to **Jobs** to see past runs, logs, and status.
9. **(Optional) Set up schedules and notifications:**
   - Use **Schedules** for recurring jobs.
   - Use **Notifications** for email, Slack, etc.

---

### GitLab CE

- **Purpose:** Self-hosted Git repositories, CI/CD pipelines, and DevOps platform.
- **Access:** [http://192.168.56.30:8929](http://192.168.56.30:8929)
- **First login:** Set a password for `root` user.
- **Usage:**  
  - Create groups and projects.
  - Push/pull code via HTTPS or SSH (port 2289).
  - Set up CI/CD pipelines in `.gitlab-ci.yml`.

## Customization

- Edit `playbook.yml` to add, remove, or configure containers.
- To persist data, mount host directories as Docker volumes (edit the playbook).
- For advanced configuration, refer to each tool's official documentation.

## Troubleshooting

- If a service is not reachable, check with `docker ps` and `docker logs <container>`.
- Ports may be changed in `playbook.yml` if needed.
- First boot may take several minutes as images are downloaded and initialized.
