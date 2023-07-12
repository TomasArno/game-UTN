from player import *
from constantes import *
from auxiliar import Auxiliar


class Enemy:
    def __init__(
        self,
        x,
        y,
        speed_walk,
        speed_run,
        gravity,
        frame_rate_ms,
        move_rate_ms,
        p_scale=1,
        is_active=True,
    ) -> None:
        self.walk_r = Auxiliar.getSurfaceFromSeparateFiles(
            "images/caracters/enemies/ork_sword/WALK/WALK_00{0}.png",
            0,
            7,
            scale=p_scale,
        )
        self.walk_l = Auxiliar.getSurfaceFromSeparateFiles(
            "images/caracters/enemies/ork_sword/WALK/WALK_00{0}.png",
            0,
            7,
            flip=True,
            scale=p_scale,
        )
        self.stay_r = Auxiliar.getSurfaceFromSeparateFiles(
            "images/caracters/enemies/ork_sword/IDLE/IDLE_00{0}.png",
            0,
            7,
            scale=p_scale,
        )
        self.stay_l = Auxiliar.getSurfaceFromSeparateFiles(
            "images/caracters/enemies/ork_sword/IDLE/IDLE_00{0}.png",
            0,
            7,
            flip=True,
            scale=p_scale,
        )
        self.die_r = Auxiliar.getSurfaceFromSeparateFiles(
            "images/caracters/enemies/ork_sword/DIE/DIE_00{0}.png",
            0,
            7,
            scale=p_scale,
        )
        self.die_l = Auxiliar.getSurfaceFromSeparateFiles(
            "images/caracters/enemies/ork_sword/DIE/DIE_00{0}.png",
            0,
            7,
            flip=True,
            scale=p_scale,
        )

        self.attack_r = Auxiliar.getSurfaceFromSeparateFiles(
            "images/caracters/enemies/ork_sword/ATTAK/ATTAK_00{0}.png",
            0,
            7,
            scale=p_scale,
        )

        self.attack_l = Auxiliar.getSurfaceFromSeparateFiles(
            "images/caracters/enemies/ork_sword/ATTAK/ATTAK_00{0}.png",
            0,
            7,
            flip=True,
            scale=p_scale,
        )

        self.contador = 0
        self.frame = 0
        self.lives = 5
        self.score = 0
        self.move_x = 0
        self.move_y = 0
        self.speed_walk = speed_walk
        self.speed_run = speed_run
        self.gravity = gravity
        self.animation = self.stay_r
        self.direction = DIRECTION_R
        self.image = self.animation[self.frame]
        self.rect: pygame.Rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.collition_rect = pygame.Rect(
            x + self.rect.width / 4, y, self.rect.width / 2, self.rect.height
        )
        self.ground_collition_rect = pygame.Rect(self.collition_rect)
        self.ground_collition_rect.height = GROUND_COLLIDE_H
        self.ground_collition_rect.y = y + self.rect.height - GROUND_COLLIDE_H

        self.is_active = is_active
        self.is_jump = False
        self.is_fall = False
        self.is_shoot = False
        self.is_knife = False

        self.finish_dead_animation = False

        self.tiempo_transcurrido_animation = 0
        self.frame_rate_ms = frame_rate_ms
        self.tiempo_transcurrido_move = 0
        self.move_rate_ms = move_rate_ms
        self.y_start_jump = 0

        self.tiempo_transcurrido = 0
        self.tiempo_last_jump = 0

    def is_on_plataform(self, plataform_list):
        retorno = False

        if self.ground_collition_rect.bottom >= GROUND_LEVEL:
            retorno = True
        else:
            for plataforma in plataform_list:
                if self.ground_collition_rect.colliderect(
                    plataforma.ground_collition_rect
                ):
                    retorno = True
                    break
        return retorno

    def check_life(self):
        if self.lives <= 0:
            self.is_active = False

    def receive_attack(self, element, player):
        if element == "bullet":
            self.lives -= 2
            player.score += 100
        else:
            self.lives -= 1
            player.score += 200

    def check_view_direction(self):
        if self.direction == DIRECTION_L:
            return True
        else:
            return False

    def change_x(self, delta_x):
        self.rect.x += delta_x
        self.collition_rect.x += delta_x
        self.ground_collition_rect.x += delta_x

    def change_y(self, delta_y):
        self.rect.y += delta_y
        self.collition_rect.y += delta_y
        self.ground_collition_rect.y += delta_y

    def do_movement(self, delta_ms, plataform_list, player):
        self.tiempo_transcurrido_move += delta_ms

        if self.tiempo_transcurrido_move >= self.move_rate_ms:
            self.tiempo_transcurrido_move = 0
            self.check_life()

            if self.is_active:
                if not self.is_on_plataform(plataform_list):
                    if self.move_y == 0:
                        self.is_fall = True
                        self.change_y(self.gravity)

                else:
                    self.is_fall = False

                    if (
                        self.animation != self.attack_l
                        and self.animation != self.attack_r
                    ):
                        self.change_x(self.move_x)

                        if self.contador <= 50:
                            self.direction = DIRECTION_L
                            self.move_x = -self.speed_walk
                            self.animation = self.walk_l
                            self.contador += 1

                        elif self.contador <= 100:
                            self.direction = DIRECTION_R
                            self.move_x = self.speed_walk
                            self.animation = self.walk_r
                            self.contador += 1

                        else:
                            self.contador = 0

                    if self.collition_rect.colliderect(player.collition_rect):
                        if self.check_view_direction():
                            self.animation = self.attack_l
                        else:
                            self.animation = self.attack_r

                    else:
                        if self.check_view_direction():
                            self.animation = self.walk_l
                        else:
                            self.animation = self.walk_r

            elif self.animation != self.die_l and self.animation != self.die_r:
                if self.check_view_direction():
                    self.animation = self.die_l
                else:
                    self.animation = self.die_r

                self.frame = 0

    def do_animation(self, delta_ms, player):
        self.tiempo_transcurrido_animation += delta_ms
        if self.tiempo_transcurrido_animation >= self.frame_rate_ms:
            self.tiempo_transcurrido_animation = 0

            if self.frame < len(self.animation) - 1:
                self.frame += 1
            else:
                self.frame = 0

                if self.animation == self.attack_l or self.animation == self.attack_r:
                    player.receive_attack()

                if not self.is_active:
                    self.finish_dead_animation = True

    def update(self, delta_ms, plataform_list, player):
        if not self.finish_dead_animation:
            self.do_movement(delta_ms, plataform_list, player)
            self.do_animation(delta_ms, player)

    def draw(self, screen):
        if DEBUG:
            pygame.draw.rect(screen, color=(255, 255, 0), rect=self.rect)
            pygame.draw.rect(screen, color=(255, 0, 0), rect=self.collition_rect)

        self.image = self.animation[self.frame]
        screen.blit(self.image, self.rect)

    def set_enemies(level):
        level_enemies = Auxiliar.leer_json("config.json", "levels")[level]["enemies"]

        enemies_list = []

        for enemy in level_enemies:
            enemies_list.append(
                Enemy(
                    enemy["x"],
                    enemy["y"],
                    enemy["speed_walk"],
                    enemy["speed_run"],
                    enemy["gravity"],
                    enemy["frame_rate_ms"],
                    enemy["move_rate_ms"],
                    enemy["p_scale"],
                    enemy["is_active"],
                )
            )

        return enemies_list
