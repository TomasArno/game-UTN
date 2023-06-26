class Widget:
    def __init__(self, master_form, x, y, w, h, bg_color, border_color) -> None:
        self.master_form = master_form
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.background_color = bg_color
        self.border_color = border_color

    def draw(self):
        self.master_form.slave_surface.blit(self.slave_surface, self.slave_rect)
