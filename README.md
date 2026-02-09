# WireGuard VPS Deployer

Automated Ansible playbooks to harden a fresh VPS and deploy a WireGuard VPN server with automated client configuration generation.

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
ansible_password: "your_root_password"
```

## 🛠️ Configuration

### Global Settings

In `inventories/wireguard/host_vars/wireguard_server.yaml`:

* **prepare_vps**: (bool) Set to `false` if you want to skip the hardening process.
* **local_user**: Your local OS username (used for SSH keys generation).

### Role: VPS Preparation (`roles/prepare-vps`)

This role secures the server by creating a non-root sudo user and disabling root login and password-based SSH authentication. Configuration in `roles/prepare-vps/defaults/main.yml`:

| Variable | Description | Example |
| :--- | :--- | :--- |
| **ssh_key_path** | Path to an existing public key to authorize. Generate keys if this var is empty string | `/home/user/.ssh/id_rsa.pub` |
| **generate_ssh_folder** | Where to store new keys if generation is needed. | `~/.ssh` |
| **wg_user** | The sudo user created to replace root access. | `wgadmin` |

### Role: WireGuard Deployment  (`roles/wireguard`)

Configuration in `roles/wireguard/defaults/main.yml`:

| Name | Description | Default |
| :--- | :--- | :--- |
| **vpn_network** | Declare the VPN subnet | `10.203.200` |
| **vpn_port** | The port the VPN server listens on for incoming connections. | `51820` |
| **clients** | A number of client to generate configs for. | `15` |
| **client_config_path** | Local filesystem path where client configurations are stored. | `~/wireguard_role/profiles` |

## 📖 Usage

Run the playbook:

```bash
ansible-playbook -i inventories/wireguard/hosts.yml deploy-wireguard-server.yaml
```

After completion, your client configurations will be available in the `client_config_path` directory.
