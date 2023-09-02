import os
import random

import pygame

from Scenes.starfight.Misil import Misil
from Scenes.starfight.Nave import Nave
from data.resource_utils import generateImagePath
from pantallas import pantallasize


class AlienNave(Nave):
    def __init__(self, x, y):
        self.image = pygame.image.load(
            generateImagePath(os.path.dirname(os.path.abspath(__file__)), "starfight", "enemy.png"))
        self.image_rotada = pygame.transform.rotate(self.image, 90)
        self.rect = self.image_rotada.get_rect(topleft=(x, y))
        self.misiles = []
        self.retardo_inicial = random.randint(500, 1500)  # entre 0.5 y 1.5 segundos
        self.tiempo_inicial = pygame.time.get_ticks()
        self.tiempo_ultimo_ataque = pygame.time.get_ticks()
        self.destino_y = 0
        self.moviendo = False

    def update(self, dt):

        self.intervalo_ataque = random.randint(500, 1500)
        entero_aleatorio = random.randint(0, 20)
        character_speed = 300  # velocidad en píxeles por segundo

        if not self.moviendo or abs(self.rect.y - self.destino_y) < 5:
            #limite de movimiento del enemigo, 100 arriba y 650 abajo (modificado con la funcion offset)

            self.destino_y = random.randint(int(pantallasize.getHeightPosition(100)), int(pantallasize.getHeightPosition(650)))
            self.moviendo = True
        else:
            if self.rect.y < self.destino_y:
                self.rect.y += character_speed * dt
            else:
                self.rect.y -= character_speed * dt

        entero_aleatorio = random.randint(0, 40)
        if entero_aleatorio > 25:
            tiempo_actual = pygame.time.get_ticks()
            if tiempo_actual - self.tiempo_ultimo_ataque > self.intervalo_ataque:
                misil = Misil(self.rect.midleft)
                self.misiles.append(misil)
                self.tiempo_ultimo_ataque = tiempo_actual

        for misil in self.misiles:
            misil.update(dt, False)

            # Eliminar misiles fuera de la pantalla
            # todo fix screen size
            if misil.rect.right < pantallasize.getWidthPosition(0):
                self.misiles.remove(misil)

    def render(self, screen):
        screen.blit(self.image_rotada, self.rect)
        for misil in self.misiles:
            misil.render(screen)
