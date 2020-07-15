import pygame
from pygame import mixer



class TextBox:
    def __init__(self, string, font, size, xpos, ypos):
        self.string = string
        self.font = font
        self.size = size
        self.xpos = xpos
        self.ypos = ypos
        self.create()

    def create(self):
        self.sysfont = pygame.font.SysFont(self.font, self.size)
        self.render = self.sysfont.render(self.string, True, (255, 255, 255), (0, 0, 0,))
        self.rect = self.render.get_rect()
        self.rect.topleft = (self.xpos, self.ypos)
    def hover(self):
        self.sysfont = pygame.font.SysFont('Arial', self.size + 5)
        self.render = self.sysfont.render(self.string, True, (255, 255, 255), (0, 0, 0,))

    def offhover(self):
        self.sysfont = pygame.font.SysFont('Arial', self.size)
        self.render = self.sysfont.render(self.string, True, (255, 255, 255), (0, 0, 0,))

    def update(self, score):
        self.render = self.sysfont.render(str(score), True, (255, 255, 255), (0, 0, 0,))

    def blit(self, display):
        display.blit(self.render, self.rect)

class Menu:
    def help_info():
        
        title = TextBox("How to play", "Arial", 25, x_border/2, y_border/2)
        info = TextBox("Player 1 uses the arrow keys Player 2 uses WASD", "Arial", 25, x_border/2 -200, y_border/2 + 50)
        back = TextBox("Back", "Arial", 25, 50, 50)
        click = False
        help = True

        while help:
            display.fill((0, 0, 0))
            mx, my = pygame.mouse.get_pos()
            back.blit(display)
            title.blit(display)
            info.blit(display)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        click = True
            if back.rect.collidepoint(mx, my):
                back.hover()
                if click:
                    break
            else:
                back.offhover()

            click = False
            pygame.display.update()


    def main_menu():
        menu = True
        title = TextBox("Truly Amazing Pong", "Arial", 30, x_border/ 2, y_border /2 - 50)
        start = TextBox("Start", "Arial", 30, x_border/ 2, y_border /2)
        help = TextBox("How to play", "Arial", 30, x_border/2, y_border / 2 + 50)
        settings = TextBox("Settings", "Arial", 30, x_border/2, y_border / 2 + 100)
        credits = TextBox("- A Truly Awful Game by Kenson", "Arial", 20, x_border / 2 + 200, y_border/2)

        #start = pygame.mixer.Sound("start.wav")
        #channel = pygame.mixer.Sound.play(start)
    
        while menu:
            mx, my = pygame.mouse.get_pos()
            display.fill((0,0,0))
            title.blit(display)
            start.blit(display)
            help.blit(display)
            settings.blit(display)
            credits.blit(display)
            click = False
            pygame.draw.rect(display, (255,255,255), (0, y_border / 2 - 15, x_border, 5), 0)
        
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    menu = False
                    pygame.quit()
                    exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        click = True

            if start.rect.collidepoint((mx, my)):
                start.hover()
                if click:
                    break
            else:
                start.offhover()

            if help.rect.collidepoint((mx, my)):
                help.hover()
                if click:
                    Menu.help_info()
            else:
                help.offhover()

            if settings.rect.collidepoint((mx, my)):
                settings.hover()
                if click:
                    break
            else:
                settings.offhover()

            click = False

            pygame.display.update()

