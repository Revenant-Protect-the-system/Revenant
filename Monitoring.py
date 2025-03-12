#
# File containing all functions related and involving the 
# Monitoring/ sniffing of packets
#

import numpy as np
from matplotlib.tri import Triangulation
import matplotlib.pyplot as plt
from scapy.all import *
from scapy.all import Ether, IP, TCP, UDP, ICMP
import logging
import time
import psutil

from DatabaseManager import Database

limit = 1000
packet_Count = 0
protocol_counter = {'Ether' : 0, 'IP' : 0, 'TCP' : 0, 'UDP' : 0, 'ICMP' : 0}
main_Database = Database()

def printChart():
    
    protocols = list(protocol_counter.keys())
    # List of packet counts (y-axis)
    values = list(protocol_counter.values())

    # Create the scatter plot
    plt.figure(figsize=(8, 6))
    plt.scatter(protocols, values, color='blue', s=100, edgecolors='black', alpha=0.7)

    # Add labels and title to the plot
    plt.xlabel("Protocol")
    plt.ylabel("Packet Count")
    plt.title("Packet Count per Protocol (Scatter Plot)")
    
    # Add grid for better readability
    plt.grid(True, which='both', linestyle='--', linewidth=0.5)

    # Add annotation to each point (optional)
    for i, protocol in enumerate(protocols):
        plt.text(protocols[i], values[i], f"{values[i]}", ha='center', va='bottom', fontsize=15)

    # Show the plot
    plt.tight_layout()
    plt.show()

def logPacket(packet):
    if packet.haslayer(Ether):
        main_Database.Add(packet[Ether].src)
    elif packet.haslayer(IP):
        main_Database.Add(packet[IP].src)
    else:
        None

def packetScan(packet):
    global packet_Count
    packet_Count += 1
    
    logPacket(packet)

    if packet.haslayer(Ether):
        print(f"Ethernet Layer : {packet[Ether].src} > {packet[Ether].dst}")    
        protocol_counter['Ether'] += 1
    if packet.haslayer(IP):
        print(f"IP Layer : {packet[IP].src} > {packet[IP].dst}")    
        protocol_counter['IP'] += 1
    if packet.haslayer(TCP):
        print(f"TCP Packet : {packet[TCP].sport} > {packet[TCP].dport}")    
        protocol_counter['TCP'] += 1
    if packet.haslayer(UDP):
        print(f"UDP Packet : {packet[UDP].sport} > {packet[UDP].dport}")    
        protocol_counter['UDP'] += 1
    if packet.haslayer(ICMP):
        print(f"ICMP Packet : Type - {packet[ICMP].type} , Code - {packet[ICMP].code}")   
        protocol_counter['ICMP'] += 1
    

def capturePackets():
    # sniffs for packet(s) up to limit on the interface
    # prn executes the given function on each packet sniffed
    captured = sniff(prn=packetScan, count = limit)
    print("\n\n")
    print(protocol_counter)
    print(captured)
    print("\n\n\n\n\n\n\n")
    main_Database.Print()
    printChart()
    main_Database.Save()
    return captured

def beginMonitoring():
    packets = capturePackets()

    return

beginMonitoring()