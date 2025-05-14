# 1. import all assets
import time
import GUI
import Firewall
import numpy as np
import DatabaseManager
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

    add = [1,2,3,4]
    # 2.1. Get IP
    if packet.haslayer(Ether):
        add[0] = packet[Ether].src
    elif packet.haslayer(IP):
        add[0] = packet[IP].src
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
        packet_capture_time = 1.0
        time_start = time.time()
        time_end = time_start + packet_capture_time
        while time.time() < time_end:                       # only close after <packet_capture_time> seconds
            sniff(prn=LogPacket, count=1)
        packet_capture_time = time.time() - time_start      # Due to delay, the packet may take longer to capture
        

        # 3,2. Scan input packets for DDoS looking activity
        under_attack = Firewall.Check_For_DDoS(data_cache, packet_capture_time)
        # 3.3. IF there's a suspected DDoS attack:
        if under_attack:
            pass
            # 3.3.1. Block the ip
            # 3.3.2. Email the Admin
        # Create 1 frame of the GUI
        gui.Input(data_cache)
        gui.Update()
        gui.Render()
        print("\n\n\n")
except GUI.Close_Window:
    pass

# 4. Close & Save all tools used
gui.Close()
database.Save()
