import subprocess

def block_ip(ip):
    
    command = f"netsh advfirewall firewall add rule name=\'Block {ip}' dir=in action = block remoteip={ip}"
    subprocess.run(command, shell=True) 
    print(f"Ip blocked! IP: {ip}")

