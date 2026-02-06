# Deploy wireguard server on VPS and generate client keys

A cheap VPS hoster usually provide you only VPS IP address and root password.

Goal of this repository is prepare VPS for real world:) and deploy Wireguard.

## Configure

Set VSP IP in `inventories/wireguard/hosts.yml`
`ansible_host: 192.168.0.93`

Set root creadetials in `inventories/wireguard/host_vars/wireguard_server.yaml`
`ansible_password: vps`

If you dont want prepare harden your VSP set `prepare_vps` to false in 
`inventories/wireguard/host_vars/wireguard_server.yaml`

Set your local user name in `inventories/wireguard/host_vars/wireguard_server.yaml`
`local_user: vps`
Its used to generate ssh key

### Configure prepare VPS role

Prepare-vps:
ssh_key_path:
generate_ssh_folder:
wg_user: "wgadmin"

Wireguard:
vpn_network
vpn_port
clients
client_config_path