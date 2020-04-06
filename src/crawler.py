#!/usr/bin/env python
import requests
import re
import urllib.parse as urlparse

target_url = "https://rootino.ir"


def extract_link(url):
    res = requests.get(url)
    return re.findall('(?:href=")(.*?)"', str(res.content))

target_links = []

def crawler(url):
    links = extract_link(url)
    for link in links:
        link = urlparse.urljoin(url, link)
        if "#" in link:
            link = link.split("#")
        if url in link and link not in  target_links:
            target_links.append(link)
            crawler(url)
            print(link)

crawler(target_url)