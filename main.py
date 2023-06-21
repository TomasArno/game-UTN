import pygame
import sys
from constantes import *
from player import Player

screen = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))
pygame.init()
clock = pygame.time.Clock()

imagen_fondo = pygame.image.load("images/locations/forest/all.png")
imagen_fondo = pygame.transform.scale(imagen_fondo, (ANCHO_VENTANA, ALTO_VENTANA))
player_1 = Player(650, 0, 4, 8, 8, 16, 10, 300)


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player_1.jump(True)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                player_1.jump(False)

    keys_pressed = pygame.key.get_pressed()

    if keys_pressed[pygame.K_RIGHT] and not keys_pressed[pygame.K_LEFT]:
        player_1.walk(VIEW_DIRECTION_R)
    elif keys_pressed[pygame.K_LEFT] and not keys_pressed[pygame.K_RIGHT]:
        player_1.walk(VIEW_DIRECTION_L)
    elif (
        keys_pressed[pygame.K_LEFT]
        and keys_pressed[pygame.K_RIGHT]
        and not keys_pressed[pygame.K_SPACE]
    ):
        player_1.stay()
    elif (
        not keys_pressed[pygame.K_LEFT]
        and not keys_pressed[pygame.K_RIGHT]
        and not keys_pressed[pygame.K_SPACE]
    ):
        player_1.stay()

    screen.blit(imagen_fondo, imagen_fondo.get_rect())

    delta_ms = clock.tick(FPS)
    player_1.update(delta_ms)
    player_1.draw(screen)

    # enemigos update
    # player dibujarlo
    # dibujar todo el nivel

    pygame.display.flip()
