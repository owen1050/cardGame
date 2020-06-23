from http.server import BaseHTTPRequestHandler, HTTPServer
import time, threading
from random import random
from calcPokerHand import calcValue

class texasHold():
    def __init__(self):
        self.names = []
        self.chipCounts = []
        self.bets = []
        self.cards = []
        self.playersInCurrentHand = []

        self.numberOfPlayers = 0
        self.dealer = 0
        self.waitingOnPlayer = ""
        self.blind = 10
        self.readyAtPlayer = 0
        self.wholeDeck = ["H14","H2","H3","H4","H5","H6","H7","H8","H9","H10","H11","H12","H13","S14","S2","S3","S4","S5","S6","S7","S8","S9","S10","S11","S12","S13","D14","D2","D3","D4","D5","D6","D7","D8","D9","D10","D11","D12","D13","C14","C2","C3","C4","C5","C6","C7","C8","C9","C10","C11","C12","C13"]
        self.currentDeck = []
        self.callValue = 0
        self.tableCards = ["b1", "b1", "b1", "b1", "b1"]
        self.pot = 0
        self.toRemove = []
        self.sittingOut = []
        self.atEnd = True
        self.winner = ""


    def getPlayerIndex(self, name):
        if name in self.names:
            return self.names.index(name)

    def getPlayerIndexHand(self, name):
        if name in self.playersInCurrentHand:
            return self.playersInCurrentHand.index(name)

    def newPlayer(self, name, chipCounts = 1000, bet = 0, cards = ["b1","b1"]):
        if name in self.names:
            return "Name already taken"
        else:
            self.names.append(name)
            self.chipCounts.append(chipCounts)
            self.bets.append(bet)
            self.cards.append(cards)
            self.numberOfPlayers = self.numberOfPlayers + 1
            return "created player named:" + name

    def removePlayer(self, name):
        if name in self.names:
            self.toRemove.append(name)
            self.playerFolded(name)

            return "removed "+ name
        else:
            return "player not in game"

    def setChipCounts(self, name, newCount):
        if name in self.names:
            indexOfPlayer = self.names.index(name)
            self.chipCounts[indexOfPlayer] = int(newCount)
            return "set " + name + "'s chip count to " + str(newCount)
        else:
            self.newPlayer(name)
            return self.setChipCounts(name, newCount)
            
    def setBet(self, name, newBet):
        if name in self.names:
            indexOfPlayer = self.names.index(name)
            if int(newBet) > int(self.callValue):
                self.callValue = newBet
                self.readyAtPlayer = indexOfPlayer
            
            self.bets[indexOfPlayer] = int(newBet)
            return "set " + name + "'s bet to " + str(newBet)
        else:
            self.newPlayer(name)
            return self.setBet(name, newBet)

    def setCards(self, name, newCards):
        if name in self.names:
            indexOfPlayer = self.names.index(name)
            self.cards[indexOfPlayer] = newCards
            return "set " + name + "'s bet to " + str(newCards)
        else:
            self.newPlayer(name)
            return self.setCards(name, newCards)

    def getPlayerInfo(self, name):
        if name in self.names:
            pi = self.names.index(name)
            return "player" + str(pi) + ":" +game.names[pi]+ ":"+ game.cards[pi][0] + ":" + game.cards[pi][1] + ":" + str(game.chipCounts[pi]) + ":" + str(game.bets[pi]) + ":"
        else:
            self.newPlayer(name)
            return self.getPlayerInfo(name, name)

    def playerFolded(self, name):
        if name in self.playersInCurrentHand:
            oldIndex = self.getPlayerIndexHand(name)
            self.playersInCurrentHand.remove(name)
            print(self.playersInCurrentHand)

            self.setCards(name, ("e1","e1"))

            if(len(self.playersInCurrentHand) < 2):
                self.dealer = self.dealer - 1
                if(self.dealer < 0):
                    self.dealer = self.numberOfPlayers-1

                i = self.getPlayerIndex(self.playersInCurrentHand[0])
                tot = 0
                for b in self.bets:
                    tot = tot + int(b)

                self.chipCounts[i] = self.chipCounts[i] + self.pot + tot

                self.atEnd = True
                self.winner = self.playersInCurrentHand[0]


            else:
                if(self.readyAtPlayer < oldIndex):
                    pass
                else:
                    self.readyAtPlayer = self.readyAtPlayer - 1
                    if(self.readyAtPlayer < 0):
                        self.readyAtPlayer = self.readyAtPlayer + len(self.playersInCurrentHand)

            

            return "player " + name + " folded"
        else:
            return "player not in current hand"

    def startHand(self):

        if(self.numberOfPlayers > 1):
            self.atEnd = False
            self.playersInCurrentHand.clear()
            self.tableCards = ["b1", "b1", "b1", "b1", "b1"]

            for player in self.toRemove:
                pi = self.getPlayerIndex(player)
                self.names.pop(pi)
                self.chipCounts.pop(pi)
                self.bets.pop(pi)
                self.cards.pop(pi)
                self.numberOfPlayers = self.numberOfPlayers - 1

            for name in self.names:
                if name in self.sittingOut:
                    pass
                else:
                    self.playersInCurrentHand.append(name)

            self.dealCards()

            sb = self.dealer - 1
            bb = self.dealer - 2
            fb = self.dealer - 3
            
            pih = len(self.playersInCurrentHand)
            if sb < 0:
                sb = pih + sb
            while bb < 0:
                bb = pih + bb
            while fb < 0:
                fb = pih + fb

            self.readyAtPlayer = bb - 1
            while self.readyAtPlayer < 0:
                self.readyAtPlayer = self.readyAtPlayer + pih

            self.pot = self.blind//2 + self.blind
            self.callValue = self.blind
            self.setBet(self.playersInCurrentHand[sb], self.blind//2)
            self.chipCounts[sb] = self.chipCounts[sb] - self.blind//2

            self.setBet(self.playersInCurrentHand[bb], self.blind)
            self.chipCounts[bb] = self.chipCounts[bb] - self.blind

            self.waitingOnPlayer = self.playersInCurrentHand[fb]
            

            return "PICH:" + str(self.playersInCurrentHand)
        return "not enough players to start game"

    def dealCards(self):
        self.currentDeck = self.wholeDeck.copy()
        tcards = []
        for hands in self.cards:
            th = []
            r1 = int(random() * len(self.currentDeck))
            th.append(self.currentDeck.pop(r1))
            r2 = int(random() * len(self.currentDeck))
            th.append(self.currentDeck.pop(r2))
            tcards.append(th)
        self.cards = tcards

    def flop(self):
        r1 = int(random() * len(self.currentDeck))
        self.tableCards[0] = self.currentDeck.pop(r1)
        r2 = int(random() * len(self.currentDeck))
        self.tableCards[1] = self.currentDeck.pop(r2)
        r3 = int(random() * len(self.currentDeck))        
        self.tableCards[2] = self.currentDeck.pop(r3)

        pot = 0
        for i in range(len(self.bets)):
            pot = pot + self.bets[i]
            self.bets[i] = 0
        self.pot = pot
        self.callValue = 0

    def turn(self):
        r1 = int(random() * len(self.currentDeck))
        self.tableCards[3] = self.currentDeck.pop(r1)

        pot = 0
        for i in range(len(self.bets)):
            pot = pot + self.bets[i]
            self.bets[i] = 0
        self.pot = self.pot + pot
        self.callValue = 0

    def river(self):
        r1 = int(random() * len(self.currentDeck))
        self.tableCards[4] = self.currentDeck.pop(r1)

        pot = 0
        for i in range(len(self.bets)):
            pot = pot + self.bets[i]
            self.bets[i] = 0
        self.pot = self.pot + pot
        self.callValue = 0

    def evalWinnerAndReset(self):
        #need to eval winner and give chips at some point
        hands = {}
        for p in self.playersInCurrentHand:
            i = self.getPlayerIndex(p)
            hands[p] = self.cards[i]
        print(hands)
        for h in hands:
            for t in self.tableCards:
                
                hands[h].append(t)
        print(hands)
        maxScore = 0
        winningPlayer = ""
        winningHand = ""
        for h in hands:
            score, winningHand = calcValue(hands[h])
            if score > maxScore:
                maxScore = score
                winningPlayer = h

            print(h, score)

        print(maxScore)

        self.dealer = self.dealer - 1
        if(self.dealer < 0):
            self.dealer = self.numberOfPlayers-1

        i = self.getPlayerIndex(winningPlayer)
        self.chipCounts[i] = self.chipCounts[i] + self.pot

        self.atEnd = True
        self.winner = winningPlayer
        self.waitingOnPlayer = ""

    def startHandDelay(self):
        time.sleep(10)
        self.startHand()


    def advanceWaiting(self):
        ind = self.getPlayerIndexHand(self.waitingOnPlayer)
        if ind - 1 >= 0:
            self.waitingOnPlayer = self.playersInCurrentHand[ind-1]
        else:
            self.waitingOnPlayer = self.playersInCurrentHand[len(self.playersInCurrentHand) - 1]


        ind = self.getPlayerIndexHand(self.waitingOnPlayer)
        print(self.waitingOnPlayer, ind, self.readyAtPlayer)

        if ind == self.readyAtPlayer:
            if self.tableCards[0] == "b1":
                self.flop()
            elif self.tableCards[3] == "b1":
                self.turn()
            elif self.tableCards[4] == "b1":
                self.river()
            else:
                self.evalWinnerAndReset()


class server(BaseHTTPRequestHandler):
    
    def log_message(self, format, *args):
        return

    def do_GET(self):
        global game
        
        content_len = int(self.headers.get('Content-Length'))
        post_body = str(self.rfile.read(content_len))
        body = post_body[2:-1]
        #print("body:" + body)
        replyString = ""
        
        if body.find("~update") >= 0:
            replyString = replyString + "~!" + str(game.numberOfPlayers)+ "!"

            for player in game.names:
                replyString = replyString + game.getPlayerInfo(player)
            replyString = replyString + "PICH:"
            for player in game.playersInCurrentHand:
                replyString = replyString + str(player) + ":"

            replyString = replyString + "WAITINGON[" + game.waitingOnPlayer+"]"
            replyString = replyString + "CALL[" + str(game.callValue)+"]"
            replyString = replyString + "BLIND[" + str(game.blind)+"]"
            replyString = replyString + "TABLE[" + str(game.tableCards)+"]"
            replyString = replyString + "POT[" + str(game.pot)+"]"
            if(game.atEnd):
                replyString = replyString + "WINNER["+ game.winner + "]"


            replyString = replyString + "~"
        else:
            i0 = body.find("!") + 1
            i1 = body.find("!", i0)
            playerName = body[i0:i1]
            print("Name:" + playerName)

            if playerName in game.names:
                
                i0 = body.find(":") + 1
                i1 = body.find(":", i0)

                actionStr = body[i0:i1]
                print(actionStr)
                i0 = body.find(":", i1) + 1
                i1 = body.find(":", i0)

                valueStr= body[i0:i1]
                print(valueStr)

                if actionStr == "bet" and game.atEnd == False:
                    if int(valueStr) == int(game.callValue) or int(valueStr) >= int(game.callValue) + int(game.blind):
                        
                        if playerName == game.waitingOnPlayer:
                            game.setChipCounts(playerName, game.chipCounts[game.getPlayerIndex(playerName)] -(int(valueStr) - game.bets[game.getPlayerIndex(playerName)]))
                            replyString = game.setBet(playerName, valueStr)
                            game.advanceWaiting()

                if actionStr == "fold":
                    if playerName == game.waitingOnPlayer:
                        game.advanceWaiting()
                    replyString = game.playerFolded(playerName)
                    

                if actionStr == "setChips":
                    replyString = game.setChipCounts(playerName, valueStr)

                if actionStr == "setCards":
                    i0 = valueStr.find(",")
                    card1 = valueStr[:i0]
                    card2 = valueStr[i0+1:]
                    replyString = game.setCards(playerName, (card1, card2))

                if actionStr == "startHand":
                    if(game.atEnd):
                        replyString = game.startHand()

                if actionStr == "remove":
                    replyString = game.removePlayer(playerName)


            else:
                if game.numberOfPlayers < 8:
                    replyString = game.newPlayer(playerName)
                else:
                    replyString = "sorry the game is full"
        
        if(replyString == ""):
            replyString = "Error, no action based off body"

        self.send_response(200)
        self.send_header('Content-type','text/html')
        self.send_header('Content-Length',len(replyString))
        self.end_headers()
        self.wfile.write(bytes(replyString, "utf-8"))
        #print("reply:" + replyString)


port = 23666

game = texasHold()

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
