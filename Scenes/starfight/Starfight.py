import os
import random

import pygame

from Scenes.Scene import Scene, screen_width, screen_height
from Scenes.starfight.Nave import Nave
from data import GameState
from data.DrawUtils import addText, dibujarFondos
from data.leermisiones import leer_misiones, leer_mensaje_inicial
from data.stringutils import debugRect, wraptext

class Starfight(Scene):
    def __init__(self, gameflowscene, alien, activeGameState:GameState):
        self.readingProcess = None
        self.current_dir = os.path.dirname(os.path.abspath(__file__))
        self.gameflowscene = gameflowscene
        self.alien = alien
        self.renderRequired = True
        if activeGameState is not None:
            self.initScene(activeGameState)
        self.nave = Nave(100,100)

    def initScene(self, activeGameState):
        super().initScene(activeGameState)
        self.activeGameState = activeGameState
        print("Scene loaded")
        pass

    def process_input(self, events, pressed_keys, button):
        super().process_input(events, pressed_keys, button)
        # handle_inicio_mouse_click(mission_button, draw_exit_by_state(screen), pygame.mouse.get_pos())
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:  # Lanzar misil con la tecla espacio
                    self.nave.lanzar_misil()
                elif event.key == pygame.K_UP:  # Si se presiona la flecha hacia arriba
                    self.nave.mover_arriba()
                elif event.key == pygame.K_DOWN:  # Si se presiona la flecha hacia abajo
                    self.nave.mover_abajo()
        return None

    def update(self):
        self.renderRequired = True
        self.nave.update(self.activeGameState.get_delta_time())
        if self.activeGameState.defensa == 0:
            print("gameover")
            #todo: gameover
        if self.alien["defensa"] == 0:
            print("enemigo derrotado")


    def generateImagePath(self, folder, filename):
        return os.path.join(self.current_dir, '..', 'recursos', 'imagenes', folder, filename)

    def render(self, screen, activeGameState):
        self.renderRequired= True
        if not self.renderRequired:
            return
        else:
            self.renderRequired = False
            self.activeGameState = activeGameState

            # Set the background color to black
            screen.fill((0, 0, 0))

            # Refresh the display
            pygame.display.flip()
            super().render(screen)
            # posicion avatar
        self.nave.render(screen)
        pygame.display.flip()
