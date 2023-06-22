import pygame
from sys import exit
from constants import *
from player import Player
from plataforma import Platform

screen = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))
pygame.init()
clock = pygame.time.Clock()

imagen_fondo = pygame.image.load(f"{PATH_IMAGES}/locations/forest/all.png")
imagen_fondo = pygame.transform.scale(imagen_fondo, (ANCHO_VENTANA, ALTO_VENTANA))
player_1 = Player(0, 0, 4, 8, 8, 16, 10, 200)

lista_plataformas = []
lista_plataformas.append(Platform(400, 500, 70, 70, 1))
lista_plataformas.append(Platform(470, 430, 70, 70, 2))
lista_plataformas.append(Platform(540, 360, 70, 70, 4))
lista_plataformas.append(Platform(610, 290, 70, 70, 5))

while True:
    delta_ms = clock.tick(FPS)
    screen.blit(imagen_fondo, imagen_fondo.get_rect())

    for plataforma in lista_plataformas:
        plataforma.render(screen)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    keys_pressed = pygame.key.get_pressed()

    player_1.events(keys_pressed, delta_ms)
    player_1.update(delta_ms, lista_plataformas)
    player_1.render(screen)

    # enemigos update
    # player dibujarlo
    # dibujar todo el nivel

    pygame.display.flip()
