import pygame, sys, math, random
from random import randrange
from tkinter import *
from pygame.math import Vector2

# ----------------------------- Disclaimer -----------------------------------------
# The following code was written by:
# Name: Vasantharajan Sharmilann
# ----------------------------------------------------------------------------------

# Initialize the game
pygame.init()

# Global font declarations
font = pygame.font.SysFont('comicsans', 20, True)
font2 = pygame.font.SysFont('comicsans', 22, True)
font3 = pygame.font.SysFont('comicsans', 30, True)

# Player attributes
playerX = 0
playerY = 500
velocityX = 1
velocityY = 1

lifeForce = 100
percent_covered = 0

# Import images and sounds
playerImg = pygame.image.load("crosshair.png")
playerDeadImg = pygame.image.load("scythe.png")
bkgImg = pygame.image.load('background.jpeg')
gameBackground = pygame.image.load('gameBkg.jpeg')
win_screen = pygame.image.load('winScreen.jpeg')

bkgMusic = pygame.mixer.music.load('bkg_music.mp3')
pygame.mixer.music.play(-1)

explosionSound = pygame.mixer.Sound('explosion.wav')

# Enemy Declarations
enemyX = 100
enemyY = 100
sparxX = 0
sparxY = 400

# Velocity declarations (Speed)
e_velocityX = 0.35
e_velocityY = 0.35
sparx_velX = 0.4
sparx_velY = 0.4

enemy_color = (255, 0, 0) # Red

# Enemy sprite images
enemyImg = pygame.image.load("enemy.png")
sparxImg = pygame.image.load("sparx.png")

# Screen layout
screen = pygame.display.set_mode((520,520)) # Screen Dimensions (Not alterable by user)
player_color = (0, 0, 255) # Blue
screen_width = 520
screen_height = 520

currTrail = []

# In order to make the trail
class PlayerOne(pygame.sprite.Sprite):
    p1_movement = 0

    def __init__(self):
        super(PlayerOne, self).__init__()
        self.playerX = 5
        self.playerY = 498
        self.surf = pygame.Surface((10, 10))
        self.surf.fill((255, 0, 0))
        self.rect = self.surf.get_rect()
        self.rect.center = (self.playerX, self.playerY) # Starting pos
        self.currArea = 0
        self.totalArea = 0

        self.velocityX = 0.5
        self.velocityY = 0.5
        self.trail = []

    def update(self, pressed_keys):
        if pressed_keys[pygame.K_w]:
            self.rect.move_ip(0, -1)
        if pressed_keys[pygame.K_s]:
            self.rect.move_ip(0, 1)
        if pressed_keys[pygame.K_a]:
            self.rect.move_ip(-1, 0)
        if pressed_keys[pygame.K_d]:
            self.rect.move_ip(1, 0)

        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > 520:
            self.rect.right = 520
        if self.rect.top <= 10:
            self.rect.top = 10
        if self.rect.bottom >= 520:
            self.rect.bottom = 520

        drawOnToScreen(lifeForce, percent_covered)

        pos = self.rect.center
        if self.trail:
            if self.trail[-1] != pos:
                self.trail.append(pos)
        else:
            self.trail = [pos, pos]


# Drawing function
def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, 1, color)
    textRect = textobj.get_rect()
    textRect.topleft = (x, y)
    surface.blit(textobj, textRect)

click = False

# Initialize main menu function
def main_menu():
    while True:
        screen.fill((0,0,0))
        screen.blit(bkgImg, (0,0))
        draw_text('Main Menu', font3, (255,255,255), screen, 200, 170)

        mx, my = pygame.mouse.get_pos()

        button_1 = pygame.Rect(190, 220, 150, 30)
        button_2 = pygame.Rect(190, 280, 150, 30)

        pygame.draw.rect(screen, (255, 0, 0), button_1)
        pygame.draw.rect(screen, (255, 0, 0), button_2)
        screen.blit(font.render('START', True, (255,255,255)), (240, 229))
        screen.blit(font.render('QUIT', True, (255, 255, 255)), (245, 289))

        click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        if button_1.collidepoint((mx,my)):
            if click:
                return
        if button_2.collidepoint((mx, my)):
            if click:
                print("You have quit the game. Thanks for playing!")
                sys.exit()

        pygame.display.update()

def dead():
    pygame.mixer.music.pause()
    explosionSound.play()
    while True:
        screen.fill((194, 41, 14))
        draw_text('You have died... Please hit ESC to continue.', font2, (0, 0, 0), screen, 65, 250)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

        scythe()
        pygame.display.update()

