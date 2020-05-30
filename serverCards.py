from http.server import BaseHTTPRequestHandler, HTTPServer
import time, threading

port = 23659
"""
playerList = ["owen", "ben"]
pingTime = {"owen" : 0, "ben" : 0}
hands = {"owen" : "<AS><JD><8H>", "ben" : "<JD><8H>"}
table = ["AC", "10S"]
bets = {"owen" : 0, "ben" : 10}
turn = "owen"
"""

playerList = []
pingTime = {}
hands = {}
table = []
bets = {}
turn = ""

class server(BaseHTTPRequestHandler):

    def do_GET(self):
        global playerList, table, bets, hands, turn, pingTime
        content_len = int(self.headers.get('Content-Length'))
        post_body = str(self.rfile.read(content_len))
        body = post_body[2:]
        print(body)
        replyString = ""
        try:
            if(body[0:11] == "~newPlayer:"):
                i0 = 11
                i1 = body.find(":", i0)
                newPlayerName = body[i0:i1]
                playerList.append(newPlayerName)
                pingTime[newPlayerName] = time.time()
                hands[newPlayerName]= ""
                bets[newPlayerName] = 0
                outString = "New player:" + newPlayerName
                if(replyString == ""):
                    replyString = outString
                else:
                    replyString = replyString + ":" + outString
        except:
            print("error in new player")

        try:
            if(body[0:7] == "~update"):

                outString = "~players:"
                for player in playerList:
                    outString = outString + str(player) +":"
                outString = outString + "/table:"

                for card in table:
                    outString = outString + str(card) +":"
                outString = outString + "/hands:"

                for playerName in hands:
                    outString = outString + playerName + "-" + str(hands[playerName]) +":"
                outString = outString + "/bets:"
                
                for playerName in bets:
                    outString = outString + playerName + "-" + str(bets[playerName]) +":"
                outString = outString + "/turn:"

                outString = outString + turn + ":/"

                i0 = 7
                i1 = body.find(":", i0)
                playerName = body[i0:i1]
                pingTime[playerName] = time.time()

                if(replyString == ""):
                    replyString = outString
                else:
                    replyString = replyString + ":" + outString
        except:
            print("error update")


        if(replyString == ""):
            replyString = "Error, no match"

        self.send_response(200)
        self.send_header('Content-type','text/html')
        self.send_header('Content-Length',len(replyString))
        self.end_headers()
        self.wfile.write(bytes(replyString, "utf-8"))
        print(replyString)

def startServer():
    # Create a web server and define the handler to manage the
    # incoming request
    ser = HTTPServer(('', port), server)
    print ('Started httpserver on port ' , port)

    # Wait forever for incoming http requests
    ser.serve_forever()

def disconectTest():
    global playerList, table, bets, hands, turn, pingTime
    while(True):
        time.sleep(0.05)
        try:
            for player in pingTime:
                if(pingTime[player] + 5 < time.time()):
                    playerList.remove(player)
                    bets.pop(player)
                    hands.pop(player)
                    pingTime.pop(player)
                    print(player + " timed out from the game")
        except:
            print("error in test game")

try:
    serverThread = threading.Thread(target = startServer)
    serverThread.start()

    dcThread = threading.Thread(target = disconectTest)
    dcThread.start()

except KeyboardInterrupt:
    print ('^C received, shutting down the web server')
    server.socket.close()
