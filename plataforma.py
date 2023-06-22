import pygame
from constants import *
from auxiliar import Auxiliar


class Platform:
    def __init__(self, x, y, width, height, type) -> None:
        self.block = Auxiliar.getSurfaceFromSpriteSheet(
            f"{PATH_IMAGES}/PIXEL ADVENTURE/PIXEL ADVENTURE/Recursos/Terrain/Terrain (16x16).png",
            4,
            3,
        )[type]

        self.block = pygame.transform.scale(self.block, (width, height))
        self.rect = self.block.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.rect_bottom_collition = pygame.Rect(
            self.rect.x,
            self.rect.y,
            self.rect.w,
            2,
        )

    def render(self, screen):
        if DEBUG:
            pygame.draw.rect(screen, RED, self.rect)
        screen.blit(self.block, self.rect)
        if DEBUG:
            pygame.draw.rect(screen, GREEN, self.rect_bottom_collition)
