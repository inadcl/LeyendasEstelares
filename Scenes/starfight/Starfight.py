import os

import pygame

from Scenes.Scene import Scene
from Scenes.starfight.AlienNave import AlienNave
from Scenes.starfight.Nave import Nave
from data import GameState

class Starfight(Scene):
    def __init__(self, gameflowscene, alien, activeGameState:GameState):
        super().__init__()
        self.readingProcess = None
        self.current_dir = os.path.dirname(os.path.abspath(__file__))
        self.gameflowscene = gameflowscene
        self.alien = alien
        self.renderRequired = True
        if activeGameState is not None:
            self.initScene(activeGameState)
        self.nave = Nave(100,100)
        self.alienship = AlienNave(900,500)
        self.game_over = False
        self.game_win = False

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
        if self.game_over:
            return False
        if self.game_win:
            return True

        for misil in self.nave.misiles:
            if misil.live and misil.rect.colliderect(self.alienship.rect):
                self.alien.defensa = self.alien.defensa - self.activeGameState.ataque
                if self.alien.defensa <= 0:
                    print("enemigo derrotado")
                    self.game_win = True
                else:
                    self.misil.live = False

        for misil in self.alienship.misiles:
            if misil.live and misil.rect.colliderect(self.nave.rect):
                self.activeGameState.disminuir_defensa(self.alien.ataque)
                if self.activeGameState.defensa <= 0:
                    print("Jugador muerto")
                    self.game_over = True
                else:
                    self.misil.live = False

        self.nave.update(self.activeGameState.get_delta_time())
        self.alienship.update(self.activeGameState.get_delta_time())
        if self.activeGameState.defensa <= 0:
            print("gameover")
            #todo: gameover
        if self.alien.defensa <= 0:
            print("enemigo derrotado")

        return None


    def generateImagePath(self, folder, filename):
        return os.path.join(self.current_dir, '..', 'recursos', 'imagenes', folder, filename)

    def render(self, screen, activeGameState):
        self.renderRequired= True
        if not self.renderRequired or self.game_win or self.game_over:
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
        self.alienship.render(screen)
        pygame.display.flip()
