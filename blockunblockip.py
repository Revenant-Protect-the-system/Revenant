import time
import sys
if sys.platform.startswith('win'):
    print("Running on Windows")
elif sys.platform.startswith('linux'):
    print("Running on Linux")
    import iptc             # NOTE: "iptc" (AKA "python-iptable") will only works on Linux and the library itself can only be downloaded on a Linux system.

blocked = {}

BLOCK_TIME = 9000  

def block_ip(ip):
    if sys.platform.startswith('win'):
        print(f"<Pretend ip \"{ip}\" is blocked>")
    elif sys.platform.startswith('linux'):
        if ip in blocked:
            return  

        rule = iptc.Rule()
        rule.src = ip
        rule.protocol = "tcp"  
        target = iptc.Target(rule, "DROP")
        rule.target = target

        chain = iptc.Chain(iptc.Table(iptc.Table.FILTER), "INPUT")
        chain.insert_rule(rule)

        blocked[ip] = time.time()
        print(f"Blocked {ip}")

def unblock_expired():
    if sys.platform.startswith('win'):
        print("<unblock_expired()>")
    elif sys.platform.startswith('linux'):
        now = time.time()
        chain = iptc.Chain(iptc.Table(iptc.Table.FILTER), "INPUT")

        for ip, timestamp in list(blocked.items()):
            if now - timestamp >= BLOCK_TIME:
            
                for rule in chain.rules:
                    if rule.src == ip and rule.target.name == "DROP":
                        chain.delete_rule(rule)
                        print(f"Unblocked {ip}")
                        break
                del blocked[ip]
