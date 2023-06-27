import pygame
from constants import *
from sys import exit
from enemy import Enemy
from player import Player
from plataforma import Platform
from auxiliar import Auxiliar

screen = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))


def terminar_juego():
    if player.is_dead and player.finish_dead_animation:
        screen.fill(BLACK)
        font = pygame.font.SysFont("Arial", 100)
        font_surface = font.render("YOU LOSE", True, RED)

        screen.blit(font_surface, (ANCHO_VENTANA / 3, ALTO_VENTANA / 2))

        return True


# Configuracion Pygame
pygame.init()
clock = pygame.time.Clock()

imagen_fondo = pygame.transform.scale(
    pygame.image.load(Auxiliar.set_background_level("level_1")),
    (ANCHO_VENTANA, ALTO_VENTANA),
)

player = Player("mask", 0, 0, 4, 8, 8, 16, 140, 7, 7)


lista_plataformas = []
lista_plataformas.append(Platform(400, 500, 70, 70, 1))
lista_plataformas.append(Platform(470, 430, 70, 70, 2))
lista_plataformas.append(Platform(540, 360, 70, 70, 4))
lista_plataformas.append(Platform(610, 290, 70, 70, 5))

# tick_2s = pygame.USEREVENT
# pygame.time.set_timer(tick_2s, 2000)

enemies_list = [Enemy("enemy", 1, 4, 8, 8, 7), Enemy("enemy", 500, 4, 8, 8, 7)]

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    if not terminar_juego():
        delta_ms = clock.tick(FPS)
        screen.blit(imagen_fondo, imagen_fondo.get_rect())

        for plataforma in lista_plataformas:
            plataforma.render(screen)

        keys_pressed = pygame.key.get_pressed()

        player.events(keys_pressed, delta_ms)
        player.update(delta_ms, lista_plataformas, enemies_list)
        player.render(screen)

        for enemy in enemies_list:
            enemy.update(delta_ms, lista_plataformas, player)
            enemy.render(screen)

    pygame.display.flip()
