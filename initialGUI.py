import pygame, math, time

t0 = time.time()

cardNumToStr = {1:"A", 2:"2", 3:"3",4:"4", 5:"5", 6:"6",7:"7", 8:"8", 9:"9",10:"10", 11:"J", 12:"Q", 13:"K"}

pygame.init()

WIDTH = 1250
HEIGHT = 800

gameDisplay = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption('Owens Game')

font48 = pygame.font.SysFont(None, 48)
font30 = pygame.font.SysFont(None, 30)

clock = pygame.time.Clock()

crashed = False

gameDisplay.fill((42,112,60))

print("init time:" + str(time.time()-t0))

class ball():
    def __init__(self, x, y, vx, vy, r):
        global WIDTH, HEIGHT
        self.x = x
        self.y = y
        self. vx = vx
        self.vy = vy
        self. r = r
        self.prevGroundCount = 0
    def draw(self):
        global gameDisplay
        pygame.draw.circle(gameDisplay, (0,255,255), (self.x, self.y), self.r, 3)
    def clear(self):
        global gameDisplay
        pygame.draw.circle(gameDisplay, (0,0,0), (self.x, self.y), self.r, 3)
    def update(self):
        global gameDisplay, WIDTH, HEIGHT
        self.clear()
        wallF = 0.93

        self.vy = self.vy + 1
        self.y = self.y + self.vy

        self.x = self.x + self.vx
        if self.x + self.r > WIDTH:
            self.x = WIDTH - self.r
            self.vx = self.vx * -wallF
        if self.x < self.r:
            self.x = self.r
            self.vx = self.vx * -wallF

        if self.y + self.r > HEIGHT:
            self.y = HEIGHT - self.r
            self.vy = self.vy * -wallF

        if self.y < self.r:
            self.y = self.r
            self.vy = self.vy * -wallF

        if self.prevGroundCount > 3 and  self.y == HEIGHT - self.r:
            self.vx = self.vx * 0.99

        if self.y == HEIGHT - self.r:
            self.prevGroundCount = self.prevGroundCount + 1
        else:
            self.prevGroundCount = 0


        self.draw()

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

    def __init__(self, x, y, w, h, color, text, textColor):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.color = color
        self.text = text
        self.textColor = textColor

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
        self.text = text

t0 = time.time()
offset = 100
checkButton = button(offset + 15,740 , 100,50, (255,255,255), "check", (0,0,0))
foldButton = button(offset + 130,740 , 100,50, (255,255,255), "fold", (0,0,0))
sub10Bet = button(offset + 280,740 , 70,50, (255,255,255), "-10x", (0,0,0))
sub1Bet = button(offset + 355,740 , 70,50, (255,255,255), "-1x", (0,0,0))
add10Bet = button(offset + 580,740 , 70,50, (255,255,255), "+10x", (0,0,0))
add1Bet = button(offset + 505,740 , 70,50, (255,255,255), "+1x", (0,0,0))
betAmount = button(offset + 430,740 , 70,50, (255,255,255), "0", (0,0,0))
callButton = button(offset + 700,740 , 100,50, (255,255,255), "Call", (0,0,0))
allInButton = button(offset + 815,740 , 100,50, (240,0,0), "ALL IN", (0,0,0))

buttons = [checkButton, foldButton, sub1Bet, sub10Bet, add1Bet, add10Bet, betAmount, allInButton, callButton]

testCard = card(50,50, "h", 2, False)


prevClick = False

while not crashed:

    gameDisplay.fill((42,112,60))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            crashed = True
        #print(event)

    for button in buttons:
        button.draw()

    delta = time.time() - t0
    #print(delta)

    testCard.draw()

    mouse = pygame.mouse.get_pos() #mouse is a touple, 0 is x 1 is y
    click = pygame.mouse.get_pressed() #click is touple, 0 is left, 1 is middle, 2 is right click

    if prevClick == 1 and click[0] == 0:
        for button in buttons:
            if button.isClicked(mouse):
                print(button.text)

                if button.text == "-10x":
                    buttons[6].setText(str(int(buttons[6].text) - 10))
                if button.text == "-1x":
                    buttons[6].setText(str(int(buttons[6].text) - 1))
                if button.text == "+10x":
                    buttons[6].setText(str(int(buttons[6].text) + 10))
                if button.text == "+1x":
                    buttons[6].setText(str(int(buttons[6].text) + 1))

                if int(buttons[6].text) < 0:
                    buttons[6].setText("0")
    prevClick = click[0]
    
    pygame.display.update()
    clock.tick(60)

pygame.quit()
quit()
