import iptc
import time

blocked = {}

BLOCK_TIME = 9000  

def block_ip(ip):
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
