import pygame
from pygame.locals import *
from constantes import *
from auxiliar import *


class Form:
    forms_dict = {}
    levels_completed: list = []
    players_name = None

    def __init__(
        self,
        name,
        master_surface,
        w,
        h,
        active,
        color_border,
        image_background,
        x=0,
        y=0,
    ):
        self.forms_dict[name] = self
        self.master_surface: pygame.Surface = master_surface
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.image_background = image_background
        self.color_border = color_border

        self.surface: pygame.Surface = pygame.Surface((w, h), pygame.SRCALPHA, 32)
        self.slave_rect: pygame.Rect = self.surface.get_rect()
        self.slave_rect.x = x
        self.slave_rect.y = y
        self.active = active

        self.start_form_time = pygame.time.Clock()
        self.current_time = 0

        if image_background:
            self.image_background = pygame.transform.scale(
                pygame.image.load(image_background), (w, h)
            ).convert_alpha()

            self.surface.blit(self.image_background, (0, 0))

    @staticmethod
    def set_players_name(players_name):
        Form.players_name = players_name

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
    def get_form(form_name):
        for aux_form in Form.forms_dict:
            if aux_form == form_name:
                return Form.forms_dict[aux_form]
        return None

    def draw(self):
        if self.active:
            self.master_surface.blit(self.surface, self.slave_rect)
