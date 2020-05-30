import requests

url = 'http://192.168.1.254:23659'

payload = "~update:ben:~"
headers = {'Content-Length':str(len(payload))}


r = requests.get(url, data = payload, headers = headers)
print(r.text)
