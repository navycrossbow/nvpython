import requests
import os.path
import sys
from pathlib import Path


def getUrlContent(url):
    req = requests.get(url)
    return req.content


def saveToFile(filepath, content):
    with open(filepath, 'wb') as r: 
        r.write(content)



url = "https://raw.githubusercontent.com/insidetrust/statistically-likely-usernames/master/john.smith.txt"

filepath = Path(__file__).parent / "./data/john.smith.txt"
saveToFile(filepath, getUrlContent(url))