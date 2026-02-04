# Deploy wireguard server on VPS and generate client keys

Common:
ansible_host
ansible_user
ansible_password
prepare_vps
local_user

Prepare-vps:
ssh_key_path:
generate_ssh_folder:
wg_user: "wgadmin"

Wireguard:
vpn_network
vpn_port
clients
client_config_path