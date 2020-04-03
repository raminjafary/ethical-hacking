#!/usr/bin/env python

import scapy.all as scapy


def get_mac_address(ip):
    req = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    req_broadcast = broadcast/req
    answered = scapy.srp(req_broadcast, verbose=False, timeout=1)[0]
    return answered[0][1].hwsrc


def sniff(interface):
    scapy.sniff(iface=interface, store=False, prn=process_data)


def process_data(packet):
    if packet.haslayer(scapy.ARP) and packet[scapy.ARP].op == 2:
        try:
            real_mac = get_mac_address(packet[scapy.ARP].psrc)
            response_mac = packet[scapy.ARP].hwsrc
            if real_mac != response_mac:
                print("You are under attack..!")
        except IndexError:
            pass


sniff("your ineterface")
