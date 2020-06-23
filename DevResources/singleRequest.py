import requests

url = 'http://192.168.1.151:23666'

payload = "~!owen!action:remove:1:~"
#payload = "~!owen!action:bet:10:~"
payload = "~update"
headers = {'Content-Length':str(len(payload))}

r = requests.get(url, data = payload, headers = headers)
print(r.text)