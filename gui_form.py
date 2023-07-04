import pygame
from pygame.locals import *


class Form:
    forms_dict = {}

    def __init__(
        self, name, master_surface, x, y, w, h, color_background, color_border, active
    ):
        self.forms_dict[name] = self
        self.master_surface = master_surface
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.color_background = color_background
        self.color_border = color_border

        self.surface = pygame.Surface((w, h))
        self.slave_rect = self.surface.get_rect()
        self.slave_rect.x = x
        self.slave_rect.y = y
        self.active = active

        self.completed_level = False

        self.start_form_time = pygame.time.Clock()
        self.current_time = 0

        if self.color_background != None:
            self.surface.fill(self.color_background)

    @staticmethod
    def set_active(name):
        for aux_form in Form.forms_dict.values():
            aux_form.active = False
        Form.forms_dict[name].active = True

    @staticmethod
    def get_active():
        for aux_form in Form.forms_dict.values():
            if aux_form.active:
                return aux_form
        return None

    @staticmethod
    def terminar_juego():
        Form.set_active("form_menu_A")
        # if player.is_dead and player.finish_dead_animation:
        #     screen.fill(BLACK)
        #     font = pygame.font.SysFont("Arial", 100)
        #     font_surface = font.render("YOU LOSE", True, RED)

        #     screen.blit(font_surface, (ANCHO_VENTANA / 3, ALTO_VENTANA / 2))

        #     return True

    def draw(self):
        self.master_surface.blit(self.surface, self.slave_rect)
