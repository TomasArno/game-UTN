import pygame
from pygame.locals import *
from constantes import *
from auxiliar import *


class Form:
    forms_dict = {}
    levels_completed: list = []

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

        self.surface: pygame.Surface = pygame.Surface((w, h))
        self.slave_rect: pygame.Rect = self.surface.get_rect()
        self.slave_rect.x = x
        self.slave_rect.y = y
        self.active = active
        self.actual_level = False

        self.start_form_time = pygame.time.Clock()
        self.current_time = 0

        if image_background:
            self.image_background = pygame.transform.scale(
                pygame.image.load(image_background), (w, h)
            ).convert_alpha()

            self.surface.blit(self.image_background, (0, 0))

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

    # @staticmethod
    # def set_actual_level(name):
    #     for level in Form.forms_dict.values():
    #         level.actual_level = False
    #     Form.forms_dict[name].actual_level = True

    # @staticmethod
    # def get_actual_level():
    #     for level in Form.forms_dict.values():
    #         if level.actual_level:
    #             return level
    #     return None

    #     # self.surface.fill(C_GREEN)
    #     # self.slave_rect.x = 1300
    #     font = Auxiliar.generate_text("Arial", 100, "YOU WIN", C_GREEN)
    #     self.surface.blit(font, (ANCHO_VENTANA / 2.5, ALTO_VENTANA / 2.5))
    #     print(font.get_rect())

    #     pass
    #     # self.surface.fill(C_BLACK)
    #     # font = Auxiliar.generate_text("Arial", 100, "YOU LOSE", C_RED)
    #     # self.surface.blit(font, (ANCHO_VENTANA / 2.5, ALTO_VENTANA / 2.5))

    def draw(self):
        if self.active:
            if DEBUG:
                pygame.draw.rect(self.surface, color=(0, 255, 0), rect=self.slave_rect)

            self.master_surface.blit(self.surface, self.slave_rect)
