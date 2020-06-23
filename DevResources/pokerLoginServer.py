import requests, threading, time, isRunning
from http.server import BaseHTTPRequestHandler, HTTPServer

activePlayers = []
url = 'http://192.168.1.229:23662'

class server(BaseHTTPRequestHandler):

    def log_message(self, format, *args):
        return

    def onSucLogin(self, name):
        global activePlayers, url

        
        bank = {}
        f = open("bank.txt", "r")
        fin = f.read()
        f.close()
        i0 = 0
        i1 = 0
        i2 = 0
        while(i2 + 2 < len(fin)):
            i0 = fin.find("!", i2)
            i1 = fin.find(":", i0)
            i2 = fin.find("!", i1)

            un = fin[i0+1:i1]
            pw = fin[i1+1:i2]
            bank[un] = int(pw)
        print("bank after login", bank)

        if name in bank:
            payload = "~!" + name+"!setChips:" + str(bank[name])+ ":~"
            headers = {'Content-Length':str(len(payload))}
            r = requests.get(url = url, data = payload, headers = headers)
            payload = "~!" + name+"!setChips:" + str(bank[name])+ ":~"
            headers = {'Content-Length':str(len(payload))}
            r = requests.get(url = url, data = payload, headers = headers)

        else:
            bank[name] = 1000

        fileOut = "!"
        for user in bank:
            fileOut = fileOut + user + ":" + str(bank[user]) + "!"

        print("File:",fileOut)
        f = open("bank.txt", "w")
        f.write(fileOut)
        f.close()

        activePlayers.append({name:time.time()})

    def do_GET(self):
        global activePlayers


        
        logins = {}
        f = open("logins.txt", "r")
        fin = f.read()
        f.close()
        i0 = 0
        i1 = 0
        i2 = 0
        while(i2 + 2 < len(fin)):
            i0 = fin.find("!", i2)
            i1 = fin.find(":", i0)
            i2 = fin.find("!", i1)

            un = fin[i0+1:i1]
            pw = fin[i1+1:i2]
            logins[un] = pw

        print("imported logins",logins)
        content_len = int(self.headers.get('Content-Length'))
        post_body = str(self.rfile.read(content_len))
        body = post_body[2:-1]
        replyString = "def reply"
        print("body:",body)
        if body[0:3] == "~un":
            print("username")
            i0 = body.find(":")
            i1 = body.find(":", i0+1)

            unIn = body[i0+1:i1]
            print("uin and lgins before new check", unIn, logins)
            if unIn in logins:
                replyString = "good"
            else:
                replyString = "good:new"

        if body[0:3] == "~pw":
            print("in password")
            i0 = body.find(":")
            i1 = body.find(":", i0+1)

            unIn = body[i0+1:i1]
            print("uparce", i0, i1, unIn)
            i0 = body.find(":", i1)
            i1 = body.find(":", i0 +1)

            pwIn = body[i0+1:i1]
            print("upwarce", i0, i1, pwIn)
            if unIn in logins:
                print("login and pwin before true check:", logins[unIn], pwIn)
                if logins[unIn] == pwIn:
                    replyString = "true"
                    self.onSucLogin(unIn)
                else:
                    replyString = "false"
            else:
                logins[unIn] = pwIn
                self.onSucLogin(unIn)
                print(logins, "added new user")

        print(activePlayers)
        for pl in activePlayers:
            for p in pl:
                if body.find(p) >= 0:
                    pl[p] = time.time()

        print("logins post parce:", logins)
        self.send_response(200)
        self.send_header('Content-type','text/html')
        self.send_header('Content-Length',len(replyString))
        self.end_headers()
        self.wfile.write(bytes(replyString, "utf-8"))
        print("reply:", replyString)


        fileOut = "!"
        for user in logins:
            fileOut = fileOut + user + ":" + logins[user] + "!"

        print("File:",fileOut)
        f = open("logins.txt", "w")
        f.write(fileOut)
        f.close()
    
port = 23675

ser = HTTPServer(('', port), server)

def startServer():
    global ser
    
    print ('Started httpserver on port ' , port)

    ser.serve_forever()

def removeOnDC():
    global activePlayers, url
    while isRunning.isRunning:
        time.sleep(3)
        for pl in activePlayers:
            for p in pl:
                if time.time() - pl[p] > 5:
                    print("remove", p)

                    payload = "~!" + name+"!action:remove:1:~"
                    headers = {'Content-Length':str(len(payload))}
                    r = requests.get(url = url, data = payload, headers = headers)

                    activePlayers.remove(pl)


try:
    monThread = threading.Thread(target = removeOnDC)
    monThread.start()

    serverThread = threading.Thread(target = startServer)
    serverThread.start()

except KeyboardInterrupt:
    print ('^C received, shutting down the web server')
    ser.shutdown()
    quit()