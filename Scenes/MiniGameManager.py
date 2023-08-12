import os
import random

import pygame

from Scenes.Scene import Scene, screen_width, screen_height
from Scenes.starfight.Starfight import Starfight
from data import GameState
from data.DrawUtils import addText, dibujarFondos
from data.leermisiones import leer_misiones, leer_mensaje_inicial
from data.stringutils import debugRect, wraptext
from enum import Enum
class Minijuegos(Enum):
    STARFIGHT = 1

    @staticmethod
    def getEnum(minijuego):
        if minijuego.upper() == Minijuegos.STARFIGHT.name:
            return Minijuegos.STARFIGHT.name

class MiniGameManager(Scene):
    def __init__(self, gameflowscene, minijuego, alien, activeGameState:GameState):
        self.readingProcess = None
        self.current_dir = os.path.dirname(os.path.abspath(__file__))
        self.gameflowscene = gameflowscene
        self.minijuego = Minijuegos.getEnum(minijuego)
        self.alien = alien
        self.renderRequired = True
        if self.minijuego == Minijuegos.STARFIGHT.name:
            self.activeGame = Starfight(gameflowscene, alien, activeGameState)
        else:
            self.activeGame = None
        if activeGameState is not None:
            self.initScene(activeGameState)


    def initScene(self, activeGameState):
        super().initScene(activeGameState)
        self.activeGameState = activeGameState
        print("Scene loaded")
        self.activeGame.initScene(activeGameState)
        pass

    def process_input(self, events, pressed_keys, button):
        super().process_input(events, pressed_keys, button)
        return self.activeGame.process_input(events, pressed_keys, button)

    def update(self):
        self.activeGame.update()



    def render(self, screen, activeGameState):
        if self.renderRequired:
            self.renderRequired = False
            self.activeGameState = activeGameState

            # Set the background color to black
            screen.fill((0, 0, 0))

            # Refresh the display
            pygame.display.flip()
            super().render(screen)
            # posicion avatar
        self.activeGame.render(screen, activeGameState)
