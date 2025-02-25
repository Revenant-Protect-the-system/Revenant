#
# File containing all functions related and involving the 
# Monitoring/ sniffing of packets
#

import matplotlib.pyplot as plt
from scapy.all import *
from scapy.all import Ether, IP, TCP, UDP, ICMP
import logging
import time
import psutil

limit = 10
packet_Count = 0
protocol_counter = {'Ether' : 0, 'IP' : 0, 'TCP' : 0, 'UDP' : 0, 'ICMP' : 0}

def packetScan(packet):
    global packet_Count
    packet_Count += 1

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
    
    #print("Updating chart...")
    #plt.bar(protocol_counter.keys(), protocol_counter.values())
    #plt.xlabel("Protocol")
    #plt.ylabel("Packet Count")
    #plt.title("Packet Count per Protocol")
    #plt.show()


def capturePackets():
    # sniffs for packet(s) up to limit on the interface
    # prn executes the given function on each packet sniffed
    captured = sniff(prn=packetScan, count = limit)
    print("\n\n")
    print(protocol_counter)
    print(captured)

    return captured

def beginMonitoring():
    packets = capturePackets()

    return

beginMonitoring()