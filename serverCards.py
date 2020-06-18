from http.server import BaseHTTPRequestHandler, HTTPServer
import time, threading

port = 23663

numberOfPlayers = 0

names = []
chipCounts = []
bets = []
cards = []

class server(BaseHTTPRequestHandler):
    
    def log_message(self, format, *args):
        return

    def do_GET(self):
        global numberOfPlayers, names, chipCounts, bets, cards
        content_len = int(self.headers.get('Content-Length'))
        post_body = str(self.rfile.read(content_len))
        body = post_body[2:-1]
        print("body:" + body)
        replyString = ""
        
        if body.find("~update") >= 0:
            replyString = replyString + "~!" + str(numberOfPlayers)+ "!"

            for pi in range(numberOfPlayers):
                replyString = replyString + "player" + str(pi+1) + ":" +names[pi]+ ":"+ cards[pi][0] + ":" + cards[pi][1] + ":" + str(chipCounts[pi]) + ":" + str(bets[pi]) + ":"
            replyString = replyString + "~"
        else:
            i0 = body.find("!") + 1
            i1 = body.find("!", i0)
            playerName = body[i0:i1]
            print("Name:" + playerName)
            if playerName in names:
                pi = names.index(playerName)

                i0 = body.find(":") + 1
                i1 = body.find(":", i0)

                actionStr = body[i0:i1]
                print("Action:" + actionStr)

                i0 = body.find(":", i1) + 1
                i1 = body.find(":", i0)

                actionStr2 = body[i0:i1]
                print("Value:" + actionStr2)

                replyString = "ran action"
            else:
                if numberOfPlayers + 1 <= 8:
                    numberOfPlayers = numberOfPlayers + 1
                    names.append(playerName)
                    chipCounts.append(0)
                    bets.append(0)
                    cards.append(["0", "0"])
                    replyString = "Added player " + playerName
                else:
                    replyString = "sorry the game is full"
        



        if(replyString == ""):
            replyString = "Error, no action based off body"

        self.send_response(200)
        self.send_header('Content-type','text/html')
        self.send_header('Content-Length',len(replyString))
        self.end_headers()
        self.wfile.write(bytes(replyString, "utf-8"))
        print("reply:" + replyString)

ser = HTTPServer(('', port), server)

def startServer():
    global ser
    
    print ('Started httpserver on port ' , port)

    ser.serve_forever()

try:
    serverThread = threading.Thread(target = startServer)
    serverThread.start()

except KeyboardInterrupt:
    print ('^C received, shutting down the web server')
    ser.shutdown()
    quit()
