from pygame.locals import *
from gui_form import Form
from gui_button import Button
from constantes import *
import pygame


class FormMenuD(Form):
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
            x=self.w / 2 - 30,
            y=self.h - 50,
            w=60,
            h=50,
            color_background=None,
            color_border=None,
            image_background="images/gui/jungle/btn/menu.png",
            on_click=self.on_click_boton,
            on_click_param="form_menu_A",
            font="Verdana",
            font_size=30,
            font_color=C_WHITE,
        )
        self.lista_widget = [self.boton1]

        self.score = 0
        self.stars = 0
        self.last_game_results = None

    def on_click_boton(self, parametro):
        self.set_active(parametro)

    def set_score(self, score, results):
        self.score = score
        self.last_game_results = results

        if self.last_game_results == "win":
            if self.score > 2000:
                self.stars = 3
            elif self.score > 1000:
                self.stars = 2
            elif self.score > 500:
                self.stars = 1
            elif self.score < 500:
                self.stars = 0
        else:
            self.stars = 0

    def update(self, lista_eventos, keys, delta_ms):
        for aux_widget in self.lista_widget:
            aux_widget.update(lista_eventos)

    def draw(self):
        super().draw()
        for aux_widget in self.lista_widget:
            aux_widget.draw()

        image_header: pygame.surface.Surface = pygame.transform.scale(
            pygame.image.load(
                f"images/gui/jungle/results/header_{self.last_game_results}.png"
            ),
            (self.w, 150),
        ).convert_alpha()

        image_stars: pygame.surface.Surface = pygame.transform.scale(
            pygame.image.load(f"images/gui/jungle/results/star_{self.stars}.png"),
            (200, 100),
        ).convert_alpha()

        self.surface.blit(image_header, (0, 0))
        self.surface.blit(image_stars, (self.w / 2 - 100, self.h / 2 - 100))
