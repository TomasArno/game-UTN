import pygame
from constantes import *
from auxiliar import Auxiliar
from player import Player


class Background:
    def __init__(self, x, y, width, height, path):
        self.image = pygame.image.load(Auxiliar.set_background_level(path)).convert()
        self.image = pygame.transform.scale(self.image, (width, height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self, player: Player):
        # self.rect.x = player.rect.centerx
        pass

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        # if(DEBUG):
        #     pygame.draw.rect(screen,color=(255,0 ,0),rect=self.collition_rect)
