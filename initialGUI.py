import pygame, math, time, requests

uname = input("Username:")
pw = input("password:")
print(uname, pw)

url = 'http://192.168.1.229:23664'

t0 = time.time()

cardNumToStr = {1:"A", 2:"2", 3:"3",4:"4", 5:"5", 6:"6",7:"7", 8:"8", 9:"9",10:"10", 11:"J", 12:"Q", 13:"K"}

pygame.init()

WIDTH = 1250
HEIGHT = 800

gameDisplay = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("8 Player Texas Hold\'em")

font48 = pygame.font.SysFont(None, 48)
font30 = pygame.font.SysFont(None, 30)

clock = pygame.time.Clock()

crashed = False

gameDisplay.fill((42,112,60))

print("init time:" + str(time.time()-t0))


class card():
    def __init__(self, x, y, suit, value, rotate):
        self.x = x
        self.y = y
        self.suit = suit
        self.value = value
        self.r = 20
        self.width = 90
        self.height = 127
        self.rotate = rotate

    def draw(self):
        global gameDisplay, cardNumToStr, font
        x = self.x
        y = self.y
        r = self.r
        h = self.height
        w = self.width

        pi = math.pi
        lineThickness = 2
        
        if self.rotate:
            c1 = pygame.draw.rect(surface = gameDisplay, color = (255,255,255),rect =  (x, y, h, w),width = lineThickness,  border_radius = 0)
        else:
            c1 = pygame.draw.rect(surface = gameDisplay, color = (255,255,255),rect =  (x, y, w, h),width = lineThickness,  border_radius = 0)
        gameDisplay.fill((255,255,255), c1)
        
        
        if self.suit != "b":
            pth = str(self.suit) + ".jpg"
            suitImg = pygame.image.load(pth)

            gameDisplay.blit(suitImg, (x + w/4.5,y + h/7))

            suitCol = (0,0,0)
            if self.suit == "h" or self.suit == "d":
                suitCol = (220,0,0)
            
            img = font48.render(cardNumToStr[self.value], True, suitCol)
            if self.rotate:
                gameDisplay.blit(img, (x + h/1.5,y + w/3))
            else:
                gameDisplay.blit(img, (x + w/2.6,y + h - 35))
        else:
            pth = "b.png"
            suitImg = pygame.image.load(pth)
            if self.rotate:
                suitImg = pygame.transform.rotate(suitImg, 90)
            gameDisplay.blit(suitImg, (x ,y))
        

    def setSuit(self, suit):
        self.suit = suit

    def setValue(self, value):
        self.value = value

    def setX(self, x):
        self.x = x

    def setY(self, y):
        self.y = y

class button():

    def __init__(self, x, y, w, h, color, text, textColor, textVert = False):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.color = color
        self.text = text
        self.textColor = textColor
        self.textVert = textVert


    def draw(self):
        global gameDisplay
        c1 = pygame.draw.rect(surface = gameDisplay, color = self.color,rect =  (self.x, self.y, self.w, self.h),width = 0,  border_radius = 0)
        img = font30.render(self.text, True, self.textColor)
        textSize = img.get_rect().size
        gameDisplay.blit(img, (self.x + self.w/2 - textSize[0]/2, self.y + self.h/2 - textSize[1]/2))

    def isClicked(self, coord):
        x = coord[0]
        y = coord[1]
        if self.x < x < self.x + self.w and self.y < y < self.y + self.h:
            return True
        return False

    def setText(self, text):
        self.text = str(text)

class texasHold():
    def __init__(self):
        self.names = []
        self.chipCounts = []
        self.bets = []
        self.cards = []
        self.playersInCurrentHand = []

        self.numberOfPlayers = 0


    def getChipCount(self, name):
        if name in self.names:
            indexOfPlayer = self.names.index(name)
            return self.chipCounts[indexOfPlayer]

    def getBet(self, name):
        if name in self.names:
            indexOfPlayer = self.names.index(name)
            return self.bets[indexOfPlayer]

    def getCards(self, name):
        if name in self.names:
            indexOfPlayer = self.names.index(name)
            return self.cards[indexOfPlayer]

    def newPlayer(self, name, chipCounts = 0, bet = 0, cards = ["0","0"]):
        if name in self.names:
            return "Name already taken"
        else:
            self.names.append(name)
            self.chipCounts.append(chipCounts)
            self.bets.append(bet)
            self.cards.append(cards)
            self.numberOfPlayers = self.numberOfPlayers + 1
            return "created player named:" + name

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
            return "player" + str(pi+1) + ":" +game.names[pi]+ ":"+ game.cards[pi][0] + ":" + game.cards[pi][1] + ":" + str(game.chipCounts[pi]) + ":" + str(game.bets[pi]) + ":"
        else:
            self.newPlayer(name)
            return self.getPlayerInfo(name, name)

    def playerFolded(self, name):
        if name in self.playersInCurrentHand:
            self.playersInCurrentHand.remove(name)
            return "player " + name + " folded"
        else:
            return "player not in current hand"

    def updateDatabase(self, update):
        i0 = 0
        i1 = update.find(":", i0)

        name = update[i0:i1]

        i0 = update.find(":", i1) + 1
        i1 = update.find(":", i0)

        card1 = update[i0:i1]

        i0 = update.find(":", i1) + 1
        i1 = update.find(":", i0)

        card2 = update[i0:i1]

        i0 = update.find(":", i1) + 1
        i1 = update.find(":", i0)

        chips = update[i0:i1]

        i0 = update.find(":", i1) + 1
        i1 = update.find(":", i0)

        bet = update[i0:i1]

        self.setCards(name, (card1, card2))
        self.setChipCounts(name, chips)
        self.setBet(name, bet)

        return "updated database", name, card1, card2, chips, bet


