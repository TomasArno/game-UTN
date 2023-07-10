from pygame.locals import *
from constantes import *
from gui_form import Form
from gui_button import Button
import pygame


class FormMenuA(Form):
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

        # self.boton2 = Button(
        #     master=self,
        #     x=30,
        #     y=180,
        #     w=100,
        #     h=50,
        #     color_background=None,
        #     color_border=None,
        #     image_background="images/gui/jungle/bubble/level.png",
        #     on_click=self.on_click_boton3,
        #     on_click_param="form_game_L1",
        #     font="Verdana",
        #     font_size=30,
        #     font_color=C_WHITE,
        # )
        self.boton1 = Button(
            master=self,
            x=140,
            y=180,
            w=25,
            h=50,
            color_background=None,
            color_border=None,
            image_background="images/gui/jungle/bubble/1.png",
            on_click=self.on_click_boton3,
            on_click_param="form_game_L1",
            font="Verdana",
            font_size=30,
            font_color=C_WHITE,
        )

        # self.boton8 = Button(
        #     master=self,
        #     x=165,
        #     y=230,
        #     w=100,
        #     h=50,
        #     color_background=None,
        #     color_border=None,
        #     image_background="images/gui/jungle/bubble/level.png",
        #     on_click=self.on_click_boton3,
        #     on_click_param="form_game_L1",
        #     font="Verdana",
        #     font_size=30,
        #     font_color=C_WHITE,
        # )

        self.boton2 = Button(
            master=self,
            x=275,
            y=230,
            w=25,
            h=50,
            color_background=None,
            color_border=None,
            image_background="images/gui/jungle/level_select/lock.png",
            on_click=self.on_click_boton3,
            on_click_param="form_game_L2",
            font="Verdana",
            font_size=30,
            font_color=C_WHITE,
        )

        # self.boton9 = Button(
        #     master=self,
        #     x=300,
        #     y=280,
        #     w=100,
        #     h=50,
        #     color_background=None,
        #     color_border=None,
        #     image_background="images/gui/jungle/bubble/level.png",
        #     on_click=self.on_click_boton3,
        #     on_click_param="form_game_L1",
        #     font="Verdana",
        #     font_size=30,
        #     font_color=C_WHITE,
        # )
        self.boton3 = Button(
            master=self,
            x=410,
            y=280,
            w=25,
            h=50,
            color_background=None,
            color_border=None,
            image_background="images/gui/jungle/level_select/lock.png",
            on_click=self.on_click_boton3,
            on_click_param="form_game_L3",
            font="Verdana",
            font_size=30,
            font_color=C_WHITE,
        )

        self.boton4 = Button(
            master=self,
            x=260,
            y=self.h - 60,
            w=60,
            h=50,
            color_background=None,
            color_border=None,
            image_background="images/gui/jungle/btn/prize.png",
            on_click=self.on_click_boton3,
            on_click_param="",
            font="Verdana",
            font_size=30,
            font_color=C_WHITE,
        )
        # self.boton5 = Button(
        #     master=self,
        #     x=20,
        #     y=260,
        #     w=140,
        #     h=50,
        #     color_background=None,
        #     color_border=None,
        #     image_background="images/gui/set_gui_01/Comic_Border/Buttons/Button_M_02.png",
        #     on_click=self.on_click_boton3,
        #     on_click_param="form_menu_B",
        #     text="SQL",
        #     font="Verdana",
        #     font_size=30,
        #     font_color=C_WHITE,
        # )

        self.lista_widget = [self.boton1, self.boton2, self.boton3, self.boton4]

    def on_click_boton1(self, parametro):
        self.pb1.value += 1

    def on_click_boton2(self, parametro):
        self.pb1.value -= 1

    def on_click_boton3(
        self, parametro
    ):  # si agrego boton que no sea para ir a algun nivel tiene que ser otro boton
        # self.set_actual_level(parametro)

        self.set_active(parametro)

    def update(self, lista_eventos, keys, delta_ms):
        for aux_widget in self.lista_widget:
            aux_widget.update(lista_eventos)

        if "l1" in self.levels_completed:
            self.boton2.set_image("images/gui/jungle/bubble/2.png")
        if "l2" in self.levels_completed:
            self.boton3.set_image("images/gui/jungle/bubble/3.png")

    def draw(self):
        super().draw()
        for aux_widget in self.lista_widget:
            aux_widget.draw()

        image_header = pygame.transform.scale(
            pygame.image.load("images/gui/jungle/level_select/header.png"),
            (self.w, 150),
        ).convert_alpha()

        self.surface.blit(image_header, (0, 0))
