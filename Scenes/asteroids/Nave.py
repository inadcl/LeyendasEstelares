import os

import pygame

from Scenes.asteroids.Misil import Misil
from data.resource_utils import generateImagePath
from pantallas import pantallasize


class Nave:
    def __init__(self, x, y):

        self.image = pygame.image.load(
            generateImagePath(os.path.dirname(os.path.abspath(__file__)), "starfight", "player.png"))
        self.image_rotada = pygame.transform.rotate(self.image, -90)
        self.rect = self.image_rotada.get_rect(topleft=(x, y))
        self.misiles = []
        self.goUp = False
        self.goDown = False
        self.fire = False

    def mover_arriba(self):
        self.goDown = False
        self.goUp = True

    def mover_abajo(self):
        self.goUp = False
        self.goDown = True

    def lanzar_misil(self):
        misil = Misil(self.rect.midright)
        self.misiles.append(misil)

    def update(self, dt):
        character_speed = 2000  # velocidad en píxeles por segundo
        if self.goUp and self.rect.y > pantallasize.getHeightPosition(125):
            self.goUp = False
            print("arriba" + str(self.rect.y))
            print("deltatime" + str(dt))
            self.rect.y -= character_speed * dt  # Ajusta este valor para cambiar la velocidad de movimiento

        if self.goDown and self.rect.y < pantallasize.getHeightPosition(650):
            self.goDown = False
            print("abajo" + str(self.rect.y))
            print("deltatime" + str(dt))
            self.rect.y += character_speed * dt  # Ajusta este valor para cambiar la velocidad de movimiento

        for misil in self.misiles:
            if not misil.live:
                self.misiles.remove(misil)

            misil.update(dt, True)

            # Eliminar misiles fuera de la pantalla
            # todo fix screen size
            if misil.rect.left > pantallasize.getWidthPosition(1000) or misil.rect.left < pantallasize.getWidthPosition(0):
                self.misiles.remove(misil)

    def render(self, screen):
        screen.blit(self.image_rotada, self.rect)
        for misil in self.misiles:
            misil.render(screen)
