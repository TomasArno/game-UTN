import pygame
from constants import *
from gui_widget import Widget


class Button(Widget):
    def __init__(
        self,
        master,
        x,
        y,
        w,
        h,
        bg_color,
        border_color,
        text,
        font,
        font_size,
        font_color,
        on_click,
        on_click_params,
    ) -> None:
        super().__init__(
            master,
            x,
            y,
            w,
            h,
            bg_color,
            border_color,
        )
        pygame.font.init()

        self.on_click = on_click
        self.on_click_params = on_click_params
        self.text = text
        self.font_sys = pygame.font.SysFont(font, font_size)
        self.font_color = font_color
        self.render()

    def render(self):
        surface_text = self.font_sys.render(
            self.text, True, self.font_color, self.background_color
        )
        self.slave_surface: pygame.Surface = pygame.surface.Surface((self.w, self.h))

        self.slave_rect = self.slave_surface.get_rect()

        self.slave_rect.x = self.x
        self.slave_rect.y = self.y
        self.slave_rect_collide = pygame.Rect(self.slave_rect)
        self.slave_rect_collide.x += self.master_form.x
        self.slave_rect_collide.y += self.master_form.y
        self.slave_surface.fill(self.background_color)
        self.slave_surface.blit(surface_text, (10, 10))

    def update(self, event_list):
        for event in event_list:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.slave_rect_collide.collidepoint(event.pos):
                    self.on_click(self.on_click_params)

        self.render()
