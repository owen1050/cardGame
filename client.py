import requests

url = 'http://100.35.205.75:23659'

payload = "helloapp"
headers = {'Content-Length':str(len(payload))}


r = requests.get(url, data = payload, headers = headers)