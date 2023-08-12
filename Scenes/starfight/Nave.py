import os

import pygame

from Scenes.starfight.Misil import Misil
from data.resource_utils import generateImagePath


class Nave:
    def __init__(self, x, y):

        self.image = pygame.image.load(generateImagePath(os.path.dirname(os.path.abspath(__file__)), "starfight", "player.png"))
        self.image_rotada = pygame.transform.rotate(self.image, -90)
        self.rect = self.image_rotada.get_rect(topleft=(x, y))
        self.misiles = []

    def mover_arriba(self):
        if self.rect.y > 100:
            print("arriba" + str(self.rect.y))
            self.rect.y -= 5  # Ajusta este valor para cambiar la velocidad de movimiento

    def mover_abajo(self):
        if self.rect.y < 950:
            print("abajo" + str(self.rect.y))
            self.rect.y += 5  # Ajusta este valor para cambiar la velocidad de movimiento
    def lanzar_misil(self):
        misil = Misil(self.rect.midright)
        self.misiles.append(misil)

    def update(self):
        for misil in self.misiles:
            misil.update()

            # Eliminar misiles fuera de la pantalla
            #todo fix screen size
            if misil.rect.left > 1024:
                self.misiles.remove(misil)

            # for misil in self.misiles:
            #     if misil.rect.colliderect(
            #             self.rect):  # 'otro_rect' es el rectángulo de otro objeto con el que quieres detectar la colisión
            #         # Aquí manejas la lógica de la colisión, por ejemplo, eliminar el misil o reducir la salud de un enemigo
            #         self.nave.misiles.remove(misil)

    def render(self, screen):
        screen.blit(self.image_rotada, self.rect)
        for misil in self.misiles:
            misil.render(screen)