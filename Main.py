# 1. import all assets
import time
import GUI
import Firewall
import numpy as np
import blockunblockip
import DatabaseManager
import notificationCode
from scapy.all import *
from scapy.all import Ether, IP, TCP, UDP, ICMP

# 2. Initialise global variables/objects
database = DatabaseManager.Database_Class()                 # 2.1. Instantiate Database
gui = GUI.GUI_Class(1000, 600)                            # 2.2. Instantiate GUI
data_cache = list()
data_cache_capacity = 1000

# 3. Introduce functions used
def LogPacket(packet):
    # 1. Get next index in "data_cache"
    global data_cache

    error = False

    add = [1,2,3,4]
    # 2.1. Get IP
    if packet.haslayer(IP):
        add[0] = packet[IP].src
    elif packet.haslayer(Ether):
        add[0] = packet[Ether].src
        print("ERROR: only ethernet connection:")
        error = True
    # 2.2. Get source location 
    if packet.haslayer(Ether):
        add[1] = packet[Ether].src
    if packet.haslayer(IP):
        add[1] = packet[IP].src
    if packet.haslayer(TCP):
        add[1] = packet[TCP].sport
    if packet.haslayer(UDP):
        add[1] = packet[UDP].sport
    if packet.haslayer(ICMP):               # NOTE: ICMPs are very popular for DDoS!!!
        add[1] = packet[ICMP].type
    # 2.3. Get file size of the packet
    add[2] = len(packet)
    # 2.4. Get time of the packet's arrival
    add[3] = float(time.time())
    # 3. Add to the data cache
    if error:
        print("-",add)
    data_cache.append(add)
    if len(data_cache) > data_cache_capacity:
        del data_cache[0]
    
    database.Add(packet)




# INITIAL variables to setup before main loop:
database.Open()
# 3. Activate main loop:
try:
    while True:                                             # Repeat endlessly until a "Close_Window" exception is thrown
        # 3.1. Collect one seconds worth of Packets
        data_cache = list() # Wipe the list so that we aren't going over old data
        packet_capture_time = 1.0
        time_start = time.time()
        time_end = time_start + packet_capture_time
        while time.time() < time_end:                       # only close after <packet_capture_time> seconds
            sniff(prn=LogPacket, count=1)
        packet_capture_time = time.time() - time_start      # Due to delay, the packet may take longer to capture

        # 3,2. Scan input packets for DDoS looking activity
        ip_dict = Firewall.Check_For_DDoS(data_cache, packet_capture_time)
        # 3.3. Block/and email admins of any sispicious IPs
        for ip in ip_dict.keys():
            if ip_dict[ip][2] == True:
                print(f"blocking suspicious ip \"{ip}\"")
                blockunblockip.block_ip(ip)
                print("notifying admins")
                for admin in admin_emails.emails:
                    message = ""
                    if ip[1] == "volume":
                        message = f'''Dear Admin
                        
                        a suspected volumetric DDoS attack has been detected by IP \"{ip[0]}\". 
                        Revenant has responded by temporarily blocking the IP for {blockunblockip.BLOCK_TIME} seconds.
                        If you want to block the IP, please console "Database.txt" for ip \"{ip[0]}\" before time {time.time()}s
                        
                        yours faithfully Revenant'''
                    if ip[1] == "layer":
                        message = f'''Dear Admin
                        
                        a suspected aplication layer DDoS attack has been detected by IP \"{ip[0]}\". 
                        Revenant has responded by temporarily blocking the IP for {blockunblockip.BLOCK_TIME} seconds.
                        If you want to block the IP, please console "Database.txt" for ip \"{ip[0]}\" before time {time.time()}s
                        
                        yours faithfully Revenant'''
                    
                    notificationCode.sendEmail(admin, "Revenant: Temporarily blocked suspected DDoS attack", message)
                    print("- Emailed", admin)
        # convert "ip_dict" into a format "gui" can use
        ip_list = list()
        for ip in ip_dict.keys():
            ip_list.append( (ip, ip_dict[ip][0], ip_dict[ip][1], ip_dict[ip][2]) )
        print("ip_list =", ip_list)
        # Create 1 frame of the GUI
        gui.Input(ip_list)
        gui.Update(ip_list)
        gui.Render()
        print("\n")
except GUI.Close_Window:
    # 4. Close & Save all tools used
    gui.Close()
    database.Save()
