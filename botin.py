import pygame
from constantes import *
from auxiliar import Auxiliar


class Item:
    def __init__(
        self, x, y, width, height, frame_rate_ms, move_rate_ms, is_active=True
    ):
        self.stay = Auxiliar.getSurfaceFromSpriteSheet(
            Auxiliar.leer_json("config.json", "levels")["l1"]["item_image"],
            17,
            1,
        )

        self.contador = 0
        self.tiempo_transcurrido_animation = 0
        self.frame_rate_ms = frame_rate_ms
        self.tiempo_transcurrido_move = 0
        self.move_rate_ms = move_rate_ms
        self.frame = 0
        self.animation = self.stay
        self.image = self.animation[self.frame]
        self.rect: pygame.Rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.move_y = 0
        self.is_active = is_active

    def set_items(level):
        level_items = Auxiliar.leer_json("config.json", "levels")[level]["items"]

        item_list = []

        for item in level_items:
            item_list.append(
                Item(
                    item["x"],
                    item["y"],
                    item["w"],
                    item["h"],
                    item["frame_rate_ms"],
                    item["move_rate_ms"],
                    item["is_active"],
                )
            )

        return item_list

    def change_y(self, delta_y):
        self.rect.y += delta_y

    def check_collide(self, player):
        if self.rect.colliderect(player.collition_rect):
            player.grab_item()
            self.is_active = False

    def do_movement(self, delta_ms, player):
        self.tiempo_transcurrido_move += delta_ms
        if self.tiempo_transcurrido_move >= self.move_rate_ms:
            self.tiempo_transcurrido_move = 0

            self.change_y(self.move_y)
            if self.contador <= 3:
                self.move_y = -2
                self.contador += 1
            elif self.contador <= 6:
                self.move_y = 2
                self.contador += 1
            else:
                self.contador = 0
            self.check_collide(player)

    def do_animation(self, delta_ms):
        self.tiempo_transcurrido_animation += delta_ms
        if self.tiempo_transcurrido_animation >= self.frame_rate_ms:
            self.tiempo_transcurrido_animation = 0
            if self.frame < len(self.animation) - 1:
                self.frame += 1
            else:
                self.frame = 0

    def update(self, delta_ms, player):
        # if not self.finish_dead_animation:
        self.do_movement(delta_ms, player)
        self.do_animation(delta_ms)

    def draw(self, screen):
        if DEBUG:
            pygame.draw.rect(screen, color=(0, 0, 255), rect=self.rect)

        self.image = self.animation[self.frame]
        screen.blit(self.image, self.rect)
