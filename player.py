import pygame
from constants import *
from auxiliar import Auxiliar


class Player:
    def __init__(
        self,
        character,
        x,
        y,
        speed_walk,
        speed_run,
        gravity,
        jump_velocity,
        jump_high,
        frame_rate_movements_ms,
        frame_rate_animation_ms,
    ) -> None:
        self.stay_r = Auxiliar.getSurfaceFromSpriteSheet(
            Auxiliar.getSpritesOfCharacter(character)["stay"], 11, 1
        )

        self.stay_l = Auxiliar.getSurfaceFromSpriteSheet(
            Auxiliar.getSpritesOfCharacter(character)["stay"], 11, 1, True
        )

        self.walk_r = Auxiliar.getSurfaceFromSpriteSheet(
            Auxiliar.getSpritesOfCharacter(character)["walk"], 12, 1
        )

        self.walk_l = Auxiliar.getSurfaceFromSpriteSheet(
            Auxiliar.getSpritesOfCharacter(character)["walk"], 12, 1, True
        )

        self.jump_r = Auxiliar.getSurfaceFromSpriteSheet(
            Auxiliar.getSpritesOfCharacter(character)["jump"], 1, 1
        )

        self.jump_l = Auxiliar.getSurfaceFromSpriteSheet(
            Auxiliar.getSpritesOfCharacter(character)["jump"], 1, 1, True
        )

        self.dead_r = Auxiliar.getSurfaceFromSpriteSheet(
            Auxiliar.getSpritesOfCharacter(character)["dead"], 7, 1, True
        )

        self.dead_l = Auxiliar.getSurfaceFromSpriteSheet(
            Auxiliar.getSpritesOfCharacter(character)["dead"], 7, 1
        )
        self.frame: int = 0
        self.animation = self.stay_r
        self.image = self.animation[self.frame]
        self.rect: pygame.Rect = self.image.get_rect()
        self.rect.x: int = x
        self.rect.y: int = y
        self.move_x = 0
        self.move_y = 0
        self.speed_walk: int = speed_walk
        self.speed_run: int = speed_run
        self.gravity: int = gravity
        self.time_elapsed_ms = 0
        self.view_direction: bool = VIEW_DIRECTION_R
        self.frame_rate_movements_ms = frame_rate_movements_ms
        self.frame_rate_animation_ms = frame_rate_animation_ms
        self.lives = 3
        self.jump_velocity = jump_velocity
        self.jump_high = jump_high
        self.jump_starting_pos_y = 0
        self.is_jump = False
        self.rect_bottom_collition = pygame.Rect(
            self.rect.x + self.rect.w / 4,
            self.rect.y + self.rect.h - 10,
            self.rect.w / 2,
            10,
        )

        self.is_dead = False
        self.dead_flag = False
        self.finish_dead_animation = False

    # @property ANIMATION RECIBE LISTA Y DEBE SER UNA SUEPRFICIE PARA FUNCIONAR

    # def animation(self):
    #     return self.__animation

    # @animation.setter
    # def animation(self, animation):
    #     scaled_animation = pygame.transform.scale(animation, (50, 50))
    #     self.__animation = scaled_animation

    def stay(self):
        if self.animation != self.stay_l and self.animation != self.stay_r:
            if self.view_direction:
                self.animation = self.stay_r
            else:
                self.animation = self.stay_l

            self.move_x = 0
            self.move_y = 0
            self.frame = 0

    def walk(self, view_direction):
        if self.view_direction != view_direction or (
            self.animation != self.walk_l and self.animation != self.walk_r
        ):
            self.frame = 0
            self.view_direction = view_direction

            if self.view_direction:
                self.move_x = self.speed_walk
                self.animation = self.walk_r
            else:
                self.move_x = -self.speed_walk
                self.animation = self.walk_l

    def jump(self, jump):
        if jump and not self.is_jump:
            self.jump_starting_pos_y = self.rect.y
            self.is_jump = True
            self.frame = 0

            if self.view_direction:
                self.animation = self.jump_r
                self.move_x = self.speed_walk
            else:
                self.animation = self.jump_l
                self.move_x = -self.speed_walk

            self.move_y = -self.jump_velocity

        elif not jump:
            self.is_jump = False
            self.stay()

    def dead(self):
        if not self.dead_flag:
            print("dead")
            self.dead_flag = True
            self.frame = 0

            if self.view_direction:
                self.animation = self.dead_r
            else:
                self.animation = self.dead_l

    def events(
        self, keys_pressed, delta_ms
    ):  # ver como hacer desaparecer al player tras morir
        if self.is_dead:
            self.dead()
        else:
            if keys_pressed[pygame.K_SPACE]:
                self.jump(True)

            elif keys_pressed[pygame.K_RIGHT] and not keys_pressed[pygame.K_LEFT]:
                self.walk(VIEW_DIRECTION_R)

            elif keys_pressed[pygame.K_LEFT] and not keys_pressed[pygame.K_RIGHT]:
                self.walk(VIEW_DIRECTION_L)

            elif (
                keys_pressed[pygame.K_LEFT]
                and keys_pressed[pygame.K_RIGHT]
                and not keys_pressed[pygame.K_SPACE]
                and not self.is_dead
            ):
                self.stay()

            elif (
                not keys_pressed[pygame.K_LEFT]
                and not keys_pressed[pygame.K_RIGHT]
                and not keys_pressed[pygame.K_SPACE]
                and not self.is_dead
            ):
                self.stay()

    def collide_platform(self, platforms: list):
        retorno = False
        if self.rect.y >= GROUND_LEVEL:
            return True
        else:
            for platform in platforms:
                if self.rect_bottom_collition.colliderect(
                    platform.rect_bottom_collition
                ):
                    return True
        return retorno

    def collide_enemy(self, enemies_list):
        for enemy in enemies_list:
            if self.rect.colliderect(enemy.rect) and not self.rect.colliderect(
                enemy.rect_top_collition
            ):
                return True

    def add_x(self, value):
        self.rect.x += value
        self.rect_bottom_collition.x += value

    def add_y(self, value):
        self.rect.y += value
        self.rect_bottom_collition.y += value

    def update_moves(self, delta_ms, platform_list, enemies_list):
        self.time_elapsed_ms += delta_ms

        if self.time_elapsed_ms >= self.frame_rate_movements_ms:
            self.time_elapsed_ms = 0

            if (
                abs(self.jump_starting_pos_y - self.rect.y) > self.jump_high
                and self.is_jump
            ):
                self.move_y = 0

            self.add_x(self.move_x)
            self.add_y(self.move_y)

            if self.collide_enemy(enemies_list):
                self.is_dead = True

            if not self.collide_platform(platform_list) and self.rect.y < GROUND_LEVEL:
                self.add_y(self.gravity)

            elif self.is_jump:
                self.jump(False)

    def update_animations(
        self, delta_ms
    ):  # preguntar porque se queda congelado si le subo el animation rate_ms
        self.time_elapsed_ms += delta_ms

        if self.time_elapsed_ms >= self.frame_rate_animation_ms:
            self.time_elapsed_ms = 0
            if self.frame < len(self.animation) - 1:
                self.frame += 1
            else:
                if self.is_dead:
                    self.finish_dead_animation = True
                self.frame = 0

    def update(self, delta_ms, platform_list, enemies_list):
        self.update_moves(delta_ms, platform_list, enemies_list)
        self.update_animations(delta_ms)

    def render(self, screen):
        if DEBUG:
            pygame.draw.rect(screen, RED, self.rect)
            pygame.draw.rect(screen, GREEN, self.rect_bottom_collition)

        if not self.finish_dead_animation:
            self.image = self.animation[self.frame]
            screen.blit(self.image, self.rect)
