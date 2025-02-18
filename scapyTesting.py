# Scapy Testing for Project
# To use have the following:
#   pip install scapy
#   "Add Python to PATH" (for executable with scapy)
#   To do, Add enviroment variables 
#       "C:\Users\<User>\AppData\Local\Programs\Python\Python311\"
#       "C:\Users\<User>\AppData\Local\Programs\Python\Python311\Scripts\"

# Move Site-Packages for scapy to correct folder to execute
#   only if " No module named 'scapy.all' " is shown
from scapy.all import *

t = AsyncSniffer(iface="", count=2)
t.start()
t.join()  # this will hold until 200 packets are collected
results = t.results
print(len(results))
print(results)

print(conf.ifaces)
print(dev_from_index(6))
print(network_name(conf.iface))
print(resolve_iface(conf.iface))
print(dev_from_networkname(conf.iface))
print(conf.iface)