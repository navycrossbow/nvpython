#Given a set of domains, this script will query the zScaler API and return their category

import sys
# insert at 1, 0 is the script path (or '' in REPL)
sys.path.insert(0, '/dev/config/')


import config

import time
import http.client
import json

print(config.zscaler_baseuri)

#https://help.zscaler.com/zia/api-getting-started
def obfuscateApiKey (apiKey):
    seed = apiKey #'YOUR_API_KEY'
    now = int(time.time() * 1000)
    n = str(now)[-6:]
    r = str(int(n) >> 1).zfill(6)
    key = ""
    for i in range(0, len(str(n)), 1):
        key += seed[int(str(n)[i])]
    for j in range(0, len(str(r)), 1):
        key += seed[int(str(r)[j])+2]
    return key
    #print("Timestamp:", now, "\tKey", key)

def getTimeStamp():
    now = int(time.time() * 1000)
    return now

#gets an authenticated session id
def getAuthenticatedSessionId():
    conn = http.client.HTTPSConnection(config.zscaler_baseuri)
    timestamp = getTimeStamp()
    headers = {
        'content-type': "application/json",
        'cache-control': "no-cache"
    }
    payload = {
        "apiKey" : obfuscateApiKey(config.zscaler_apikey),
        "username": config.zscaler_username,
        "password": config.zscaler_password,
        "timestamp": timestamp
    }
    url = "/api/v1/authenticatedSession"
    conn.request('POST', url, json.dumps(payload), headers)
    response = conn.getresponse()
    headers = response.getheaders()

    sessionId = ''
    for i in headers:
        if 'JSESSIONID' in str(i):
            s1 = str(i).split(',')
            s2 = s1[1].split(';')
            s3 = s2[0].replace(" 'JSESSIONID=", "")
            sessionId = s3
            break
    return (sessionId)


def getUrlLookup(sessionid, payload):
    authenticatedHeaders = {
        'content-type': "application/json",
        'cache-control': "no-cache",
        'cookie': "JSESSIONID="+sessionid
    }
    conn = http.client.HTTPSConnection(config.zscaler_baseuri)
    url = "/api/v1/urlLookup"
    conn.request('POST', url, json.dumps(payload), authenticatedHeaders)
    lookupResponse = conn.getresponse()
    data = lookupResponse.read()
    print(data)
    d1 = data.decode("utf-8")
    d2 = json.loads(d1)
    print(d2)


payload = [
    "viruses.org",
    "facebook.com",
    "bbc.com"
]

sessionid = getAuthenticatedSessionId()
print (sessionid)
getUrlLookup(sessionid, payload)