class Paddle:
    width = 10
    height = 70
    vel = 5
    count = 0
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Ball:
    color = (0,0,255)
    radius = 10
    acceleration = 1
    angleFactor = 15
    maxSpeed = 10
    minAngleFactor = 10
    score1 = 0
    score2 = 0

    def __init__(self, posx, posy, velx, vely):
        self.posx = posx
        self.posy = posy
        self.velx = velx
        self.vely = vely

    def updateBall(self): ##Ball update functino
        self.posx += self.velx
        self.posy += self.vely

        # check left player collision
        if self.posx + self.radius >= player1.x and self.posx <= player1.x + player1.width:
            if self.posy + self.radius >= player1.y and self.posy - self.radius <= player1.y + player1.height:
                if self.velx > 0:
                    if self.velx < self.maxSpeed:
                        self.velx += self.acceleration
                    elif self.angleFactor > 1:
                        self.angleFactor -= 1

                    self.vely = int((self.posy - (player1.y + player1.height/2))/ self.angleFactor)
                    self.velx *= -1

        #check right player collision
        if self.posx - self.radius <= player2.x + player2.width and self.posx - self.radius >= player2.x:
            if self.posy + self.radius >= player2.y and self.posy - self.radius <= player2.y + player2.height:
                if self.velx < 0:
                    self.velx *= -1
                    if self.velx < self.maxSpeed:
                        self.velx += self.acceleration
                    elif self.angleFactor > self.minAngleFactor:
                        self.angleFactor -= 1
                    self.vely = int((self.posy - (player2.y + player2.height/2))/self.angleFactor)

        #win condition
        if self.posx + self.radius <= 0 or self.posx - self.radius >= x_border:
            if self.posx - self.radius <= 0:
                self.velx = 2
                self.score2 += 1
                scoreboard2.update(self.score1)
                print("Player 1 wins!")
            else:
                self.velx = -2
                self.score1 += 1
                scoreboard1.update(self.score1)
                print("PLayer 2 wins!")
            self.vely = 0
            self.posx = round(x_border/2)
            self.posy = round(y_border/2)
            self.angleFactor = 15
            
        
        #top and bottom wall deflection
        if self.posy - self.radius <= 0 or self.posy + self.radius >= y_border:
            self.vely *= -1


pygame.mixer.init()
pygame.init()
pygame.font.init()
pygame.mixer.music.load("background1.mp3")
pygame.mixer.music.play()

##These are game constants
x_border = 900
y_border = 400
x_margin = 10
gameDelay = 10 ##the number of ms per game tick, in other words the period of each tick in ms
angleFactor = 15 
lineWidth = 5
run = True

display = pygame.display.set_mode((x_border, y_border))
pygame.display.set_caption('Truly Amazing Pong')
player1 = Paddle(x_border - Paddle.width - x_margin, y_border/2 - Paddle.height/2)
player2 = Paddle(0 + x_margin, y_border/2 - Paddle.height/2)
ball = Ball(round(x_border/2), round(y_border/2), 1, 0)

Menu.main_menu();
scoreboard1 = TextBox(str(0), "Arial", 40, x_border/4, y_border/4)
scoreboard2 = TextBox(str(0), "Arial", 40, x_border/4 * 3, y_border/4)

while run:
    pygame.time.delay(gameDelay)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    keys = pygame.key.get_pressed()

    if keys[pygame.K_UP] and player1.y > 0:
        player1.y -= player1.vel
    if keys[pygame.K_DOWN] and player1.y < y_border - player1.height:
        player1.y += player1.vel
    
    if keys[pygame.K_w] and player2.y > 0:
        player2.y -= player2.vel
    if keys[pygame.K_s] and player2.y < y_border - player2.height:
        player2.y += player2.vel


    ball.updateBall()
    
    display.fill((0,0,0))
    border = pygame.draw.rect(display, (255, 255, 255), (x_border/2 - lineWidth/2, 0, lineWidth, y_border), 0)
    border.center=(x_border/2, y_border/2)
    pygame.draw.circle(display, (255, 255, 255), (int(x_border/2), int(y_border/2)), Ball.radius + 19, 6 )
    scoreboard1.blit(display)
    scoreboard2.blit(display)

    pygame.draw.circle(display, ball.color, (ball.posx, ball.posy), ball.radius, 0 )
    pygame.draw.rect(display, (0, 255, 0), (player2.x, player2.y, player2.width, player2.height))
    pygame.draw.rect(display, (255, 0, 0), (player1.x, player1.y, player1.width, player1.height))
    
    pygame.display.update()

pygame.quit()


