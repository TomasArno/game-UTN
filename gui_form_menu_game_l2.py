from pygame.locals import *
from constantes import *
from gui_form import Form
from gui_button import Button
from gui_textbox import TextBox
from gui_progressbar import ProgressBar
from player import Player
from enemigo import Enemy
from plataforma import Plataform
from botin import Item
from background import Background
from bullet import Bullet


class FormGameLevel2(Form):
    def __init__(
        self, name, master_surface, x, y, w, h, color_background, color_border, active
    ):
        super().__init__(
            name, master_surface, x, y, w, h, color_background, color_border, active
        )

        # --- GUI WIDGET ---
        self.boton1 = Button(
            master=self,
            x=0,
            y=0,
            w=140,
            h=50,
            color_background=None,
            color_border=None,
            image_background="images/gui/set_gui_01/Comic_Border/Buttons/Button_M_02.png",
            on_click=self.on_click_boton1,
            on_click_param="form_menu_B",
            text="BACK",
            font="Verdana",
            font_size=30,
            font_color=C_WHITE,
        )
        self.boton2 = Button(
            master=self,
            x=200,
            y=0,
            w=140,
            h=50,
            color_background=None,
            color_border=None,
            image_background="images/gui/set_gui_01/Comic_Border/Buttons/Button_M_02.png",
            on_click=self.on_click_boton1,
            on_click_param="form_menu_B",
            text="PAUSE",
            font="Verdana",
            font_size=30,
            font_color=C_WHITE,
        )

        self.pb_lives = ProgressBar(
            master=self,
            x=500,
            y=50,
            w=240,
            h=50,
            color_background=None,
            color_border=None,
            image_background="images/gui/set_gui_01/Comic_Border/Bars/Bar_Background01.png",
            image_progress="images/gui/set_gui_01/Comic_Border/Bars/Bar_Segment05.png",
            value=5,
            value_max=5,
        )
        self.widget_list = [self.boton1, self.boton2, self.pb_lives]

        # --- GAME ELEMNTS ---
        self.static_background = Background(
            x=0,
            y=0,
            width=w,
            height=h,
            path="l2",
        )

        self.player_1 = Player(
            x=0,
            y=400,
            speed_walk=10,
            speed_run=12,
            gravity=14,
            jump_power=30,
            frame_rate_ms=100,
            move_rate_ms=50,
            jump_height=140,
            p_scale=0.2,
            interval_time_jump=300,
            on_shoot=self.shoot_player,
        )

        self.enemy_list: list = Enemy.set_enemies("l2")
        self.plataform_list = Plataform.set_platforms("l2")
        self.items_list = Item.set_items("l2")
        self.bullet_list = []

    def on_click_boton1(self, parametro):
        self.set_active(parametro)

    def shoot_player(self, direction):
        bullet_end_x = None
        if direction == 0:
            bullet_end_x = 0
        else:
            bullet_end_x = ANCHO_VENTANA

        self.bullet_list.append(
            Bullet(
                self.player_1,
                self.player_1.rect.centerx,
                self.player_1.rect.centery,
                bullet_end_x,
                self.player_1.rect.centery,
                20,
                path="images/gui/set_gui_01/Comic_Border/Bars/Bar_Segment05.png",
                frame_rate_ms=100,
                move_rate_ms=20,
                width=5,
                height=5,
            )
        )

    def update(self, lista_eventos, keys, delta_ms):
        # self.current_time = self.start_form_time.tick()
        # self.current_time = (self.start_form_time - self.current_time) / 1000

        # if self.current_time == 20:
        #     self.terminar_juego()

        for aux_widget in self.widget_list:
            aux_widget.update(lista_eventos)

        for bullet_element in self.bullet_list:
            bullet_element.update(
                delta_ms, self.plataform_list, self.enemy_list, self.player_1
            )

        for item in self.items_list:
            if not item.is_active:
                self.items_list.remove(item)

            if not self.items_list:
                self.terminar_juego()

            item.update(delta_ms, self.player_1)

        for enemy_element in self.enemy_list:
            if not enemy_element.is_active:
                self.enemy_list.remove(enemy_element)

            enemy_element.update(delta_ms, self.plataform_list, self.player_1)

        self.player_1.events(delta_ms, keys)
        self.player_1.update(delta_ms, self.plataform_list)

        self.pb_lives.value = self.player_1.lives

    def draw(self):
        super().draw()
        self.static_background.draw(self.surface)

        for aux_widget in self.widget_list:
            aux_widget.draw()

        for plataforma in self.plataform_list:
            plataforma.draw(self.surface)

        for item in self.items_list:
            item.draw(self.surface)

        for enemy_element in self.enemy_list:
            enemy_element.draw(self.surface)

        self.player_1.draw(self.surface)

        for bullet_element in self.bullet_list:
            bullet_element.draw(self.surface)
