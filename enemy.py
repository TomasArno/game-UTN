import pygame
from constants import *
from auxiliar import Auxiliar
from player import Player


class Enemy:
    def __init__(
        self,
        character,
        x,
        speed_walk,
        speed_run,
        gravity,
        frame_rate_ms,
    ) -> None:
        self.stay_r = Auxiliar.getSurfaceFromSpriteSheet(
            Auxiliar.getSpritesOfCharacter(character)["stay"], 9, 1, True
        )

        self.stay_l = Auxiliar.getSurfaceFromSpriteSheet(
            Auxiliar.getSpritesOfCharacter(character)["stay"], 9, 1
        )

        self.walk_r = Auxiliar.getSurfaceFromSpriteSheet(
            Auxiliar.getSpritesOfCharacter(character)["walk"], 16, 1, True
        )

        self.walk_l = Auxiliar.getSurfaceFromSpriteSheet(
            Auxiliar.getSpritesOfCharacter(character)["walk"], 16, 1
        )

        self.run_r = Auxiliar.getSurfaceFromSpriteSheet(
            Auxiliar.getSpritesOfCharacter(character)["run"], 12, 1, True
        )

        self.run_l = Auxiliar.getSurfaceFromSpriteSheet(
            Auxiliar.getSpritesOfCharacter(character)["run"], 12, 1
        )

        self.dead_r = Auxiliar.getSurfaceFromSpriteSheet(
            Auxiliar.getSpritesOfCharacter(character)["dead"], 7, 1, True
        )

        self.dead_l = Auxiliar.getSurfaceFromSpriteSheet(
            Auxiliar.getSpritesOfCharacter(character)["dead"], 7, 1
        )

        self.animation = self.stay_r
        self.frame = 0
        self.image = self.animation[self.frame]
        self.rect: pygame.Rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = GROUND_LEVEL
        self.move_x = 0
        self.speed_walk = speed_walk
        self.speed_run = speed_run
        self.gravity = gravity
        self.time_elapsed_ms = 0
        self.view_direction = VIEW_DIRECTION_R
        self.frame_rate_ms = frame_rate_ms
        self.rect_top_collition = pygame.Rect(
            self.rect.x + self.rect.w / 9, self.rect.y, self.rect.w / 1.2, 2
        )
        self.is_dead = False
        self.dead_flag = False
        self.finish_dead_animation = False
        self.run()

    def stay(self):
        if self.animation != self.stay_l and self.animation != self.stay_r:
            if self.view_direction:
                self.animation = self.stay_r
            else:
                self.animation = self.stay_l

            self.move_x = 0
            self.frame = 0

    def walk(self):
        if self.animation != self.walk_l and self.animation != self.walk_r:
            self.frame = 0

            if self.view_direction:
                self.move_x = self.speed_walk
                self.animation = self.walk_r
            else:
                self.move_x = -self.speed_walk
                self.animation = self.walk_l

    def run(self):
        if self.animation != self.walk_l and self.animation != self.walk_r:
            self.frame = 0

            if self.view_direction:
                self.move_x = self.speed_run
                self.animation = self.run_r
            else:
                self.move_x = -self.speed_run
                self.animation = self.run_l

    def dead(self):
        if not self.dead_flag:
            self.dead_flag = True
            self.frame = 0

            if self.view_direction:
                self.animation = self.dead_r
            else:
                self.animation = self.dead_l

    def collide_player(self, player):
        if self.rect_top_collition.colliderect(player.rect_bottom_collition):
            return True

    def add_x(self, value):
        self.rect.x += value
        self.rect_top_collition.x += value

    def update_moves(self, delta_ms, platform_list, player):
        self.time_elapsed_ms += delta_ms

        if self.time_elapsed_ms >= self.frame_rate_ms:
            self.time_elapsed_ms = 0

            if self.collide_player(player):
                self.is_dead = True

            if not DEBUG:
                if not self.is_dead:
                    if self.rect.x >= ANCHO_VENTANA:
                        self.view_direction = False
                        self.run()

                    elif self.rect.x <= 0:
                        self.view_direction = True
                        self.run()
                else:
                    self.dead()
                    self.rect.x = 0  # ver porque seguia corriendo
                    self.rect.y = 0
            else:
                self.stay()

            self.add_x(self.move_x)

    def update_animations(self, delta_ms):
        self.time_elapsed_ms += delta_ms

        if self.time_elapsed_ms >= self.frame_rate_ms:
            self.time_elapsed_ms = 0
            if self.frame < len(self.animation) - 1:
                self.frame += 1
            else:
                if self.is_dead:
                    self.finish_dead_animation = True

                self.frame = 0

    def update(self, delta_ms, platform_list, player):
        self.update_moves(delta_ms, platform_list, player)
        self.update_animations(delta_ms)

    def render(self, screen):
        if DEBUG:
            pygame.draw.rect(screen, RED, self.rect)
            pygame.draw.rect(screen, GREEN, self.rect_top_collition)

        if not self.finish_dead_animation:
            self.image = self.animation[self.frame]
            screen.blit(self.image, self.rect)
        else:
            pygame.draw.rect(screen, RED, self.rect)  # el rect del enemigo sigue
