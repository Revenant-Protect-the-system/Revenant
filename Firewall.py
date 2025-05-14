import time
import numpy as np
#import blockunblockip
import notificationCode

class blockunblockip: ############################################# Placeholder
    BLOCK_TIME = 9000 ############################################# Placeholder




DDOS_BYTES_PER_SECOND = 300000                  # IF more than this many Bytes are sent through the network by an individual IP: then it's flagged as a DDoS attack
DDOS_PACKETS_PER_SECOND = 400                   # IF more than this many packets are sent by an individual IP: then it's flagged as a DDoS attack
adminEmails = list()

def Check_For_DDoS(data, time_gap):
    # 1. log every IP in data
    ip_dict = dict()
    for row in data:
        ip_dict[row[0]] = 0
    i = 0
    # 2. Assign a numerical id to all IPs
    for key in ip_dict.keys():
        ip_dict[key] = i
        i += 1

    # 3. create list to store all ip data in
    ip_array = np.full((len(ip_dict), 5), 0)
    for i in range(len(ip_dict)):
        ip_array[i][0] = i

    # 4. Give every IP the following data
    for row in data:
        dict_key = row[0]
        array_key = ip_dict[dict_key]
        # 4.1. how many packets have been recieved by an individual IP
        ip_array[array_key][1] += 1
        # 4.2. How many bytes of data that IP has pushed through the network
        ip_array[array_key][2] += row[2]
    # 4.3. Make all data relative to the time it was taken over
    for i in range(len(ip_array)):
        ip_array[i][1] /= time_gap
        ip_array[i][2] /= time_gap

    # 5. Go through all IPs and flag ones that loop like DDoS
    ip_dict_inverted = {v: k for k, v in ip_dict.items()}
    sus_ips = list()
    for row in ip_array:
        ip = ip_dict_inverted[ row[0] ]
        # 5.1. IF an IP has appeared over 20 times per second: flag as DDoS
        if row[1] > DDOS_PACKETS_PER_SECOND:
            print(f"suspected Volumetric DDoS attack by ip \"{ip}\"!")
            sus_ips.append((ip, "volume"))
            continue
        # 5.2. IF an IP has uploaded over 2B/s: flag as DDoS
        if row[2] > DDOS_BYTES_PER_SECOND:
            print(f"suspected Aplication Layer DDoS attack by ip \"{ip}\"!")
            sus_ips.append((ip, "layer"))
            continue
    
    for ip in sus_ips:
        print(f"blocking suspicious ip \"{ip[0]}\"")
        #blockunblockip.block_ip(ip[0])##############################################################################################
        print("notifying admins")
        for admin in adminEmails:
            message = ""
            if ip[1] == "volume":
                message = f'''Dear Admin
                
                a suspected volumetric attack has been detected by IP \"{ip[0]}\". 
                Revenant has responded by temporarily blocking the IP for {blockunblockip.BLOCK_TIME} seconds.
                If you want to block the IP, please console "Database.txt" for ip \"{ip[0]}\" before time {time.time()}s
                
                yours faithfully Revenant'''
            notificationCode.sendEmail(admin, "Suspected DDoS attack has been blocked")


    # <TESTING>
    print("Contents of 'ip_array':")
    for i in range(len(ip_dict)):
        ip = ip_dict_inverted[i]
        packets = ip_array[i][1]
        bytes = ip_array[i][2]
        print(f"ip {ip} sends {packets} packets/s and consumes {bytes} Bytes/s!")
    # </TESTING>
    
    return False###############################################################