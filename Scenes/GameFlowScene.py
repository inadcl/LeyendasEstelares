import os

import pygame

from Scenes.Scene import Scene, screen_width, screen_height
from data.GameState import GameState
from data.leermisiones import leer_misiones





class GameFlowScene(Scene):
    gamestate:GameState;
    def initScene(self, gameState):
        super().initScene(gameState)
        self.gameState = gameState

        self.misiones = leer_misiones()
        print("Scene loaded")
        pass
    def process_input(self, events, pressed_keys, button):
        super().process_input(events, pressed_keys, button)
        pass

    def update(self):
        pass

    def render(self, screen):
        screen.fill((255, 255, 255))
        current_dir = os.path.dirname(os.path.abspath(__file__))
        image_path = os.path.join(current_dir, '..', 'recursos', 'imagenes', 'ui', 'background.png')
        background = pygame.image.load(image_path)
        screen.blit(background, (0, 0))
        self.dibujarNave(screen)
        super().render(screen)
        # Actualizar la pantalla
        pass
        # Here add the rendering code for the game scene
    def dibujarNave(self, screen):
        background_image = pygame.image.load(os.path.join("recursos", os.path.join(os.path.join("imagenes", "nave")
                                                                                   , "skin_nave.png")))
        screen.blit(background_image, (0, 0))
        pass