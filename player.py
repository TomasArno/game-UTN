import pygame
from constantes import *
from auxiliar import Auxiliar
from bullet import Bullet


class Player:
    def __init__(
        self,
        x,
        y,
        speed_walk,
        speed_run,
        gravity,
        jump_power,
        frame_rate_ms,
        move_rate_ms,
        jump_height,
        p_scale=1,
        interval_time_jump=100,
        interval_time_attack=100,
    ) -> None:
        """
        self.walk_r = Auxiliar.getSurfaceFromSpriteSheet("images/caracters/stink/walk.png",15,1,scale=p_scale)[:12]
        """

        self.stay_r = Auxiliar.getSurfaceFromSeparateFiles(
            "images/caracters/players/cowgirl/Idle ({0}).png",
            1,
            10,
            flip=False,
            scale=p_scale,
        )
        self.stay_l = Auxiliar.getSurfaceFromSeparateFiles(
            "images/caracters/players/cowgirl/Idle ({0}).png",
            1,
            10,
            flip=True,
            scale=p_scale,
        )
        self.jump_r = Auxiliar.getSurfaceFromSeparateFiles(
            "images/caracters/players/cowgirl/Jump ({0}).png",
            1,
            10,
            flip=False,
            scale=p_scale,
        )
        self.jump_l = Auxiliar.getSurfaceFromSeparateFiles(
            "images/caracters/players/cowgirl/Jump ({0}).png",
            1,
            10,
            flip=True,
            scale=p_scale,
        )
        self.walk_r = Auxiliar.getSurfaceFromSeparateFiles(
            "images/caracters/players/cowgirl/Run ({0}).png",
            1,
            8,
            flip=False,
            scale=p_scale,
        )
        self.walk_l = Auxiliar.getSurfaceFromSeparateFiles(
            "images/caracters/players/cowgirl/Run ({0}).png",
            1,
            8,
            flip=True,
            scale=p_scale,
        )
        self.shoot_r = Auxiliar.getSurfaceFromSeparateFiles(
            "images/caracters/players/cowgirl/Shoot ({0}).png",
            1,
            3,
            flip=False,
            scale=p_scale,
            repeat_frame=2,
        )
        self.shoot_l = Auxiliar.getSurfaceFromSeparateFiles(
            "images/caracters/players/cowgirl/Shoot ({0}).png",
            1,
            3,
            flip=True,
            scale=p_scale,
            repeat_frame=2,
        )
        self.knife_r = Auxiliar.getSurfaceFromSeparateFiles(
            "images/caracters/players/cowgirl/Melee ({0}).png",
            1,
            7,
            flip=False,
            scale=p_scale,
            repeat_frame=1,
        )
        self.knife_l = Auxiliar.getSurfaceFromSeparateFiles(
            "images/caracters/players/cowgirl/Melee ({0}).png",
            1,
            7,
            flip=True,
            scale=p_scale,
            repeat_frame=1,
        )
        self.dead_r = Auxiliar.getSurfaceFromSeparateFiles(
            "images/caracters/players/cowgirl/Dead ({0}).png",
            1,
            10,
            flip=False,
            scale=p_scale,
            repeat_frame=1,
        )
        self.dead_l = Auxiliar.getSurfaceFromSeparateFiles(
            "images/caracters/players/cowgirl/Dead ({0}).png",
            1,
            10,
            flip=True,
            scale=p_scale,
            repeat_frame=1,
        )

        self.frame = 0
        self.animation = self.stay_r
        self.image = self.animation[self.frame]
        self.direction = DIRECTION_R
        self.lives = 5
        self.score = 0
        self.move_x = 0
        self.move_y = 0
        self.speed_walk = speed_walk
        self.speed_run = speed_run
        self.gravity = gravity
        self.jump_power = jump_power
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.collition_rect = pygame.Rect(
            x + self.rect.width / 3, y, self.rect.width / 3, self.rect.height
        )
        self.collition_rect_knife_r = pygame.Rect(
            self.collition_rect.x + self.collition_rect.width,
            y + self.rect.h / 4,
            20,
            self.rect.height / 2,
        )
        self.collition_rect_knife_l = pygame.Rect(
            self.collition_rect.x - 25, y + self.rect.h / 4, 25, self.rect.height / 2
        )
        self.ground_collition_rect = pygame.Rect(self.collition_rect)
        self.ground_collition_rect.height = GROUND_COLLIDE_H
        self.ground_collition_rect.y = y + self.rect.height - GROUND_COLLIDE_H

        self.finish_dead_animation = False
        self.is_dead = False

        self.is_jump = False
        self.is_fall = False
        self.is_knife = False
        self.is_shoot = False

        self.y_start_jump = 0
        self.jump_height = jump_height

        self.frame_rate_ms = frame_rate_ms
        self.time_transcurrido_animation = 0
        self.move_rate_ms = move_rate_ms
        self.time_transcurrido_move = 0
        self.time_transcurrido = 0

        self.time_last_attack = 0
        self.time_last_jump = 0
        self.interval_time_jump = interval_time_jump
        self.interval_time_attack = interval_time_attack

    def walk(self, direction):
        if self.direction != direction or (
            self.animation != self.walk_r and self.animation != self.walk_l
        ):
            self.frame = 0
            self.direction = direction
            if direction == DIRECTION_R:
                self.move_x = self.speed_walk
                self.animation = self.walk_r
            else:
                self.move_x = -self.speed_walk
                self.animation = self.walk_l

    def shoot(self, on_off=True, bullet_list=None):
        self.is_shoot = on_off
        if self.is_shoot:
            self.frame = 0
            if self.direction == DIRECTION_R:
                self.animation = self.shoot_r
            else:
                self.animation = self.shoot_l

            self.shoot_player(bullet_list)

    def knife(self, on_off=True, enemy_list=None):
        self.is_knife = on_off
        if on_off == True and self.is_jump == False and self.is_fall == False:
            if self.animation != self.knife_r and self.animation != self.knife_l:
                self.frame = 0
                if self.direction == DIRECTION_R:
                    self.animation = self.knife_r
                else:
                    self.animation = self.knife_l

                enemy = self.check_collition_knife(enemy_list)
                if enemy:
                    enemy.receive_attack("knife", self)

    def jump(self, on_off=True):
        if on_off and self.is_jump == False and self.is_fall == False:
            self.y_start_jump = self.rect.y
            if self.direction == DIRECTION_R:
                self.move_x = int(self.move_x)
                self.move_y = -self.jump_power
                self.animation = self.jump_r
            else:
                self.move_x = int(self.move_x)
                self.move_y = -self.jump_power
                self.animation = self.jump_l
            self.frame = 0
            self.is_jump = True

        if not on_off:
            self.is_jump = False
            self.stay()

    def stay(self):
        if not self.is_knife and not self.is_shoot:
            if self.animation != self.stay_r and self.animation != self.stay_l:
                if self.direction == DIRECTION_R:
                    self.animation = self.stay_r
                else:
                    self.animation = self.stay_l
                self.move_x = 0
                self.move_y = 0
                self.frame = 0

    def dead(self):
        if self.animation != self.dead_r and self.animation != self.dead_l:
            if self.direction == DIRECTION_R:
                self.animation = self.dead_r
            else:
                self.animation = self.dead_l

            self.move_x = 0
            self.move_y = 0
            self.frame = 0

    def check_collition_knife(self, enemy_list):
        if enemy_list:
            for enemy in enemy_list:
                if (
                    self.collition_rect_knife_l.colliderect(enemy.collition_rect)
                    or self.collition_rect_knife_r.colliderect(enemy.collition_rect)
                    and enemy.is_active
                ):
                    return enemy
                else:
                    return None

    def shoot_player(self, bullet_list):
        bullet_end_x = None
        if self.direction == 0:
            bullet_end_x = 0
        else:
            bullet_end_x = ANCHO_VENTANA

        bullet_list.append(
            Bullet(
                self,
                self.rect.centerx,
                self.rect.centery,
                bullet_end_x,
                self.rect.centery,
                20,
                path="images/gui/set_gui_01/Comic_Border/Bars/Bar_Segment05.png",
                frame_rate_ms=100,
                move_rate_ms=20,
                width=5,
                height=5,
            )
        )

    def receive_attack(self):
        self.lives -= 1
        self.score -= 50
        self.check_life()

    def grab_item(self):
        self.lives += 1
        self.score += 50
        self.check_life()

    def check_life(self):
        if self.lives <= 0:
            self.is_dead = True
        elif self.lives > 5:
            self.lives = 5

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

    def change_x(self, delta_x):
        self.rect.x += delta_x
        self.collition_rect.x += delta_x
        self.ground_collition_rect.x += delta_x
        self.collition_rect_knife_r.x += delta_x
        self.collition_rect_knife_l.x += delta_x

    def change_y(self, delta_y):
        self.rect.y += delta_y
        self.collition_rect.y += delta_y
        self.ground_collition_rect.y += delta_y
        self.collition_rect_knife_r.y += delta_y
        self.collition_rect_knife_l.y += delta_y

    def do_movement(self, delta_ms, plataform_list):
        self.time_transcurrido_move += delta_ms
        if self.time_transcurrido_move >= self.move_rate_ms:
            self.time_transcurrido_move = 0

            if not self.is_dead:
                if (
                    abs(self.y_start_jump - self.rect.y) > self.jump_height
                    and self.is_jump
                ):
                    self.move_y = 0

                self.change_x(self.move_x)
                self.change_y(self.move_y)

                if not self.is_on_plataform(plataform_list):
                    if self.move_y == 0:
                        self.is_fall = True
                        self.change_y(self.gravity)
                else:
                    if self.is_jump:
                        self.jump(False)
                    self.is_fall = False

    def do_animation(self, delta_ms):
        self.time_transcurrido_animation += delta_ms
        if self.time_transcurrido_animation >= self.frame_rate_ms:
            self.time_transcurrido_animation = 0
            if self.frame < len(self.animation) - 1:
                self.frame += 1
            else:
                self.frame = 0

                if self.is_dead:
                    self.finish_dead_animation = True

    def update(self, delta_ms, plataform_list):
        if not self.finish_dead_animation:
            self.do_movement(delta_ms, plataform_list)
            self.do_animation(delta_ms)

    def draw(self, screen):
        if DEBUG:
            pygame.draw.rect(screen, color=(255, 0, 0), rect=self.collition_rect)
            pygame.draw.rect(
                screen, color=(255, 255, 0), rect=self.ground_collition_rect
            )
            pygame.draw.rect(
                screen, color=(0, 0, 255), rect=self.collition_rect_knife_r
            )
            pygame.draw.rect(
                screen, color=(0, 0, 255), rect=self.collition_rect_knife_l
            )

        if not self.finish_dead_animation:
            self.image = self.animation[self.frame]
            screen.blit(self.image, self.rect)

    def events(self, delta_ms, keys, enemy_list, bullet_list):
        self.time_transcurrido += delta_ms

        if self.is_dead:
            self.dead()

        else:
            if (
                keys[pygame.K_LEFT]
                and not keys[pygame.K_RIGHT]
                and not keys[pygame.K_s]
                and not keys[pygame.K_a]
            ):
                self.walk(DIRECTION_L)

            if (
                not keys[pygame.K_LEFT]
                and keys[pygame.K_RIGHT]
                and not keys[pygame.K_s]
                and not keys[pygame.K_a]
            ):
                self.walk(DIRECTION_R)

            if (
                not keys[pygame.K_LEFT]
                and not keys[pygame.K_RIGHT]
                and not keys[pygame.K_SPACE]
            ):
                self.stay()
            if (
                keys[pygame.K_LEFT]
                and keys[pygame.K_RIGHT]
                and not keys[pygame.K_SPACE]
            ):
                self.stay()

            if keys[pygame.K_SPACE]:
                if (
                    self.time_transcurrido - self.time_last_jump
                ) > self.interval_time_jump:
                    self.jump(on_off=True)
                    self.time_last_jump = self.time_transcurrido

            if not keys[pygame.K_s]:
                self.shoot(on_off=False)

            if not keys[pygame.K_a]:
                self.knife(on_off=False)

            if (
                keys[pygame.K_s]
                and not keys[pygame.K_a]
                and not keys[pygame.K_LEFT]
                and not keys[pygame.K_RIGHT]
            ):
                if (
                    self.time_transcurrido - self.time_last_attack
                ) > self.interval_time_attack:
                    self.shoot(bullet_list=bullet_list)
                    self.time_last_attack = self.time_transcurrido

            if (
                keys[pygame.K_a]
                and not keys[pygame.K_s]
                and not keys[pygame.K_LEFT]
                and not keys[pygame.K_RIGHT]
            ):
                if (
                    self.time_transcurrido - self.time_last_attack
                ) > self.interval_time_attack:
                    self.knife(enemy_list=enemy_list)
                    self.time_last_attack = self.time_transcurrido
