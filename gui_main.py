import pygame
from pygame.locals import *
import sys
from constantes import *
from gui_form import Form
from gui_form_menu_A import FormMenuA
from gui_form_menu_B import FormMenuB
from gui_form_menu_C import FormMenuC
from gui_form_menu_D import FormMenuD
from gui_form_game import FormGame
from gui_form_menu_init import FormMenuInit
from gui_form_menu_score import FormMenuScore

flags = DOUBLEBUF
screen = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA), flags, 16)
pygame.init()
pygame.mixer.init()
clock = pygame.time.Clock()

event_1000ms = pygame.USEREVENT
pygame.time.set_timer(event_1000ms, 1000)

form_menu_init = FormMenuInit(
    name="form_menu_init",
    master_surface=screen,
    w=500,
    h=500,
    image_background="images/gui/jungle/level_select/bg.png",
    color_border=(255, 0, 255),
    active=True,
)

form_menu_score = FormMenuScore(
    name="form_menu_score",
    master_surface=screen,
    w=500,
    h=500,
    image_background="images/gui/jungle/level_select/bg.png",
    color_border=(255, 0, 255),
    active=False,
)

form_menu_A = FormMenuA(
    name="form_menu_A",
    master_surface=screen,
    w=500,
    h=500,
    image_background="images/gui/jungle/level_select/bg.png",
    color_border=(255, 0, 255),
    active=False,
)

form_menu_B = FormMenuB(
    name="form_menu_B",
    master_surface=screen,
    w=500,
    h=500,
    image_background="images/gui/jungle/level_select/bg.png",
    color_border=(255, 0, 255),
    active=False,
)

form_menu_C = FormMenuC(
    name="form_menu_C",
    master_surface=screen,
    w=500,
    h=500,
    image_background="images/gui/jungle/level_select/bg.png",
    color_border=(255, 0, 255),
    active=False,
)

form_menu_D = FormMenuD(
    name="form_menu_D",
    master_surface=screen,
    w=500,
    h=500,
    image_background="images/gui/jungle/level_select/bg.png",
    color_border=(255, 0, 255),
    active=False,
)

form_menu_score.create_table()

form_game_L1 = FormGame(
    name="form_game_L1",
    master_surface=screen,
    w=ANCHO_VENTANA,
    h=ALTO_VENTANA,
    image_background=None,
    color_border=(255, 0, 255),
    active=False,
    level="l1",
    event_cronometer=event_1000ms,
)

form_game_L2 = FormGame(
    name="form_game_L2",
    master_surface=screen,
    w=ANCHO_VENTANA,
    h=ALTO_VENTANA,
    image_background=None,
    color_border=(255, 0, 255),
    active=False,
    level="l2",
    event_cronometer=event_1000ms,
)

form_game_L3 = FormGame(
    name="form_game_L3",
    master_surface=screen,
    w=ANCHO_VENTANA,
    h=ALTO_VENTANA,
    image_background=None,
    color_border=(255, 0, 255),
    active=False,
    level="l3",
    event_cronometer=event_1000ms,
)

while True:
    lista_eventos = pygame.event.get()
    for event in lista_eventos:
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()
    delta_ms = clock.tick(FPS)

    aux_form_active = Form.get_active()
    if aux_form_active != None:
        aux_form_active.update(lista_eventos, keys, delta_ms)
        aux_form_active.draw()

    pygame.display.flip()
