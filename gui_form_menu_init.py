from pygame.locals import *
from constantes import *
from gui_form import Form
from gui_button import Button
from gui_textbox import TextBox
import pygame


class FormMenuInit(Form):
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

        self.boton1 = Button(
            master=self,
            x=self.w / 2 - 25,
            y=self.h - 50,
            w=50,
            h=50,
            color_background=None,
            color_border=None,
            image_background="images/gui/jungle/btn/next.png",
            on_click=self.on_click_boton,
            on_click_param="form_menu_A",
            font="Verdana",
            font_size=30,
            font_color=C_WHITE,
        )

        self.txt1 = TextBox(
            master=self,
            x=self.w / 2 - 125,
            y=280,
            w=250,
            h=50,
            color_background=None,
            color_border=None,
            image_background="images/gui/set_gui_01/Comic_Border/Buttons/Button_XL_08.png",
            text="Your name",
            font="Verdana",
            font_size=30,
            font_color=C_WHITE,
        )

        self.lista_widget = [
            self.boton1,
            self.txt1,
        ]

    def on_click_boton(self, parametro):
        self.set_active(parametro)

    def update(self, lista_eventos, keys, delta_ms):
        for aux_widget in self.lista_widget:
            aux_widget.update(lista_eventos)

    def draw(self):
        super().draw()
        for aux_widget in self.lista_widget:
            aux_widget.draw()

        logo = pygame.transform.scale(
            pygame.image.load("images/gui/jungle/menu/logo.png"),
            (200, 100),
        ).convert_alpha()

        image_rating = pygame.transform.scale(
            pygame.image.load("images/gui/jungle/rating/face.png"),
            (100, 100),
        ).convert_alpha()

        self.surface.blit(logo, (self.w / 2 - 110, 30))
        self.surface.blit(image_rating, (self.w / 2 - 50, 160))
