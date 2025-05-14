import time
import numpy as np
import blockunblockip
import notificationCode





DDOS_BYTES_PER_SECOND = 20000                  # IF more than this many Bytes are sent through the network by an individual IP: then it's flagged as a DDoS attack
DDOS_PACKETS_PER_SECOND = 400                   # IF more than this many packets are sent by an individual IP: then it's flagged as a DDoS attack
adminEmails = list()

def Check_For_DDoS(data, time_gap):
    # 1. log every IP in data
    ip_dict = dict()
    for row in data:
        ip = row[0]
        ip_dict[ip] = [0,0,False]               # ip_dict[ip][0] = instances
                                                # ip_dict[ip][1] = bandwidth taken
                                                # ip_dict[ip][2] = suspected of being a DDoS attack
    # 2. Count instances and total taken bandwidth by every IP
    for row in data:
        ip = row[0]
        ip_dict[ip][0] += 1             # Add 1 for ever instance of a key
        ip_dict[ip][1] += row[2]        # Add PACKET_SIZE for ever instance of a key
    # 3. Divide results by the packet collecting time to get how many instances and MB were sent per second
    for ip in ip_dict.keys():
        ip_dict[ip][0] /= time_gap
        ip_dict[ip][1] /= time_gap
    # 4. Go through all IPs and flag ones that loop like DDoS
    for ip in ip_dict.keys():
        # 5.1. IF an IP has appeared over 20 times per second: flag as DDoS
        if ip_dict[ip][0] > DDOS_PACKETS_PER_SECOND:
            print(f"suspected Volumetric DDoS attack by ip \"{ip}\"!")
            ip_dict[ip][2] = True
        # 5.2. IF an IP has uploaded over 2B/s: flag as DDoS
        if ip_dict[ip][1] > DDOS_BYTES_PER_SECOND:
            print(f"suspected Aplication Layer DDoS attack by ip \"{ip}\"!")
            ip_dict[ip][2] = True

    # <TESTING>
    print("Contents of 'ip_array':")
    for ip in ip_dict.keys():
        instances = ip_dict[ip][0]
        bandwidth = ip_dict[ip][1]
        print(f"ip {ip} sends {instances:.2f} packets/s and consumes {bandwidth:.2f} Bytes/s!")
    # </TESTING>
    
    return ip_dict