t0 = time.time()
offset = 160
checkButton = button(offset + 15,740 , 100,50, (255,255,255), "check", (0,0,0))
foldButton = button(offset + 130,740 , 100,50, (255,255,255), "fold", (0,0,0))
sub10Bet = button(offset + 280,740 , 70,50, (255,255,255), "-10x", (0,0,0))
sub1Bet = button(offset + 355,740 , 70,50, (255,255,255), "-1x", (0,0,0))
add10Bet = button(offset + 580,740 , 70,50, (255,255,255), "+10x", (0,0,0))
add1Bet = button(offset + 505,740 , 70,50, (255,255,255), "+1x", (0,0,0))
betAmount = button(offset + 430,740 , 70,50, (255,255,255), "0", (0,0,0))
callButton = button(offset + 700,740 , 100,50, (255,255,255), "Call", (0,0,0))
allInButton = button(offset + 815,740 , 100,50, (240,0,0), "ALL IN", (0,0,0))

userCard1 = card(530,600, "s", 1, False)
userCard2 = card(630,600, "h", 1, False)

op1Card1 = card(530,45, "b", 1, False)
op1Card2 = card(630,45, "b", 1, False)
op1BetButton = button(575,215 , 100,35, (255,255,255), "op1Bet", (0,0,0))
op1ChipsButton = button(575,175 , 100,35, (255,255,255), "op1Chips", (0,0,0))
op1Name = button(575,5 , 100,35, (255,255,255), "op1Name", (0,0,0))

offset = -460
op2Card1 = card(offset + 530,45, "b", 1, False)
op2Card2 = card(offset + 630,45, "b", 1, False)
op2BetButton = button(offset + 575,215 , 100,35, (255,255,255), "op2Bet", (0,0,0))
op2ChipsButton = button(offset + 575,175 , 100,35, (255,255,255), "op2Chips", (0,0,0))
op2Name = button(offset + 575,5 , 100,35, (255,255,255), "op2Name", (0,0,0))

offset = 460
op3Card1 = card(offset + 530,45, "b", 1, False)
op3Card2 = card(offset + 630,45, "b", 1, False)
op3BetButton = button(offset + 575,215 , 100,35, (255,255,255), "op3Bet", (0,0,0))
op3ChipsButton = button(offset + 575,175 , 100,35, (255,255,255), "op3Chips", (0,0,0))
op3Name = button(offset + 575,5 , 100,35, (255,255,255), "op3Name", (0,0,0))

offset = -230
op4Card1 = card(offset + 530,45, "b", 1, False)
op4Card2 = card(offset + 630,45, "b", 1, False)
op4BetButton = button(offset + 575,215 , 100,35, (255,255,255), "op4Bet", (0,0,0))
op4ChipsButton = button(offset + 575,175 , 100,35, (255,255,255), "op4Chips", (0,0,0))
op4Name = button(offset + 575,5 , 100,35, (255,255,255), "op4Name", (0,0,0))

offset = 230
op5Card1 = card(offset + 530,45, "b", 1, False)
op5Card2 = card(offset + 630,45, "b", 1, False)
op5BetButton = button(offset + 575,215 , 100,35, (255,255,255), "op5Bet", (0,0,0))
op5ChipsButton = button(offset + 575,175 , 100,35, (255,255,255), "op5Chips", (0,0,0))
op5Name = button(offset + 575,5 , 100,35, (255,255,255), "op5Name", (0,0,0))

op6Card1 = card(5,350, "b", 1, True)
op6Card2 = card(5,450, "b", 1, True)
op6BetButton = button(140,450 , 100,35, (255,255,255), "op6Bet", (0,0,0))
op6ChipsButton = button(140,410 , 100,35, (255,255,255), "op6Chips", (0,0,0))
op6Name = button(20,310 , 100,35, (255,255,255), "op6Name", (0,0,0))

op7Card1 = card(1245-127,350, "b", 1, True)
op7Card2 = card(1245-127,450, "b", 1, True)
op7BetButton = button(1250-240,450 , 100,35, (255,255,255), "op7Bet", (0,0,0))
op7ChipsButton = button(1250-240,410 , 100,35, (255,255,255), "op7Chips", (0,0,0))
op7Name = button(1250-120,310 , 100,35, (255,255,255), "op7Name", (0,0,0))

