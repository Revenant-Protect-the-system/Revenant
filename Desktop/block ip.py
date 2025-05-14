import subprocess

def block_ip(ip_address):
    command = f'netsh advfirewall firewall add rule name="Block {ip_address}" dir=in action=block remoteip={ip_address}'
    subprocess.run(command, shell=True, check=True)
    print(f"Blocked IP: {ip_address}")

block_ip("192.168.1.100")

