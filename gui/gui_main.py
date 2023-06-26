import pygame
from sys import exit
from constants import *
from gui_form_menu_a import FormMenuA
from gui_form_menu_b import FormMenuB

screen = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))
pygame.init()

clock = pygame.time.Clock()

form_menu_A = FormMenuA(
    name="form_menu_A",
    master_surface=screen,
    x=0,
    y=100,
    w=300,
    h=400,
    bg_color=(255, 255, 0),
    border_color=(255, 0, 255),
    active=True,
)
form_menu_B = FormMenuB(
    name="form_menu_B",
    master_surface=screen,
    x=0,
    y=100,
    w=300,
    h=400,
    bg_color=(0, 255, 255),
    border_color=(255, 0, 255),
    active=False,
)


while True:
    delta_ms = clock.tick(FPS)
    events_list = pygame.event.get()
    for event in events_list:
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    keys_pressed = pygame.key.get_pressed()

    if form_menu_A.active:
        form_menu_A.update(events_list)
        form_menu_A.draw()

    elif form_menu_B.active:
        form_menu_B.update(events_list)
        form_menu_B.draw()

    pygame.display.flip()
