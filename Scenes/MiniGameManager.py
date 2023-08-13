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
    def __init__(self, gameflowscene, minijuego, alien, activeGameState:GameState, minigameOption):
        super().__init__()
        self.readingProcess = None
        self.current_dir = os.path.dirname(os.path.abspath(__file__))
        self.gameflowscene = gameflowscene
        self.minijuego = Minijuegos.getEnum(minijuego)
        self.alien = alien
        self.renderRequired = True
        self.minigameOption = minigameOption
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
        new_scene = self.activeGame.process_input(events, pressed_keys, button)
        if new_scene != None:
            self.switch_on = True
            self.add_new_scene(new_scene)
            return None

    def update(self):
        status = self.activeGame.update()
        if status != None:
            if status:
                if self.gameflowscene != None:
                        self.switch_on = True
                        self.gameflowscene.renderRequired = True
                        self.gameflowscene.minigameoption = self.minigameOption
                        self.add_new_scene(self.gameflowscene)
                        return None
            else:
                #todo create game over
                if self.gameflowscene != None:
                        self.switch_on = True
                        self.gameflowscene.renderRequired = True
                        self.gameflowscene.minigameoption = self.minigameOption
                        self.add_new_scene(self.gameflowscene)
                        return None



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
