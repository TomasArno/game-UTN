from pygame.locals import *
from constantes import *
from gui_form import Form
from gui_button import Button
from gui_form_game import FormGame
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

        self.boton1 = Button(
            master=self,
            x=self.w / 4 - 33,
            y=180,
            w=65,
            h=65,
            color_background=None,
            color_border=None,
            image_background="images/PIXEL ADVENTURE/PIXEL ADVENTURE/Recursos/Menu/Levels/01.png",
            on_click=self.on_click_boton3,
            on_click_param="form_game_L1",
            font="Verdana",
            font_size=30,
            font_color=C_WHITE,
        )

        self.boton2 = Button(
            master=self,
            x=self.w / 2 - 25,
            y=184,
            w=50,
            h=50,
            color_background=None,
            color_border=None,
            image_background="images/gui/jungle/level_select/lock.png",
            font="Verdana",
            font_size=30,
            font_color=C_WHITE,
        )
        self.boton3 = Button(
            master=self,
            x=self.w / 2 - 33,
            y=180,
            w=65,
            h=65,
            color_background=None,
            color_border=None,
            image_background="images/PIXEL ADVENTURE/PIXEL ADVENTURE/Recursos/Menu/Levels/02.png",
            on_click=self.on_click_boton3,
            on_click_param="form_game_L2",
            font="Verdana",
            font_size=30,
            font_color=C_WHITE,
        )

        self.boton4 = Button(
            master=self,
            x=self.w / 1.25 - 50,
            y=184,
            w=50,
            h=50,
            color_background=None,
            color_border=None,
            image_background="images/gui/jungle/level_select/lock.png",
            font="Verdana",
            font_size=30,
            font_color=C_WHITE,
        )

        self.boton5 = Button(
            master=self,
            x=self.w / 1.25 - 50,
            y=180,
            w=65,
            h=65,
            color_background=None,
            color_border=None,
            image_background="images/PIXEL ADVENTURE/PIXEL ADVENTURE/Recursos/Menu/Levels/03.png",
            on_click=self.on_click_boton3,
            on_click_param="form_game_L3",
            font="Verdana",
            font_size=30,
            font_color=C_WHITE,
        )
        self.boton6 = Button(
            master=self,
            x=self.w / 2 - 30,
            y=self.h - 60,
            w=60,
            h=50,
            color_background=None,
            color_border=None,
            image_background="images/gui/jungle/btn/prize.png",
            on_click=self.on_click_boton3,
            on_click_param="form_menu_score",
            font="Verdana",
            font_size=30,
            font_color=C_WHITE,
        )

        self.flag_l1 = True
        self.flag_l2 = True

        self.lista_widget = [self.boton1, self.boton2, self.boton4]

    def on_click_boton1(self, parametro):
        self.pb1.value += 1

    def on_click_boton2(self, parametro):
        self.pb1.value -= 1

    def on_click_boton3(self, parametro):
        self.set_active(parametro)

    def update(self, lista_eventos, keys, delta_ms):
        for aux_widget in self.lista_widget:
            aux_widget.update(lista_eventos)

        if FormGame.game_completed:
            self.lista_widget.append(self.boton6)

        if "l1" in Form.levels_completed and self.flag_l1:
            self.flag_l1 = False
            self.boton2.inactive()
            self.lista_widget.remove(self.boton2)
            self.lista_widget.append(self.boton3)

        if "l2" in Form.levels_completed and self.flag_l2:
            self.flag_l2 = False
            self.boton4.inactive()
            self.lista_widget.remove(self.boton4)
            self.lista_widget.append(self.boton5)

    def draw(self):
        super().draw()
        for aux_widget in self.lista_widget:
            aux_widget.draw()

        image_header = pygame.transform.scale(
            pygame.image.load("images/gui/jungle/level_select/header.png"),
            (self.w, 150),
        ).convert_alpha()

        self.surface.blit(image_header, (0, 0))
