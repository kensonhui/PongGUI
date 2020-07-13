import pygame
from pygame import mixer



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
                print("Player 1 wins!")
            else:
                self.velx = -2
                print("PLayer 2 wins!")
            self.vely = 0
            self.posx = round(x_border/2)
            self.posy = round(y_border/2)
            self.angleFactor = 15
            
        
        #top and bottom wall deflection
        if self.posy - self.radius <= 0 or self.posy + self.radius >= y_border:
            self.vely *= -1

def main_menu():
    menu = True
    font = pygame.font.SysFont('Arial', 30)
    title = font.render("Truly Amazing Pong", True, (255, 255, 255), (0, 0, 0))
    titleBox = title.get_rect()
    titleBox.topleft = (x_border/ 2, y_border /2 - 50)
    startButtonText = font.render("Start!", True, (255, 255, 255), (0, 0, 0))
    startButton = startButtonText.get_rect()
    startButton.topleft = (x_border/2, y_border / 2)
    helpButtonText = font.render("How to Play", True, (255, 255, 255) , (0, 0, 0))
    helpButton = helpButtonText.get_rect()
    helpButton.topleft = (x_border/2, y_border / 2 + 30)
    #start = pygame.mixer.Sound("start.wav")
    #channel = pygame.mixer.Sound.play(start)

    
    while menu:
        mx, my = pygame.mouse.get_pos()
        display.fill((0,0,0))
        display.blit(title, titleBox)
        display.blit(startButtonText, startButton)
        display.blit(helpButtonText, helpButton)
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

        if startButton.collidepoint((mx, my)):
            font = pygame.font.SysFont('Arial', 35, True)
            startButtonText = font.render("Start!", True, (255, 255, 255), (0, 0, 0))
            if click:
                
                break
        else:
            click = False
            font = pygame.font.SysFont('Arial', 30, False)
            startButtonText = font.render("Start!", True, (255, 255, 255), (0, 0, 0))

        pygame.display.update()


pygame.mixer.init()
pygame.init()
pygame.font.init()
pygame.mixer.music.load("background1.mp3")
pygame.mixer.music.play()

x_border = 700
y_border = 400
x_margin = 10
display = pygame.display.set_mode((x_border, y_border))
pygame.display.set_caption('Coordination')
player1 = Paddle(x_border - Paddle.width - x_margin, y_border/2 - Paddle.height/2)
player2 = Paddle(0 + x_margin, y_border/2 - Paddle.height/2)
run = True
ball = Ball(round(x_border/2), round(y_border/2), 1, 0)
gameDelay = 10
angleFactor = 15
main_menu();

lineWidth = 5


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
    pygame.draw.rect(display, (255, 255, 255), (x_border/2 - lineWidth/2, 0, lineWidth, y_border), 0)
    pygame.draw.circle(display, (255, 255, 255), (int(x_border/2), int(y_border/2)), Ball.radius + 19, 6 )

    pygame.draw.circle(display, ball.color, (ball.posx, ball.posy), ball.radius, 0 )
    pygame.draw.rect(display, (0, 255, 0), (player2.x, player2.y, player2.width, player2.height))
    pygame.draw.rect(display, (255, 0, 0), (player1.x, player1.y, player1.width, player1.height))
    
    pygame.display.update()

pygame.quit()


