import math
import os
import random

import pygame

from Scenes.asteroids.Nave import Nave
from data.resource_utils import generateImagePath
from pantallas import pantallasize


class Asteroid(Nave):
    def __init__(self, x, y, arriba=False, abajo=False, size=None):
        self.x = x
        self.y = y
        self.arriba = arriba
        self.abajo = abajo
        if size == None:
            self.size = [0.5]*5 + [1.0]*3 + [1.5]*2
            self.selected_size = random.choice(self.size)
        else:
            self.selected_size = size
        self.speed = random.uniform(200, 500) * (1 + self.selected_size / 10)  # los meteoritos más grandes son un poco más rápidos

        self.retardo_inicial = random.randint(500, 1500)  # entre 0.5 y 1.5 segundos
        self.tiempo_inicial = pygame.time.get_ticks()
        self.tiempo_ultimo_ataque = pygame.time.get_ticks()
        self.destino_y = 0
        self.moviendo = False

        self.spritesheet = pygame.image.load(generateImagePath(os.path.dirname(os.path.abspath(__file__)), "asteroids", "asteroids.png")).convert_alpha()

        self.tile_size = 64  # Dado que el spritesheet es de 512x512 y tiene 8x8 sprites
        self.rows = 8
        self.cols = 8

        self.current_sprite = 0
        self.animation_speed = 100  # milisegundos por frame, puedes ajustar según necesites
        self.last_animation_update = pygame.time.get_ticks()


        self.sprites = self.load_sprites(self.selected_size)

        # Asumo que quieres usar el primer sprite para inicializar el rect
        self.current_sprite = 0
        self.image = self.sprites[self.current_sprite]
        self.rect = self.image.get_rect(topleft=(x, y))
        self.x = x
        self.y = y

    def scale_image(self, image, scale_factor):
        width = int(image.get_width() * scale_factor)
        height = int(image.get_height() * scale_factor)
        return pygame.transform.scale(image, (width, height))


    def hit(self):
        print(self.selected_size)
        #0.5 pequeño
        #1.0 mediano
        #1.5 grande
        if self.selected_size == 0.5:
            return None
        elif self.selected_size == 1.0:
            return 0.5
        elif self.selected_size == 1.5:
            return 1.0


    def get_random_asteroid(self, sprites_list):
        weights = [0.6, 0.3, 0.1]  # Estos pesos determinan la probabilidad de cada tamaño.
        return random.choices(sprites_list, weights)[0]
    def load_sprites(self, size):
        sprites = []
        for row in range(self.rows):
            for col in range(self.cols):
                # Define la posición y tamaño del sprite en el spritesheet.
                left = col * self.tile_size
                top = row * self.tile_size
                # Extrae el sprite y lo añade a la lista.
                sprite = self.spritesheet.subsurface(pygame.Rect(left, top, self.tile_size, self.tile_size))
                sprite_scaled = self.scale_image(sprite, size)
                # Añade el sprite escalado a la lista.
                sprites.append(sprite_scaled)
        return sprites

    def get_sprite(self, index):
        return self.sprites[index]

    def update(self, dt, now):
        # Movimiento del asteroiderrrrrrrrrrrrrrrrrrr
        angulo_arriba = math.radians(45)  # Convertir 45 grados a radianes
        angulo_abajo = math.radians(-45)  # Convertir -45 grados a radianes

        if self.arriba:
            print("arriba")
            dx_arriba = self.speed * math.cos(angulo_arriba) * dt
            dy_arriba = self.speed * math.sin(angulo_arriba) * dt

            print("arriba: "+str(dx_arriba))
            print("arriba: "+str(dy_arriba))
            self.x -= dx_arriba
            self.y -= dy_arriba
            self.rect.topleft = (self.x, self.y)
        elif self.abajo:
            dx_abajo = (self.speed * math.cos(angulo_abajo)) * dt
            dy_abajo = (self.speed * math.sin(angulo_abajo)) * dt
            self.x -= dx_abajo
            self.y -= dy_abajo
            print("dx_abajo: "+str(dx_abajo))
            print("dx_abajo: "+str(dy_abajo))
            self.rect.topleft = (self.x, self.y)

        else:
            self.x -= self.speed * dt
            self.rect.topleft = (self.x, self.y)

        # Actualizar la animación
        if now - self.last_animation_update > self.animation_speed:
            self.current_sprite = (self.current_sprite + 1) % len(self.sprites)
            self.last_animation_update = now

    def render(self, screen):
        screen.blit(self.sprites[self.current_sprite], self.rect.topleft)

