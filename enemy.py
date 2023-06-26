import pygame
from constants import *
from auxiliar import Auxiliar

# from plataforma import Platform


class Enemy:
    def __init__(
        self,
        character,
        x,
        y,
        speed_walk,
        speed_run,
        gravity,
        frame_rate_ms,
    ) -> None:
        self.stay_r = Auxiliar.getSurfaceFromSpriteSheet(
            Auxiliar.getSpritesOfCharacter(character)["stay"],
            9,
            1,
            True,
        )

        self.stay_l = Auxiliar.getSurfaceFromSpriteSheet(
            Auxiliar.getSpritesOfCharacter(character)["stay"],
            9,
            1,
        )

        self.walk_r = Auxiliar.getSurfaceFromSpriteSheet(
            Auxiliar.getSpritesOfCharacter(character)["walk"],
            16,
            1,
            True,
        )

        self.walk_l = Auxiliar.getSurfaceFromSpriteSheet(
            Auxiliar.getSpritesOfCharacter(character)["walk"],
            16,
            1,
        )

        self.run_r = Auxiliar.getSurfaceFromSpriteSheet(
            Auxiliar.getSpritesOfCharacter(character)["run"],
            12,
            1,
            True,
        )

        self.run_l = Auxiliar.getSurfaceFromSpriteSheet(
            Auxiliar.getSpritesOfCharacter(character)["run"],
            12,
            1,
        )

        self.animation = self.stay_r
        self.frame = 0
        self.image = self.animation[self.frame]
        self.rect: pygame.Rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.move_x = 0
        self.move_y = 0
        self.speed_walk = speed_walk
        self.speed_run = speed_run
        self.gravity = gravity
        self.time_elapsed_ms = 0
        self.view_direction = VIEW_DIRECTION_R
        self.frame_rate_ms = frame_rate_ms
        # self.rect_bottom_collition = pygame.Rect(
        #     self.rect.x + self.rect.w / 4,
        #     self.rect.y + self.rect.h - 10,
        #     self.rect.w / 2,
        #     10,
        # )
        self.run()

    def stay(self):
        if self.animation != self.stay_l and self.animation != self.stay_r:
            if self.view_direction:
                self.animation = self.stay_r
            else:
                self.animation = self.stay_l

            self.move_x = 0
            self.move_y = 0
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

    # def collide_object(self):
    #     if self.rect.colliderect(Player.rect):
    #         return True

    def add_x(self, value):
        self.rect.x += value
        # self.rect_bottom_collition.x += value

    def update_moves(self, delta_ms, platform_list):
        self.time_elapsed_ms += delta_ms

        if self.time_elapsed_ms >= self.frame_rate_ms:
            self.time_elapsed_ms = 0
            if self.rect.x >= ANCHO_VENTANA:
                self.view_direction = False
                self.run()

            elif self.rect.x <= 0:
                self.view_direction = True
                self.run()

            self.add_x(self.move_x)

    def update_animations(self, delta_ms):
        self.time_elapsed_ms += delta_ms

        if self.time_elapsed_ms >= self.frame_rate_ms:
            self.time_elapsed_ms = 0
            if self.frame < len(self.animation) - 1:
                self.frame += 1
            else:
                self.frame = 0

    def update(self, delta_ms, platform_list):
        self.update_animations(delta_ms)
        self.update_moves(delta_ms, platform_list)

    def render(self, screen):
        if DEBUG:
            pygame.draw.rect(screen, RED, self.rect)
            pygame.draw.rect(screen, GREEN, self.rect_bottom_collition)

        self.image = self.animation[self.frame]
        screen.blit(self.image, self.rect)
