import requests

url = 'http://192.168.1.229:23663'

setup = False
if setup:

    payload = "~update~"
    headers = {'Content-Length':str(len(payload))}

    r = requests.get(url, data = payload, headers = headers)
    print(r.text)

    payload = "~!Owen1!~"
    headers = {'Content-Length':str(len(payload))}

    r = requests.get(url, data = payload, headers = headers)
    print(r.text)

    payload = "~update~"
    headers = {'Content-Length':str(len(payload))}

    r = requests.get(url, data = payload, headers = headers)
    print(r.text)

#payload = "~!Owen2!action:bet:10000:~"
payload = "~update~"
headers = {'Content-Length':str(len(payload))}

r = requests.get(url, data = payload, headers = headers)
print(r.text)