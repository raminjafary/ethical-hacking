#!/usr/bin/env python

import subprocess
import optparse
import re


def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option("-i", "--interface", dest="interface",
                      help="Interface to change the MAC address")
    parser.add_option("-m", "--macc", dest="new_mac",
                      help="The new MAC address")
    (options, arguments) = parser.parse_args()
    if not options.interface:
        parser.error("Please specify an interface argument")
    elif not options.new_mac:
        parser.error("Please specify an interface argument")
    return options


def change_mac_address(interface, mac_address):
    print(f"Changing MAC address for interface {interface} to {mac_address}")
    subprocess.call(["ifconfig", interface, "down"])
    subprocess.call(["ifconfig", interface, "hw", "ether", mac_address])
    subprocess.call(["ifconfig", interface, "up"])


def get_current_mac_address(interface):
    ifconfig_res = subprocess.check_output(["ifconfig", interface])
    mac = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w", ifconfig_res)
    if mac:
        return mac.group(0)
    else:
        return "Could not find the MAC address"


(interface, mac_address) = get_arguments()
current_mac = get_current_mac_address(interface)
change_mac_address(interface, mac_address)
current_mac = get_current_mac_address(interface)

if current_mac == mac_address:
    print(
        f"MAC address was changed for interface {interface} to {mac_address}")
else:
    print("MAC address did not changed!")
