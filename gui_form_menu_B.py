from pygame.locals import *
from gui_form import Form
from gui_button import Button
from constantes import *
import pygame

import sqlite3


class FormMenuB(Form):
    def __init__(
        self, name, master_surface, w, h, image_background, color_border, active
    ):
        super().__init__(
            name,
            master_surface,
            w,
            h,
            color_border,
            active,
            image_background,
            x=ANCHO_VENTANA / 2 - w / 2,
            y=ALTO_VENTANA / 2 - h / 2,
        )
        self.boton2 = Button(
            master=self,
            x=self.w / 2 - 85,
            y=self.h - 60,
            w=60,
            h=50,
            color_background=None,
            color_border=None,
            image_background="images/gui/jungle/btn/menu.png",
            on_click=self.on_click_boton1,
            on_click_param="form_menu_A",
            font="Verdana",
            font_size=30,
            font_color=C_WHITE,
        )

        self.boton3 = Button(
            master=self,
            x=self.w / 2 - 20,
            y=self.h - 60,
            w=60,
            h=50,
            color_background=None,
            color_border=None,
            image_background="images/gui/jungle/btn/play.png",
            on_click=self.on_click_boton,
            font="Verdana",
            font_size=30,
            font_color=C_WHITE,
        )
        self.boton4 = Button(
            master=self,
            x=self.w / 2 + 45,
            y=self.h - 60,
            w=60,
            h=50,
            color_background=None,
            color_border=None,
            image_background="images/gui/jungle/menu/setting.png",
            on_click=self.on_click_boton1,
            on_click_param="form_menu_C",
            font="Verdana",
            font_size=30,
            font_color=C_WHITE,
        )

        self.lista_widget = [
            self.boton2,
            self.boton3,
            self.boton4,
        ]

    def set_last_form_played(self, last_form_played):
        self.last_form_played = last_form_played

    def on_click_boton(self, parametro):
        if self.last_form_played:
            self.set_active(self.last_form_played)

    def on_click_boton1(self, parametro):
        self.set_active(parametro)

    def update(self, lista_eventos, keys, delta_ms):
        for aux_widget in self.lista_widget:
            aux_widget.update(lista_eventos)

    def draw(self):
        super().draw()
        for aux_widget in self.lista_widget:
            aux_widget.draw()

        image = pygame.transform.scale(
            pygame.image.load("images/gui/jungle/pause/header.png"),
            (self.w, 150),
        ).convert_alpha()

        self.surface.blit(image, (0, 0))
