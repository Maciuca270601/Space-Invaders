import math
import random
import sys
import os
from sys import exit
import time
import shelve

import pygame
from pygame import mixer

# Intialize the pygame
pygame.init()

# create the screen
screen = pygame.display.set_mode((800, 600))

# Background
background = pygame.transform.scale(pygame.image.load(os.path.join('background.png')), (800, 600))
#background = pygame.image.load('background.png')

# Sound
mixer.music.load("background.wav")
mixer.music.play(-1)

# Caption and Icon
pygame.display.set_caption("Space Invader")
icon = pygame.image.load('enemy3_2.png')
pygame.display.set_icon(icon)

# Player
playerImg = pygame.transform.scale(pygame.image.load(os.path.join('spaceship.png')), (80, 60))
playerX = 370
playerY = 480
playerX_change = 0



# Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 25

# Bunker
bunkerImg = []
bunkerX = []
bunkerY = []
num_of_bunkers = 5

for i in range(0, 5):
    bunkerImg.append(pygame.transform.scale(pygame.image.load(os.path.join('bunker.png')), (80, 40)))
    bunkerX.append(50 + 150 * i)
    bunkerY.append(440)

for i in range(0, 5):
    enemyImg.append(pygame.transform.scale(pygame.image.load(os.path.join('enemy1_1.png')), (40, 30)))
    enemyX.append(120 * i)
    enemyY.append(50)
    enemyX_change.append(2)
    enemyY_change.append(15)

for i in range(5, 10):
    enemyImg.append(pygame.transform.scale(pygame.image.load(os.path.join('enemy2_1.png')), (40, 30)))
    enemyX.append(120 * i - 600)
    enemyY.append(100)
    enemyX_change.append(2)
    enemyY_change.append(15)

for i in range(10, 15):
    enemyImg.append(pygame.transform.scale(pygame.image.load(os.path.join('enemy3_1.png')), (40, 30)))
    enemyX.append(120 * i - 1200)
    enemyY.append(150)
    enemyX_change.append(2)
    enemyY_change.append(15)

for i in range(15, 20):
    enemyImg.append(pygame.transform.scale(pygame.image.load(os.path.join('enemy1_2.png')), (40, 30)))
    enemyX.append(120 * i - 1800)
    enemyY.append(200)
    enemyX_change.append(2)
    enemyY_change.append(15)

for i in range(20, 25):
    enemyImg.append(pygame.transform.scale(pygame.image.load(os.path.join('enemy2_2.png')), (40, 30)))
    enemyX.append(120 * i - 2400)
    enemyY.append(250)
    enemyX_change.append(2)
    enemyY_change.append(15)
# Bullet

# Ready - You can't see the bullet on the screen
# Fire - The bullet is currently moving

bulletImg = pygame.image.load('laser.png')
laserImg = pygame.image.load('enemylaser.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 10
bullet_state = "ready"

laserY = []
laserX = []
laser_state = []
for i in range(0, 5):
    laserX.append(250)
for i in range(0, 5):
    laserY.append(0)
for i in range(0, 5):
    laser_state.append("ready")

laserX_change = 0
laserY_change = 2

# Score

score_value = 0
font = pygame.font.Font('space_invaders.ttf', 32)



textX = 10
textY = 10

text2X = 500
text2Y = 10

# Game Over
over_font = pygame.font.Font('space_invaders.ttf', 64)


def show_score(x, y):
    score = font.render("Score : " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))

#def show_highscore(x, y):
    #highscore = font.render("Highscore : " + str(highscore_in_no), True, (255, 255, 255))
    #screen.blit(highscore, (x, y))


def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))
    sys.exit()

def victory_text():
    vic_text = over_font.render("VICTORY ACHIEVED", True, (255, 255, 255))
    screen.blit(vic_text, (50, 150))


def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))

def bunker(x, y ,i):
    screen.blit(bunkerImg[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 40, y + 40))

def fire_laser1(x, y):
    #global laser_state[0]
    laser_state[0] = "fire"
    screen.blit(laserImg, (x, y))

def fire_laser2(x, y):
    #global laser_state[1]
    laser_state[1] = "fire"
    screen.blit(laserImg, (x, y))

def fire_laser3(x, y):
    #global laser_state[2]
    laser_state[2] = "fire"
    screen.blit(laserImg, (x, y))

def fire_laser4(x, y):
    #global laser_state[3]
    laser_state[3] = "fire"
    screen.blit(laserImg, (x, y))

