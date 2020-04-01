#!/usr/bin/env python

import scapy.all as scapy
import argparse


def get_argument():
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--target", dest="target",
                        help="Please specify the target IP or IP range")
    options = parser.parse_args()
    return options


def scan_ip(ip):
    req = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    req_broadcast = broadcast/req
    answered, unanswered = scapy.srp(req_broadcast, verbose=False, timeout=1)

    ip_mac_list = []

    for item in answered:
        ip_mac_dict = {"ip": item[1].psrc, "mac": item[1].hwsrc}
        ip_mac_list.append(ip_mac_dict)

    return ip_mac_list


def print_ip_mac_pair(items):
    print("IP\t\t\tMAC Address\n-----------------------------------------")
    for item in items:
        print(f"{item['ip']}\t\t{item['mac']}")


options = get_argument()
result = scan_ip(options.target)
print_ip_mac_pair(result)