def pause():
    while True:
        screen.fill((48,166,217))
        draw_text('You have paused the game.', font2, (0,0,0), screen, 150, 250)
        draw_text('Press ESC to continue.', font2, (0, 0, 0), screen, 170, 285)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return

        pygame.display.update()

# ------------------------------------------------------------------------------------
# Drawing characters to the screen

def player(x,y):
    # screen.blit(playerImg, (playerX, playerY))
    pygame.draw.rect(screen, player_color, pygame.Rect(playerX, playerY, 2, 2))

def qix_enemy(x,y):
    screen.blit(enemyImg, (enemyX, enemyY))
    # pygame.draw.rect(screen, enemy_color, pygame.Rect(enemyX, enemyY, 15, 15))

def sparx(x,y):
    screen.blit(sparxImg, (sparxX, sparxY))

def scythe():
    screen.blit(playerDeadImg, (230, 150))

# ------------------------------------------------------------------------------------

pygame.display.set_caption("Qix Game")

# Collision with sprites on screen
def isCollision_sparx(sparxX, sparxY, playerX, playerY):
    distance = math.sqrt((math.pow(sparxX - playerX, 2) + math.pow(sparxY - playerY, 2)))

    if distance < 27:
        return True
    else:
        return False

def isCollision(enemyX, enemyY, playerX, playerY):
    distance = math.sqrt((math.pow(enemyX - playerX, 2) + math.pow(enemyY - playerY, 2)))

    if distance < 27:
        return True
    else:
        return False

def drawOnToScreen(lifeForce, percent_covered):
    life = font.render('Life Force: ' + str(lifeForce), True, (255,255,255))
    screen.blit(life, (0, 0))

    percent_covered = font.render('Area Covered: ' + str(percent_covered) + '%', True, (255,255,255))
    screen.blit(percent_covered, (390,0))

def win():
    while True:
        screen.fill((89, 136, 212))
        draw_text('Congrats! You have covered more than 75% of the area!', font2, (0,0,0), screen, 45, 250)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

main_menu()
p = PlayerOne() # Object declaration

# Main game loop. Continue while true

running = True
while running:
    screen.fill((0, 0, 0))
    screen.blit(gameBackground, (0,0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                main_menu()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                pause()

    # Check for user input for movement (Arrow keys)
    keys = pygame.key.get_pressed()

    if keys[pygame.K_a] and playerX > velocityX:
        playerX -= velocityX
        percent_covered += (50 / (500 * 500)) * 100
    if keys[pygame.K_d] and playerX < 500:
        playerX += velocityX
        percent_covered += (50 / (500 * 500)) * 100
    if keys[pygame.K_w] and playerY > velocityX + 12:
        playerY -= velocityY
        percent_covered += (50 / (500 * 500)) * 100
    if keys[pygame.K_s] and playerY < 500:
        playerY += velocityY
        percent_covered += (50 / (500 * 500)) * 100

    if playerX <= 0:
        playerX = 0

    if percent_covered >= 75:
        win()

    # Sparx and Qix randomized movement
    enemyX += e_velocityX
    enemyY -= e_velocityY

    if enemyX >= 500 or enemyX <= 0:
        e_velocityX *= -1
    if enemyY >= 500 or enemyY <= 12:
        e_velocityY *= -1

    sparxY -= sparx_velY

    if sparxX >= 500 or sparxX <= 0:
        sparx_velX *= -1
    if sparxY >= 500 or sparxY <= 12:
        sparx_velY *= -1

    # Collision Detection
    collision = isCollision(enemyX, enemyY, playerX, playerY) # Collision with Qix
    collision2 = isCollision_sparx(sparxX, sparxY, playerX, playerY) # Collision with Sparx

    # Once collision detected, move player to random (x,y) position on the screen
    if collision:
        print("You've hit a Qix! Be careful!")
        lifeForce -= 0.5

        if lifeForce <= 0:
            dead()

    if collision2:
        print("You've hit a Sparx! Be careful!")
        lifeForce -= 0.5

        if lifeForce <= 0:
            print("You have died... Game Over!")
            dead()
        else:
            # Change direction upon collision
            sparx_velY *= -1

    pressed_keys = pygame.key.get_pressed()
    p.update(pressed_keys)
    pygame.draw.lines(screen, (255, 255, 255), False, p.trail)
    screen.blit(playerImg, p.rect)

    sparx(sparxX, sparxY)
    qix_enemy(enemyX, enemyY)
    player(playerX, playerY)

    pygame.display.flip()