import iptc
import time

blocked = {}  # { ip: timestamp }

BLOCK_TIME = 3600  # seconds

def block_ip(ip):
    if ip in blocked:
        return  # already blocked

    rule = iptc.Rule()
    rule.src = ip
    rule.protocol = "tcp"  # optional, or "udp", or leave blank
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
            # Find the rule and remove it
            for rule in chain.rules:
                if rule.src == ip and rule.target.name == "DROP":
                    chain.delete_rule(rule)
                    print(f"Unblocked {ip}")
                    break
            del blocked[ip]