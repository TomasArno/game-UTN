from gui_form import Form
from gui_button import Button


class FormMenuA(Form):
    def __init__(
        self, name, master_surface, x, y, w, h, bg_color, border_color, active
    ):
        super().__init__(
            name, master_surface, x, y, w, h, bg_color, border_color, active
        )

        self.boton1 = Button(
            master=self,
            x=50,
            y=50,
            w=200,
            h=50,
            bg_color=(255, 0, 0),
            border_color=(255, 0, 255),
            on_click=self.on_click_boton1,
            on_click_params="form_menu_B",
            text="ABRIR B",
            font="Verdana",
            font_size=30,
            font_color=(0, 255, 0),
        )
        self.boton2 = Button(
            master=self,
            x=200,
            y=50,
            w=200,
            h=50,
            bg_color=(255, 0, 0),
            border_color=(255, 0, 255),
            on_click=self.on_click_boton1,
            on_click_params="form_menu_B",
            text="MENU 2",
            font="Verdana",
            font_size=30,
            font_color=(0, 255, 0),
        )
        self.lista_widget = [self.boton1, self.boton2]

    def on_click_boton1(self, parametro):
        self.set_active(parametro)

    def update(self, lista_eventos):
        for aux_boton in self.lista_widget:
            aux_boton.update(lista_eventos)

    def draw(self):
        super().draw()
        for aux_boton in self.lista_widget:
            aux_boton.draw()
