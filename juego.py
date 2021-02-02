import pygame
import random
import math
from pygame import mixer


pygame.init()


# Creando el fondo
pantalla = pygame.display.set_mode((800, 600))  # pasar el ancho y el alto


# Ventana de juego
pygame.display.set_caption("Space Invaders Fernando")# nombre de la venana
icono = pygame.image.load('nave.png') #definiendo el icono del juego 
pygame.display.set_icon(icono) #aplicar el icono a la ventana del juego


# imagen de fondo
img_fondo = pygame.image.load("fondo.png")


# musica de fondo
mixer.music.load("fondo.mp3") 
mixer.music.play(-1) #se le pasa -1 para poner la musica en un loop


# Definir jugador
icono_jugador = pygame.image.load('nave.png')
playerX = 370
playerY = 480
changedX = 0
playerSpeed = 10


# Puntos
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)


def mostrar_puntaje(x,y):
    score = font.render("Puntos  : "+str(score_value),True,(255,255,255))
    pantalla.blit(score,(x,y))


#Game over
def game_over():
    overfont = pygame.font.Font('freesansbold.ttf',64)
    gamefont = overfont.render("GAME OVER",True,(255,255,255))
    pantalla.blit(gamefont,(200,250))


def nano(x,y):
    font2 = pygame.font.Font('freesansbold.ttf',14)
    score = font2.render("Desarrollado por Fernando Noguera.",True,(255,255,255))
    pantalla.blit(score,(x,y))


def player(x, y):
    pantalla.blit(icono_jugador, (playerX, playerY))


# Invasores
invasoresImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
numero_invasores = 10


for i in range(numero_invasores):
    invasoresImg.append(pygame.image.load('invasor.png'))
    enemyX.append(random.randint(0, 736))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(4)
    enemyY_change.append(40)

    def enemy(x, y, i):
        pantalla.blit(invasoresImg[i], (x, y))


# Balas nave
icono_bala = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
bulletY_changed = 20  #Velocidad Disparo
estado_bala = "ready"


def disparo(x, y):
    global estado_bala
    estado_bala = "fuego"
    pantalla.blit(icono_bala, (x + 16, y + 10))


def headShoot(enemyX, enemyY, bulletX, bulletY):
    distancia = math.sqrt(math.pow(enemyX - bulletX, 2) + (math.pow(enemyY - bulletY, 2)))
    if distancia < 27:
        return True
    else:
        return False

running = True
# Loop para iniciar el juego
while running:
    pantalla.fill((0, 0, 0)) #fondo de pantalla
    pantalla.blit(img_fondo, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # movimientos jugador
        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_LEFT:
                changedX =- playerSpeed

            if event.key == pygame.K_RIGHT:
                changedX =+ playerSpeed

            if event.key == pygame.K_SPACE:
                if estado_bala is "ready":
                    bullet_sound = mixer.Sound("laser.wav")
                    bullet_sound.play()
                    bulletX = playerX
                    estado_bala = "fuego"

        if event.type == pygame.KEYUP and (event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT):
            changedX = 0

    # movimientos del jugador
    playerX += changedX
    # Restringir al jugador dentro de la ventana
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    # Movimiento del enemigo
    for i in range(numero_invasores):

        # Game Over
        if enemyY[i] > 440:
            for j in range(numero_invasores):
                enemyY[j] = 2000
            game_over()
            nano(280,350)
            break
        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 4
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -4
            enemyY[i] += enemyY_change[i]

        # al matar a un enemigo
        collision = headShoot(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            mixer.Sound("explosion.wav").play()
            bulletY = 480
            estado_bala = "ready"
            score_value += 1
            enemyX[i] = random.randint(0, 736)
            enemyY[i] = random.randint(50, 150)
        
        enemy(enemyX[i], enemyY[i], i)

    # movimiento balas
    if bulletY <= 0:
        bulletY = 480
        estado_bala = "ready"

    if estado_bala is "fuego":
        disparo(bulletX, bulletY)
        bulletY -= bulletY_changed

    mostrar_puntaje(10,10)

    player(playerX, playerY)
    pygame.display.update()
    

