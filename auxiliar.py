import pygame
import json
import re


class Auxiliar:
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

    def getSurfaceFromSpriteSheet(path, columnas, filas, flip=False, step=1):
        lista = []
        surface_imagen = pygame.image.load(path)

        fotograma_ancho = int(surface_imagen.get_width() / columnas)
        fotograma_alto = int(surface_imagen.get_height() / filas)
        x = 0
        for fila in range(filas):
            for columna in range(0, columnas, step):
                x = columna * fotograma_ancho
                y = fila * fotograma_alto
                surface_fotograma = surface_imagen.subsurface(
                    x, y, fotograma_ancho, fotograma_alto
                )
                if flip:
                    surface_fotograma = pygame.transform.flip(
                        surface_fotograma, True, False
                    )
                lista.append(surface_fotograma)
        return lista

    def getSpritesOfCharacter(character_name):
        characters_data = Auxiliar.leer_json("config.json", "sprites")

        for character in characters_data:
            if re.search(character_name.lower(), character):
                return characters_data[character]

    def set_background_level(level):
        return Auxiliar.leer_json("config.json", "levels")[level]["background_image"]
