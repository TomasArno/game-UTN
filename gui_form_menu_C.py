from pygame.locals import *
from gui_form import Form
from gui_button import Button
from gui_progressbar import ProgressBar
from constantes import *
import pygame


class FormMenuC(Form):
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

        self.pb1 = ProgressBar(
            master=self,
            x=100,
            y=180,
            w=300,
            h=50,
            color_background=None,
            color_border=None,
            image_background="images/gui/set_gui_01/Comic_Border/Bars/Bar_Background01.png",
            image_progress="images/gui/set_gui_01/Comic_Border/Bars/Bar_Segment05.png",
            value=3,
            value_max=8,
        )

        self.boton1 = Button(
            master=self,
            x=150,
            y=260,
            w=80,
            h=50,
            color_background=None,
            color_border=None,
            image_background="images/gui/jungle/btn/prew.png",
            on_click=self.on_click_boton,
            on_click_param="-",
            font="Verdana",
            font_size=30,
            font_color=C_WHITE,
        )
        self.boton2 = Button(
            master=self,
            x=270,
            y=260,
            w=80,
            h=50,
            color_background=None,
            color_border=None,
            image_background="images/gui/jungle/btn/next.png",
            on_click=self.on_click_boton,
            on_click_param="+",
            font="Verdana",
            font_size=30,
            font_color=C_WHITE,
        )

        self.boton3 = Button(
            master=self,
            x=self.w / 2 - 60,
            y=self.h - 60,
            w=60,
            h=50,
            color_background=None,
            color_border=None,
            image_background="images/gui/jungle/btn/ok.png",
            on_click=self.on_click_boton1,
            on_click_param="form_menu_B",
            font="Verdana",
            font_size=30,
            font_color=C_WHITE,
        )
        self.boton4 = Button(
            master=self,
            x=self.w / 2,
            y=self.h - 60,
            w=60,
            h=50,
            color_background=None,
            color_border=None,
            image_background="images/gui/jungle/btn/sound_off.png",
            on_click=self.on_click_boton,
            on_click_param="",
            font="Verdana",
            font_size=30,
            font_color=C_WHITE,
        )

        self.lista_widget = [
            self.boton1,
            self.boton2,
            self.boton3,
            self.boton4,
            self.pb1,
        ]

    def on_click_boton(self, parametro):
        if parametro == "+":
            self.pb1.value += 1
        elif parametro == "-":
            self.pb1.value -= 1
        else:
            self.pb1.value = 0

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
            pygame.image.load("images/gui/jungle/settings/92.png"),
            (self.w, 150),
        ).convert_alpha()

        self.surface.blit(image, (0, 0))
