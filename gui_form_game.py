from pygame.locals import *
from constantes import *
from gui_form import Form
from gui_button import Button
from gui_progressbar import ProgressBar
from player import Player
from enemigo import Enemy
from plataforma import Plataform
from background import Background
from botin import Item
from auxiliar import Auxiliar
from gui_form_menu_score import FormMenuScore


class FormGame(Form):
    game_completed = False
    flag_completed = False

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

        # --- GUI WIDGET ---

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
        self.total_score = 0
        self.level_score = 0
        self.set_player()
        self.set_enemies()
        self.set_items()
        self.set_timer()

        self.form_B = self.get_form("form_menu_B")
        self.form_D = self.get_form("form_menu_D")
        self.form_score: FormMenuScore = self.get_form("form_menu_score")

    def on_click_boton(self, parametro):
        self.set_active(parametro)

    def set_enemies(self):
        self.enemy_list: list = Enemy.set_enemies(self.level)

    def set_items(self):
        self.items_list: list = Item.set_items(self.level)

    def set_timer(self):
        if self.level == "l1":
            self.timer = TIME_LEVEL_1

        elif self.level == "l2":
            self.timer = TIME_LEVEL_2

        elif self.level == "l3":
            self.timer = TIME_LEVEL_3

    def set_player(self):
        self.player_1 = Player(
            x=0,
            y=500,
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
        )

    def update_timer(self):
        self.timer_surface = Auxiliar.generate_text(
            "Arial", 20, f"Time left:{self.timer}", C_RED
        )

    def update_score(self):
        self.score_surface = Auxiliar.generate_text(
            "Arial", 20, f"Score:{self.player_1.score}", C_RED
        )

    def restore_level(self):
        self.set_player()
        self.set_enemies()
        self.set_items()
        self.set_timer()

    def finish_level(self, results):
        self.level_score = self.player_1.score
        self.form_D.set_score(self.level_score, results)
        Form.set_active("form_menu_D")
        self.restore_level()

    def check_game_completed(self):
        if (
            "l1" in Form.levels_completed
            and "l2" in Form.levels_completed
            and "l3" in Form.levels_completed
        ):
            FormGame.game_completed = True

    def set_score_db(self):
        self.form_score.insert_row(Form.players_name, self.level_score)

    def update(self, events_list, keys, delta_ms):
        self.form_B.set_last_form_played(self.name)

        if not self.items_list and not self.player_1.is_dead and self.timer >= 0:
            if not self.completed_level:
                self.completed_level = True
                self.total_score += self.player_1.score
                Form.levels_completed.append(self.level)
            self.results = "win"
            self.finish_level(self.results)
        elif (
            self.player_1.is_dead
            and self.player_1.finish_dead_animation
            or self.timer <= 0
        ):
            self.results = "lose"
            self.finish_level(self.results)

        self.check_game_completed()

        if FormGame.game_completed and not FormGame.flag_completed:
            print("entre a set score db")
            FormGame.flag_completed = True
            self.set_score_db()

        for event in events_list:
            if event.type == self.event_timer:
                self.timer -= 1

        if self.active:
            self.update_timer()
            self.update_score()

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
            if enemy_element.finish_dead_animation and not enemy_element.is_active:
                self.enemy_list.remove(enemy_element)

            enemy_element.update(delta_ms, self.plataform_list, self.player_1)

        self.player_1.events(delta_ms, keys, self.enemy_list, self.bullet_list)
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

        self.master_surface.blit(
            self.timer_surface, (ANCHO_VENTANA - 120, ALTO_VENTANA - 85)
        )
        self.master_surface.blit(
            self.score_surface, (ANCHO_VENTANA - 225, ALTO_VENTANA - 85)
        )
