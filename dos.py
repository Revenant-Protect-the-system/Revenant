from scapy.all import *
from scapy.all import IP, ICMP, TCP, UDP
#tests conectiveity with ping test
def con_test(ip): 
    ans, unans =srp(IP(dst=ip)/ICMP()/"testICMPpacket",timeout=5)
    print(ans,"\n",unans)
#ip= input("enter the ip of destination: ")
ip = "" # put ip here
#con_test(ip)
send(IP(dst=ip)/UDP()/"testUDPpacket",count=20)