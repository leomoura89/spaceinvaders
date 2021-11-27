import math
import random

import pygame
from pygame import mixer

#Iniciar o pygame
pygame.init()

#Criar a tela do jogo
tela = pygame.display.set_mode((800,600))

#Background
background = pygame.image.load('background.png')

#Som de background
mixer.music.load('background.wav')
mixer.music.play(-1)


#Titulo e icone
pygame.display.set_caption("Guardiões do Espaço")
icon = pygame.image.load('icon.png')
pygame.display.set_icon(icon)

#Player
playerImg = pygame.image.load('spaceship.png')
playerX = 370
playerY = 480
playerX_change = 0

#Inimigos
enemyImg = []
enemyX = []
enemyY = [] 
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

#Cada inimigo vai receber essas mesmas características
for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('enemy.png'))
    enemyX.append(random.randint(0,735))
    enemyY.append(random.randint(50,150))
    enemyX_change.append(4)
    enemyY_change.append(40)

#Balas

#Pronto - Você não pode ver a bala na tela
#Fogo - A bala está em movimento
bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 10
bullet_state = "pronto"

#Score/Pontuação

score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)

textX = 10
textY = 10

#Game Over
over_font = pygame.font.Font('freesansbold.ttf', 64)

def show_score(x,y):
    score = font.render("Pontuação: "+ str(score_value), True, (255,255,255))
    tela.blit(score,(x,y))

def game_over_text():
    over_text = over_font.render("FIM DE JOGO", True, (255, 255, 255))
    tela.blit(over_text, (200, 250))

def player(x,y):
    #Desenhar o player
    tela.blit(playerImg,(x,y))

def enemy(x,y, i):
    #Desenhar o inimigo
    tela.blit(enemyImg[i],(x,y))

def fire_bullet(x,y):
    global bullet_state
    bullet_state = "fogo"
    tela.blit(bulletImg, (x + 16, y + 10))

def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX - bulletX,2))+(math.pow(enemyY - bulletY,2)))
    if distance <27:
        return True
    else:
        return False

#Loop para deixar o jogo rodando
iniciar = True
#Tudo que precisar estar sempre aparecendo na tela tem que estar nesse loop
while iniciar:

    #Cores em RGB - Red, Green, Blue. 
    tela.fill((0,0,0))
    #Background Image
    tela.blit(background, (0,0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            iniciar = False

        #Se um botão do teclado for pressionado, checar se é para direita ou esquerda
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -5
            if event.key == pygame.K_RIGHT:
                playerX_change = 5

            if event.key == pygame.K_SPACE:
                if bullet_state is "pronto":
                    bulletSound = mixer.Sound("laser.wav")
                    bulletSound.play() 
                    #Receber a coordenada X da nave do momento que apertar
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)

        #Checar quando o botão parar de ser pressionado.
        if event.type == pygame.KEYUP:
            playerX_change = 0

    #Checar os limites da nave
    playerX += playerX_change

    if playerX <=0:
        playerX = 0
    #Usar o 736 aqui pois está descontando os 64 pixels que a imagem tem
    elif playerX>=736:
        playerX = 736


    #Movimento do inimigo
    
    for i in range(num_of_enemies): 

        #Game Over
        if enemyY[i] > 440:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break

        enemyX[i] += enemyX_change[i]
        if enemyX[i] <=0:
            #velocidade do movimento no eixo X
            enemyX_change[i] = 4
            enemyY[i] += enemyY_change[i]
        #Usar o 736 aqui pois está descontando os 64 pixels que a imagem tem
        elif enemyX[i]>=736:
            #velocidade do movimento no eixo X
            enemyX_change[i] = -4
            enemyY[i] += enemyY_change[i]

        #Colisão
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosionSound = mixer.Sound("explosion.wav")
            explosionSound.play()
            bulletY = 480
            bullet_state = "pronto" 
            score_value += 1
            enemyX[i] = random.randint(0,736)
            enemyY[i] = random.randint(50,150)

        enemy(enemyX[i], enemyY[i], i)

    #Movimento das balas
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "pronto"

    if bullet_state is "fogo":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    


    player(playerX, playerY)
    show_score(textX, textY)

    #Atualizar a tela constantemente
    pygame.display.update()
