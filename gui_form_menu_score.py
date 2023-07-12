import pygame
from pygame.locals import *
from gui_form import Form
from gui_button import Button
from constantes import *
from auxiliar import Auxiliar
import sqlite3 as sql


class FormMenuScore(Form):
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
            y=self.h - 60,
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
        self.lista_widget = [
            self.boton1,
        ]

        self.text_y = 170
        self.data_score = None

    def on_click_boton(self, parametro):
        self.set_active(parametro)

    def create_table(self):
        with sql.connect("score.db") as conexion:
            try:
                sentencia = """ create  table score
                                (
                                    nombre text,
                                    score integer
                                )
                            """
                cursor = conexion.cursor()
                cursor.execute(sentencia)
                conexion.commit()
                print("Se creo la tabla score")
            except sql.OperationalError:
                print("La tabla ya existe")

    def insert_row(self, nombre, score):
        with sql.connect("score.db") as conexion:
            try:
                cursor = conexion.cursor()
                sentencia = f"insert into score values ('{nombre}',{score})"
                cursor.execute(sentencia)
                conexion.commit()
            except:
                print("Error")

    def read_rows(self):
        with sql.connect("score.db") as conexion:
            try:
                cursor = conexion.cursor()
                cursor.execute("select * from score order by score desc")
                data = cursor.fetchall()
                conexion.commit()
                return data
            except:
                print("Error")

    def show_text_and_score(self, name, score):
        font_name = Auxiliar.generate_text("Arial", 35, f"{name}", C_BLACK)
        font_score = Auxiliar.generate_text("Arial", 35, f"{score}", C_BLACK)

        self.surface.blit(font_name, (75, self.text_y))
        self.surface.blit(font_score, (320, self.text_y))

        self.text_y += font_name.get_height()

    def update(self, lista_eventos, keys, delta_ms):
        for aux_widget in self.lista_widget:
            aux_widget.update(lista_eventos)

        if self.data_score != self.read_rows():
            self.data_score = self.read_rows()
            if self.data_score:
                for score in self.data_score:
                    self.show_text_and_score(name=score[0], score=score[1])

    def draw(self):
        super().draw()
        for aux_widget in self.lista_widget:
            aux_widget.draw()

        image_header = pygame.transform.scale(
            pygame.image.load("images/gui/jungle/rating/header.png"),
            (self.w, 150),
        ).convert_alpha()

        scroll_top = pygame.transform.scale(
            pygame.image.load("images/gui/jungle/rating/scroll.png"),
            (self.w - 100, 10),
        ).convert_alpha()

        scroll_left = pygame.transform.scale(
            pygame.image.load("images/gui/jungle/rating/scroll.png"),
            (10, self.h - 230),
        ).convert_alpha()

        self.surface.blit(image_header, (0, 0))
        self.surface.blit(scroll_left, (37, 150))
        self.surface.blit(scroll_left, (237, 150))
        self.surface.blit(scroll_left, (437, 150))
        self.surface.blit(
            scroll_top, (self.w / 2 - scroll_top.get_width() / 2 - 13, 150)
        )