def fire_laser5(x, y):
    #global laser_state[4]
    laser_state[4] = "fire"
    screen.blit(laserImg, (x, y))


def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow(enemyX - bulletX, 2) + (math.pow(enemyY - bulletY, 2)))
    if distance < 50:
        return True
    else:
        return False

def isBunkerCollision(bunkerX, bunkerY, laserX, laserY):
    distance = math.sqrt(math.pow(bunkerX - laserX, 2) + (math.pow(bunkerY - laserY, 2)))
    if distance < 50:
        return True
    else:
        return False

def isSpaceshipCollision(playerX, playerY, laserX, laserY):
    distance = math.sqrt(math.pow(playerX - laserX, 2) + (math.pow(playerY - laserY, 2)))
    if distance < 25:
        return True
    else:
        return False



# Game Loop
running = True
while running:

    # RGB = Red, Green, Blue
    screen.fill((0, 0, 0))
    # Background Image
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # if keystroke is pressed check whether its right or left
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -5
            if event.key == pygame.K_RIGHT:
                playerX_change = 5
            if event.key == pygame.K_SPACE:
                if bullet_state is "ready":
                    bulletSound = mixer.Sound("laser.wav")
                    bulletSound.play()
                    # Get the current x cordinate of the spaceship
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0
        
        if laser_state[0] == "ready":
            laserX[0] = enemyX[20]
            laserY[0] = enemyY[20]
            fire_laser1(laserX[0], laserY[0])

        if laser_state[1] == "ready":
            laserX[1] = enemyX[21]
            laserY[1] = enemyY[21]
            fire_laser2(laserX[1], laserY[1])

        if laser_state[2] == "ready":
            laserX[2] = enemyX[22]
            laserY[2] = enemyY[22]
            fire_laser3(laserX[2], laserY[2])

        if laser_state[3] == "ready":
            laserX[3] = enemyX[23]
            laserY[3] = enemyY[23]
            fire_laser4(laserX[3], laserY[3])

        if laser_state[4] == "ready":
            laserX[4] = enemyX[24]
            laserY[4] = enemyY[24]
            fire_laser5(laserX[4], laserY[4])

        for contor in range(0, 5):
            if laserY[contor] >= 750:
                laser_state[contor] = "ready"
            

    playerX += playerX_change
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    # Enemy Movement
    for i in range(num_of_enemies):

        # Game Over
        if enemyY[i] > 440:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break
        sem = 0
        for z in range(num_of_enemies):
                if enemyY[z] > 0:
                   sem = 1
        if sem == 0:
            victory_text()
            break
        

        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 2
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -2
            enemyY[i] += enemyY_change[i]

        # Collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosionSound = mixer.Sound("explosion.wav")
            explosionSound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            enemyY[i] = -10000
        
        # Bunker Collision
        for bunk in range(0, 5):
            for projectile in range(0, 5):
                collision2 = isBunkerCollision(bunkerX[bunk], bunkerY[bunk], laserX[projectile], laserY[projectile])
                if collision2:
                    explosionSound = mixer.Sound("explosion.wav")
                    explosionSound.play()
                    laserY[projectile] = enemyY[20 + projectile]
                    laser_state[projectile] = "ready"
                    bunkerY[bunk] = +10000
        
        # Spaceship Collision

        for projectile in range(0, 5):
            collision3 = isSpaceshipCollision(playerX, playerY, laserX[projectile], laserY[projectile])
            if collision3:
                explosionSound = mixer.Sound("explosion.wav")
                explosionSound.play()
                game_over_text()
                break

                        
            
        enemy(enemyX[i], enemyY[i], i)
        if i % 5 == 0:
            z = int(i / 5)
            bunker(bunkerX[z], bunkerY[z], z)

    # Bullet Movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"

    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    if laser_state[0] == "fire":
        fire_laser1(laserX[0], laserY[0])
        laserY[0] += laserY_change

    if laser_state[1] == "fire":
        fire_laser2(laserX[1], laserY[1])
        laserY[1] += laserY_change

    if laser_state[2] == "fire":
        fire_laser3(laserX[2], laserY[2])
        laserY[2] += laserY_change

    if laser_state[3] == "fire":
        fire_laser4(laserX[3], laserY[3])
        laserY[3] += laserY_change

    if laser_state[4] == "fire":
        fire_laser5(laserX[4], laserY[4])
        laserY[4] += laserY_change


    player(playerX, playerY)
    show_score(textX, textY)
    #show_highscore(text2X, text2Y)
    pygame.display.update()
    