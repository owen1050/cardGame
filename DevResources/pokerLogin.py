import initialGUI, threading, requests, time, isRunning

readyToPlay = False
url = "http://192.168.1.229:23675"


print("Hello! Welcome to Owen's poker table. Email owen1050@gmail.com with issues")
uname = "player"
uPass = False
new = False
while uPass == False:
    new = False
    uname = input("Please enter username:")
    payload = "~un:"+uname + ":~"
    headers = {'Content-Length':str(len(payload))}

    r = requests.get(url = url, data = payload, headers = headers)
    update = r.text

    if(update.find("good") >=0):
        uPass = True
    if(update.find("new") >= 0):
        new = True


if new:
    print("This is a new username, if you incorrectly entered your username press control+c to cancel and re-enter")
    print("If this is your first time playing, enter your new password (DO NOT USE A SERIOS PASSWORD. Somthing like \"password\" is totally okay")
    pw = input("Password:")
    payload = "~pw:"+uname + ":" + pw + ":"
    headers = {'Content-Length':str(len(payload))}

    r = requests.get(url = url, data = payload, headers = headers)

    readyToPlay = True

else:
    pw = ""
    corPass = False
    while corPass == False:
        print("What is the password. If you forgot @owen on discord:")
        pw = input("Password:")
        payload = "~pw:"+uname + ":" + pw +":"
        headers = {'Content-Length':str(len(payload))}

        r = requests.get(url =  url, data = payload, headers = headers)
        update = r.text
        if(update.find("true") >= 0):
            print("Password correct")
            corPass = True
        else:
            print("Incorrect password, try again")
    readyToPlay = True

print("You are all set! Have fun " + uname)


def startPokerGame():
    global uname
    initialGUI.begin(uname)

def startTimeoutMon():
    global uname, isRunning

    while readyToPlay== False:
        time.sleep(0.1)

    time.sleep(3)
    while isRunning.isRunning:
        payload = "~alive:"+uname + ":~"
        headers = {'Content-Length':str(len(payload))}

        r = requests.get(url, data = payload, headers = headers)

        time.sleep(3)
                

t2 = threading.Thread(target = startTimeoutMon)
t2.start()

startPokerGame()
