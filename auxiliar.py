import pygame
import json


class Auxiliar:
    @staticmethod
    def getSurfaceFromSpriteSheet(path, columnas, filas, flip=False, step=1, scale=1):
        lista = []
        surface_imagen = pygame.image.load(path)
        fotograma_ancho = int(surface_imagen.get_width() / columnas)
        fotograma_alto = int(surface_imagen.get_height() / filas)
        fotograma_ancho_scaled = int(fotograma_ancho * scale)
        fotograma_alto_scaled = int(fotograma_alto * scale)
        x = 0

        for fila in range(filas):
            for columna in range(0, columnas, step):
                x = columna * fotograma_ancho
                y = fila * fotograma_alto
                surface_fotograma = surface_imagen.subsurface(
                    x, y, fotograma_ancho, fotograma_alto
                )
                if scale != 1:
                    surface_fotograma = pygame.transform.scale(
                        surface_fotograma,
                        (fotograma_ancho_scaled, fotograma_alto_scaled),
                    ).convert_alpha()
                if flip:
                    surface_fotograma = pygame.transform.flip(
                        surface_fotograma, True, False
                    ).convert_alpha()
                lista.append(surface_fotograma)
        return lista

    @staticmethod
    def getSurfaceFromSeparateFiles(
        path_format,
        from_index,
        quantity,
        flip=False,
        step=1,
        scale=1,
        w=0,
        h=0,
        repeat_frame=1,
    ):
        lista = []
        for i in range(from_index, quantity + from_index):
            path = path_format.format(i)
            surface_fotograma = pygame.image.load(path)
            fotograma_ancho_scaled = int(surface_fotograma.get_rect().w * scale)
            fotograma_alto_scaled = int(surface_fotograma.get_rect().h * scale)
            if scale == 1 and w != 0 and h != 0:
                surface_fotograma = pygame.transform.scale(
                    surface_fotograma, (w, h)
                ).convert_alpha()
            if scale != 1:
                surface_fotograma = pygame.transform.scale(
                    surface_fotograma, (fotograma_ancho_scaled, fotograma_alto_scaled)
                ).convert_alpha()
            if flip:
                surface_fotograma = pygame.transform.flip(
                    surface_fotograma, True, False
                ).convert_alpha()

            for i in range(repeat_frame):
                lista.append(surface_fotograma)
        return lista

    @staticmethod
    def leer_json(nombre_archivo: str, property: str) -> list[dict]:
        """
        Esta función lee el archivo JSON indicado por parámetro y devuelve el contenido de la key "jugadores"
        parseado como una lista de diccionarios
        :param nombre_archivo: String que representa el nombre del archivo a guardar/sobreescribir
        return: lista de diccionarios que contiene la data de todos los jugadores
        """
        with open(nombre_archivo) as archivo:
            return dict[dict](json.load(archivo)[property])

    @staticmethod
    def set_background_level(level):
        return Auxiliar.leer_json("config.json", "levels")[level]["background_image"]

    @staticmethod
    def generate_music(path: str, volumen: float):
        """
        Función que se encarga de generar una música de fondo para mi juego
        Recibe el path donde se ubique mi música y el volumen de la misma
        """
        pygame.mixer.music.load(path)
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(volumen)

    @staticmethod
    def generate_sound(path: str, volumen: float):
        """
        Función que se encarga de generar un sondi
        Recibe el path en donde se encuentra ese sonido y el volumen del mismo
        Retorna el sonido para esperar a que se ejecute
        """
        sonido = pygame.mixer.Sound(path)
        sonido.set_volume(volumen)
        return sonido

    @staticmethod
    def generate_text(fuente: str, tamaño: float, contenido: str, color: tuple):
        """
        Función que se encarga de generar un texto.
        Recibe la fuente, el tamaño de la misma, el contenido de ese texto y el color
        Retorna la superficie de ese texto
        """
        fuente = pygame.font.SysFont("Arial", tamaño)
        return fuente.render(contenido, True, color)
