import os
import testinfra.utils.ansible_runner


testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')

def test_listening_wireguard(host):
    assert host.socket("udp://0.0.0.0:51820").is_listening

def test_wireguard_config_exist(host):
    wg_conf = host.file('/etc/wireguard/wg0.conf')
    assert wg_conf.exists    

def test_wireguard_is_running(host):
    assert host.service('wg-quick@wg0.service').is_running