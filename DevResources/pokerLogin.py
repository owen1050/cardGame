import initialGUI, threading, requests

print("Hello! Welcome to Owen's poker table. Email owen1050@gmail.com with issues")
uname = "player"
while uname.find("player") >= 0 or uname.find("PICH") >= 0 :
    uname = input("Please enter username:")

pw = ""
corPass = False
while corPass == False:
    pw = input("What is the password (do not use a serious password):")
    payload = "~pw:"+uname + ":" + pw
    headers = {'Content-Length':str(len(payload))}

    r = requests.get(url, data = payload, headers = headers)
    update = r.text

pw = "a" #input("password:")
print(uname)


def startPokerGame():
    global uname
    initialGUI.begin(uname)

def startTimeoutMon():
    global uname
    while True:
        payload = "~alive:"+uname + "~"
        headers = {'Content-Length':str(len(payload))}

        r = requests.get(url, data = payload, headers = headers)
        update = r.text
    


t = threading.Thread(target = startPokerGame)
t.start()

t2 = threading.Thread(target = startTimeoutMon)
t2.start()
