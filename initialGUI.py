import pygame, math

cardNumToStr = {1:"A", 2:"2", 3:"3",4:"4", 5:"5", 6:"6",7:"7", 8:"8", 9:"9",10:"10", 11:"J", 12:"Q", 13:"K"}

pygame.init()

WIDTH = 1200
HEIGHT = 800

gameDisplay = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption('Owens Game')

clock = pygame.time.Clock()

crashed = False

gameDisplay.fill((42,112,60))

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
    def __init__(self, x, y, suit, value):
        self.x = x
        self.y = y
        self.suit = suit
        self.value = value
        self.r = 20
        self.width = 90
        self.height = 120
    def draw(self):
        global gameDisplay, cardNumToStr
        x = self.x
        y = self.y
        r = self.r
        h = self.height
        w = self.width
        pi = math.pi
        lineThickness = 3

        c1 = pygame.draw.rect(surface = gameDisplay, color = (255,255,255),rect =  (x, y, w, h),width = lineThickness,  border_radius = r)
        pth = str(self.suit) + ".jpg"
        suitImg = pygame.image.load(pth)
        gameDisplay.blit(suitImg, (x + w/4.5,y + h/7))


        suitCol = (0,0,0)
        if self.suit == "h" or self.suit == "d":
            suitCol = (220,0,0)
        font = pygame.font.SysFont(None, 48)
        img = font.render(cardNumToStr[self.value], True, suitCol)
        gameDisplay.blit(img, (x + w/3,y + h - 35))


for i in range(13):
    card1 = card(91*i, 0, 'h', i+1)
    card1.draw()
for i in range(13):
    card1 = card(91*i, 120, 'd', i+1)
    card1.draw()

for i in range(13):
    card1 = card(91*i, 240, 'c', i+1)
    card1.draw()

for i in range(13):
    card1 = card(91*i, 360, 's', i+1)
    card1.draw()


while not crashed:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            crashed = True

        print(event)

    pygame.display.update()
    clock.tick(60)

pygame.quit()
quit()