offset = 380
dist = 100
yTab = 375
tabCard1= card(offset + 0* dist,yTab, "b", 1, False)
tabCard2= card(offset + 1* dist,yTab, "b", 1, False)
tabCard3= card(offset + 2* dist,yTab, "b", 1, False)
tabCard4= card(offset + 3* dist,yTab, "b", 1, False)
tabCard5= card(offset + 4* dist,yTab, "b", 1, False)

potButton = button(575,315 , 100,35, (255,255,255), "TotalPot", (0,0,0))
playerBet = button(575,550 , 100,35, (255,255,255), "PlayerBet", (0,0,0))
playerChips = button(750,675 , 120,35, (255,255,255), "Chips", (0,0,0))

tabCards = [tabCard1, tabCard2, tabCard3, tabCard4, tabCard5]

userCards = [userCard1, userCard2]
op1Cards = [op1Card1, op1Card2]
op2Cards = [op2Card1, op2Card2]
op3Cards = [op3Card1, op3Card2]
op4Cards = [op4Card1, op4Card2]
op5Cards = [op5Card1, op5Card2]
op6Cards = [op6Card1, op6Card2]
op7Cards = [op7Card1, op7Card2]

cards = [tabCards, userCards, op1Cards, op2Cards, op3Cards, op4Cards, op5Cards, op6Cards, op7Cards]

interfaceButtons = [checkButton, foldButton, sub1Bet, sub10Bet, add1Bet, add10Bet, betAmount, allInButton, callButton,potButton, playerBet, playerChips]

op1Buttons = [op1BetButton, op1ChipsButton, op1Name]
op2Buttons = [op2BetButton, op2ChipsButton, op2Name]
op3Buttons = [op3BetButton, op3ChipsButton, op3Name]
op4Buttons = [op4BetButton, op4ChipsButton, op4Name]
op5Buttons = [op5BetButton, op5ChipsButton, op5Name]
op6Buttons = [op6BetButton, op6ChipsButton, op6Name]
op7Buttons = [op7BetButton, op7ChipsButton, op7Name]

buttons = [interfaceButtons, op1Buttons, op2Buttons, op3Buttons, op4Buttons, op5Buttons, op6Buttons, op7Buttons]

prevClick = False

numPlayers = 1

payload = "~!" + uname+ "!~"
headers = {'Content-Length':str(len(payload))}

r = requests.get(url, data = payload, headers = headers)

game = texasHold()

while not crashed:
    gameDisplay.fill((42,112,60))

    payload = "~update~"
    headers = {'Content-Length':str(len(payload))}

    r = requests.get(url, data = payload, headers = headers)
    update = r.text
    i0 = update.find("!") + 1
    i1 = update.find("!", i0)
    numPlayers = int(update[i0:i1])

    while update.find("player", i1) > 0:
        i0 = update.find("player", i1)
        i0 = update.find(":", i0)+1
        i1 = update.find("player", i0)

        print(game.updateDatabase(update[i0:i1]))



    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            crashed = True
        #print(event)

    
    i = 0
    p = 1
    while i < numPlayers:
        for button in buttons[i]:
            button.draw()
        
        if game.names[i] == uname:
            p = 0
            buttons[0][10].setText(game.getBet(uname))
            buttons[0][11].setText(game.getChipCount(uname))
        else:
            buttons[i+p][2].setText(game.names[i])
            buttons[i+p][1].setText(game.getChipCount(game.names[i]))
            buttons[i+p][0].setText(game.getBet(game.names[i]))

        i = i + 1

    i = 0
    while i < numPlayers+1:
        for card in cards[i]:
            card.draw() 
        i = i + 1

    delta = time.time() - t0
    #print(delta)

    mouse = pygame.mouse.get_pos() #mouse is a touple, 0 is x 1 is y
    click = pygame.mouse.get_pressed() #click is touple, 0 is left, 1 is middle, 2 is right click
    #print(mouse)
    if prevClick == 1 and click[0] == 0:
        for buttonLists in buttons:
            for button in buttonLists:
                if button.isClicked(mouse):
                    print(button.text)

                    if button.text == "-10x":
                        buttons[0][6].setText(str(int(buttons[0][6].text) - 10))
                    if button.text == "-1x":
                        buttons[0][6].setText(str(int(buttons[0][6].text) - 1))
                    if button.text == "+10x":
                        buttons[0][6].setText(str(int(buttons[0][6].text) + 10))
                    if button.text == "+1x":
                        buttons[0][6].setText(str(int(buttons[0][6].text) + 1))

                    if int(buttons[0][6].text) < 0:
                        buttons[0][6].setText("0")
    prevClick = click[0]
    
    pygame.display.update()
    clock.tick(30)

pygame.quit()
quit()
