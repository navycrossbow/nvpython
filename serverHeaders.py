import requests
import os.path
import sys
from pathlib import Path


urls = [
    "www.facebook.com",
    "www.google.com"
]

badFlags = [
    "Server".lower(),
    "X-AspNet-Version".lower(),
    "X-Runtime".lower(),
    "X-Version".lower(),
    "X-Powered-By".lower()
]

def getUrlContent(url):
    req = requests.get("https://" + url)
    return req.headers



for url in urls:
    header = getUrlContent(url)
    print("URL:\t" + url )
    for key,val in header.items():
        if (key.lower()) in badFlags:
            print ("BAD\t\t" + key + ": " + val)
        else:
            print ("\t\t" + key + ": " + val)
    print("***************************************")

