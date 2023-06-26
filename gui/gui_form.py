import pygame
from constants import *


class Form:
    forms_dict = {}

    def __init__(
        self, name, master_surface, x, y, w, h, bg_color, border_color, active
    ):
        self.forms_dict[name] = self
        self.master_surface = master_surface
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.background_color = bg_color
        self.border_color = border_color

        self.slave_surface = pygame.Surface((w, h))
        self.slave_rect = self.slave_surface.get_rect()
        self.slave_rect.x = x
        self.slave_rect.y = y
        self.active = active

        if self.background_color != None:
            self.slave_surface.fill(self.background_color)

    def set_active(self, name):
        for aux_form in self.forms_dict.values():
            aux_form.active = False
        self.forms_dict[name].active = True

    def draw(self):
        self.master_surface.blit(self.slave_surface, self.slave_rect)
