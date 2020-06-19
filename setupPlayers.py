import requests

url = 'http://192.168.1.229:23666'



setup = True
if setup:
    names = ["owen", "josh", "jake", "thomas", "kerry", "jason", "byron", "Amy"]
    
    for i in range(len(names)) :
        payload = "~!" + names[i]+ "!~"
        headers = {'Content-Length':str(len(payload))}

        r = requests.get(url, data = payload, headers = headers)
        print(r.text)

        payload = "~!" + names[i]+ "!action:setChips:" + str(i) +"~"
        headers = {'Content-Length':str(len(payload))}

        r = requests.get(url, data = payload, headers = headers)
        print(r.text)

        payload = "~!" + names[i]+ "!action:bet:" + str(i) +"~"
        headers = {'Content-Length':str(len(payload))}

        r = requests.get(url, data = payload, headers = headers)
        print(r.text)


payload = "~!owen!action:startHand:1:~"
#payload = "~update"
headers = {'Content-Length':str(len(payload))}

r = requests.get(url, data = payload, headers = headers)
print(r.text)