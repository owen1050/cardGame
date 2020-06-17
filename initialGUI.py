import pygame, math

pygame.init()

WIDTH = 1200
HEIGHT = 800

gameDisplay = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption('Owens Game')

clock = pygame.time.Clock()

crashed = False

gameDisplay.fill((0,0,0))

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
        global gameDisplay
        x = self.x
        y = self.y
        r = self.r
        h = self.height
        w = self.width
        pi = math.pi
        lineThickness = 3

        c1 = pygame.draw.rect(surface = gameDisplay, color = (255,255,255),rect =  (x, y, w, h),width = lineThickness,  border_radius = r)
        
        
        font = pygame.font.SysFont(None, 48)
        img = font.render("Test", True, (255,0,0))
        gameDisplay.blit(img, (250,400))


card1 = card(50,50, "H", 13)
card1.draw()

card1 = card(200,50, "H", 13)
card1.draw()

card1 = card(350,50, "H", 13)
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



