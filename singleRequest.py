import requests

url = 'http://192.168.1.229:23666'

payload = "~!owen!action:startHand:1:~"
payload = "~!kerry!action:fold:1:~"
#payload = "~update"
headers = {'Content-Length':str(len(payload))}

r = requests.get(url, data = payload, headers = headers)
print(r.text)