import pygame
from pygame.locals import *
from constantes import *
from gui_form import Form
from gui_button import Button
from gui_textbox import TextBox
from gui_progressbar import ProgressBar
from player import Player
from enemigo import Enemy
from plataforma import Plataform
from background import Background
from bullet import Bullet
from botin import Item
from auxiliar import Auxiliar


class FormGame(Form):
    def __init__(
        self,
        name,
        master_surface,
        w,
        h,
        color_border,
        active,
        level,
        event_cronometer,
        image_background,
    ):
        super().__init__(
            name, master_surface, w, h, image_background, color_border, active
        )

        self.name = name
        self.level = level
        self.completed_level = False

        self.event_timer = event_cronometer

        self.bullet_list = []
        self.plataform_list = Plataform.set_platforms(level)
        self.enemy_list: list = Enemy.set_enemies(level)
        self.items_list: list = Item.set_items(level)

        self.set_timer()

        # self.aux_items_list = []
        # self.aux_enemies_list = []

        # self.inactive_enemy_list: list = []
        # self.inactive_items_list: list = []

        # # --- GUI WIDGET ---

        self.boton1 = Button(
            master=self,
            x=10,
            y=10,
            w=140,
            h=50,
            color_background=None,
            color_border=None,
            image_background="images/gui/set_gui_01/Comic_Border/Buttons/Button_M_02.png",
            on_click=self.on_click_boton,
            on_click_param="form_menu_B",
            text="PAUSE",
            font="Verdana",
            font_size=30,
            font_color=C_WHITE,
        )

        self.pb_lives = ProgressBar(
            master=self,
            x=self.w - 230,
            y=self.h - 60,
            w=210,
            h=40,
            color_background=None,
            color_border=None,
            image_background="images/gui/set_gui_01/Comic_Border/Bars/Bar_Background01.png",
            image_progress="images/gui/set_gui_01/Comic_Border/Bars/Bar_Segment05.png",
            value=5,
            value_max=5,
        )
        self.widget_list = [self.boton1, self.pb_lives]

        # --- GAME ELEMNTS ---
        self.static_background = Background(x=0, y=0, width=w, height=h, path=level)
        self.set_player()

    def on_click_boton(self, parametro):
        self.set_active(parametro)

    def reload_components(self, delta_ms):
        pass
        # if not self.active:
        #     print("enemy list", self.enemy_list)
        #     self.enemy_list.extend(self.aux_enemies_list)
        #     print("enemy list desp", self.enemy_list)
        #     self.items_list.extend(self.aux_items_list)

    #     # self.tiempo_transcurrido_reload += delta_ms
    #     # if self.tiempo_transcurrido_reload >= self.reload_rate_ms:
    #     #     self.tiempo_transcurrido_reload = 0
    #     print(f"estado {self.name}", self.active)
    #         self.enemy_list: list = Enemy.set_enemies(self.level)
    #         self.items_list: list = Item.set_items(self.level)
    #         self.player_1.move_x = self.aux_x
    #         self.player_1.move_y = self.aux_y
    #         self.player_1.rect.x = self.aux_x
    #         self.player_1.rect.y = self.aux_y
    def set_player(self):
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
            interval_time_attack=300,
            on_shoot=self.shoot_player,
        )

    def set_timer(self):
        if self.level == "l1":
            self.timer = TIME_LEVEL_1

        elif self.level == "l2":
            self.timer = TIME_LEVEL_2

        elif self.level == "l3":
            self.timer = TIME_LEVEL_3

    def update_timer(self):
        self.timer_surface = Auxiliar.generate_text(
            "Arial", 20, f"Time left:{self.timer}", C_RED
        )

    def update_score(self):
        self.score_surface = Auxiliar.generate_text(
            "Arial", 20, f"Score:{self.player_1.score}", C_RED
        )

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

    def restore_level(self):
        self.items_list: list = Item.set_items(self.level)
        self.enemy_list: list = Enemy.set_enemies(self.level)
        self.set_player()
        self.set_timer()

    def finish_level(self):
        Form.set_active("form_menu_A")
        self.restore_level()

    def update(self, events_list, keys, delta_ms):
        print(
            self.timer, "timer"
        )  # ver como imprimir el timer cuando se despliega otro form para ver que es lo que sucefe que se ponen muhcos numeros

        if not self.items_list and not self.player_1.is_dead and self.timer >= 0:
            if not self.completed_level:
                self.levels_completed.append(self.level)
                self.completed_level = True

            self.finish_level()
        elif (
            self.player_1.is_dead
            and self.player_1.finish_dead_animation
            or self.timer <= 0
        ):
            self.finish_level()

        if self.active:
            for event in events_list:
                if event.type == self.event_timer:
                    self.timer -= 1
        # else:
        #     self.timer = 0

        for aux_widget in self.widget_list:
            aux_widget.update(events_list)

        for bullet_element in self.bullet_list:
            bullet_element.update(
                delta_ms, self.plataform_list, self.enemy_list, self.player_1
            )

        for item in self.items_list:
            if not item.is_active:
                self.items_list.remove(item)

            item.update(delta_ms, self.player_1)

        for enemy_element in self.enemy_list:
            if enemy_element.finish_dead_animation:
                self.enemy_list.remove(enemy_element)

            enemy_element.update(delta_ms, self.plataform_list, self.player_1)

        self.player_1.events(delta_ms, keys, self.enemy_list)
        self.player_1.update(delta_ms, self.plataform_list)
        self.pb_lives.value = self.player_1.lives

        self.update_timer()
        self.update_score()

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

        self.master_surface.blit(
            self.timer_surface, (ANCHO_VENTANA - 120, ALTO_VENTANA - 85)
        )
        self.master_surface.blit(
            self.score_surface, (ANCHO_VENTANA - 220, ALTO_VENTANA - 85)
        )
