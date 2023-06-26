import pygame
from constants import *
from sys import exit
from enemy import Enemy
from player import Player
from plataforma import Platform

screen = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))
pygame.init()
clock = pygame.time.Clock()

imagen_fondo = pygame.image.load(f"{PATH_IMAGES}/locations/forest/all.png")
imagen_fondo = pygame.transform.scale(imagen_fondo, (ANCHO_VENTANA, ALTO_VENTANA))
player = Player("mask", 0, 0, 4, 8, 8, 16, 7, 140)
enemy_1 = Enemy("enemy", 1, GROUND_LEVEL, 4, 8, 8, 7)

enemies_list = [enemy_1]

lista_plataformas = []
lista_plataformas.append(Platform(400, 500, 70, 70, 1))
lista_plataformas.append(Platform(470, 430, 70, 70, 2))
lista_plataformas.append(Platform(540, 360, 70, 70, 4))
lista_plataformas.append(Platform(610, 290, 70, 70, 5))

# tick_2s = pygame.USEREVENT
# pygame.time.set_timer(tick_2s, 2000)


while True:
    delta_ms = clock.tick(FPS)
    screen.blit(imagen_fondo, imagen_fondo.get_rect())

    for plataforma in lista_plataformas:
        plataforma.render(screen)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        # for enemy in enemies_list:
        #     enemy.run()

    keys_pressed = pygame.key.get_pressed()

    player.events(keys_pressed, delta_ms)
    player.update(delta_ms, lista_plataformas, enemies_list)
    player.render(screen)

    for enemy in enemies_list:
        enemy.update(delta_ms, lista_plataformas)
        enemy.render(screen)

    pygame.display.flip()
