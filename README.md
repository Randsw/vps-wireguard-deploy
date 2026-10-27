# WireGuard VPS Deployer

Automated Ansible playbooks to harden a fresh VPS and deploy a WireGuard VPN server with automated client configuration generation.

## 📋 Requirements

* **Ansible** on the control node (with the `ansible.posix` collection: `ansible-galaxy collection install ansible.posix`)
* A fresh **Debian/Ubuntu** VPS reachable over SSH with:
  * The server IP address
  * Root credentials (password or SSH key)

## 🚀 Quick Start

Most cheap VPS providers only give you an **IP address** and a **root password**. This repository automates the transition from a "raw" server to a secured VPN gateway.

### 1. Host Connection

Set your VPS IP address in `inventories/wireguard/hosts.yml`:

```yaml
ansible_host: 192.168.0.93
```

### 2. Authentication

Set your root credentials in `inventories/wireguard/host_vars/wireguard_server.yaml`:

```yaml
ansible_user: root
ansible_password: "your_root_password"
```

## 🛠️ Configuration

### Global Settings

In `inventories/wireguard/host_vars/wireguard_server.yaml`:

* **prepare_vps**: (bool) Set to `false` if you want to skip the hardening process.
* **local_user**: Your local OS username (used for SSH keys generation).

### Role: VPS Preparation (`roles/prepare-vps`)

This role secures the server by creating a non-root sudo user and disabling root login and password-based SSH authentication. Configuration in `roles/prepare-vps/defaults/main.yml`:

| Variable | Description | Default |
| :--- | :--- | :--- |
| **ssh_key_path** | Path to an existing public key to authorize. Keys are generated if this var is an empty string | `""` |
| **generate_ssh_folder** | Where to store newly generated keys. | `~/.ssh` |
| **wg_user** | The sudo user created to replace root access. | `wgadmin` |

The role performs the following steps:

1. Updates the APT package cache.
2. Generates a dedicated SSH key pair (`wg_vps`) if `ssh_key_path` is empty.
3. Creates the `wg_user` sudo user with passwordless sudo and authorizes the SSH key.
4. Creates swap space if none exists.
5. Hardens SSH: disables root login and password authentication.

### Role: WireGuard Deployment (`roles/wireguard`)

Configuration in `roles/wireguard/defaults/main.yml`:

| Variable | Description | Default |
| :--- | :--- | :--- |
| **vpn_network** | The VPN subnet. | `10.130.130` |
| **vpn_port** | The port the VPN server listens on for incoming connections. | `51820` |
| **clients** | Number of client configs to generate. | `15` |
| **client_config_path** | Local filesystem path where client configurations are stored. | `~/wireguard_role/profiles` |

The role performs the following steps:

1. Installs WireGuard and prerequisites on the server.
2. Generates server and client keys and enables the `wg0` interface.
3. Sets up NAT and firewall rules.
4. Fetches the generated client configs back to the control node.

## 📖 Usage

Run the playbook:

```bash
ansible-playbook -i inventories/wireguard/hosts.yml deploy-wireguard-server.yaml
```

After completion, your client configurations will be available in the `client_config_path` directory.

### Adding a client later

To add an extra client to an already-deployed server, run only the `add_client` tag:

```bash
ansible-playbook -i inventories/wireguard/hosts.yml deploy-wireguard-server.yaml --tags add_client
```

The new client's name and IP are defined by the `new_client` and `new_client_ip` variables in `roles/wireguard/tasks/additional_client.yml` — adjust them before running.

### Re-running after hardening

Once `prepare-vps` has run, root SSH login and password authentication are disabled. For subsequent runs, update `inventories/wireguard/hosts.yml` to connect as the new sudo user with the generated key:

```yaml
ansible_user: wgadmin
ansible_ssh_private_key_file: ~/.ssh/wg_vps
```

## 📁 Repository Structure

```
├── deploy-wireguard-server.yaml   # Main playbook
├── inventories/wireguard/         # Inventory and host variables
└── roles/
    ├── prepare-vps/               # VPS hardening role
    └── wireguard/                 # WireGuard deployment role
```

## 🔒 Security Notes

* Client private keys and configs are generated on the server and fetched locally; keep `client_config_path` safe.
* The sudo user is created with passwordless sudo — this is required so Ansible can escalate after password authentication is disabled.
* SSH hardening disables root login and password authentication; make sure the generated key works before closing your current session.
