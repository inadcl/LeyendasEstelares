import os

import pygame

from Scenes.Scene import Scene
from Scenes.starfight.AlienNave import AlienNave
from Scenes.starfight.Nave import Nave
from data import GameState
from data.DrawUtils import dibujar_stats, dibujarFondos
from data.resource_utils import generateSoundPathLevel2




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
        self.disparo_sonido = pygame.mixer.Sound(generateSoundPathLevel2(os.path.dirname(os.path.abspath(__file__)), "starfight","explosion.wav"))
        self.disparo_sonido.set_volume(0.5)

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
                    self.disparo_sonido.play()
                    print("enemigo derrotado")
                    self.game_win = True
                else:
                    if misil != None:
                        misil.live = False

        for misil in self.alienship.misiles:
            if misil.live and misil.rect.colliderect(self.nave.rect):
                self.activeGameState.disminuir_defensa(self.alien.ataque)
                if self.activeGameState.defensa <= 0:
                    self.disparo_sonido.play()
                    print("Jugador muerto")
                    self.game_over = True
                else:
                    if misil != None:
                        misil.live = False

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

        self.uirender(screen, activeGameState)
        self.nave.render(screen)
        self.alienship.render(screen)
        pygame.display.flip()

    def uirender(self, screen, activeGameState):

        # alien
        rect_x = 300
        rect_y = 20
        rect_width = 560
        rect_height = 65
        color_interior = "#5a5a5a"
        color_borde = "#a5a5a5"
        dibujarFondos(screen, rect_x, rect_y, rect_width, rect_height, color_interior, color_borde)

        nombre_alien_rect = (800, 40)
        karma_alien_rect = (760, 65)
        ataque_alien_rect = (795, 65)
        defensa_alien_rect = (835, 65)
        image_alien_rect = (700, 27, 50,50)
        dibujar_stats(screen, self.alien.nombre, "K: " + str(self.alien.karma),
                     "A: " + str(self.alien.ataque), "D: " + str(self.alien.defensa), nombre_alien_rect,
                      karma_alien_rect, ataque_alien_rect, defensa_alien_rect, 36, 15)

        if self.alien.image!= None:
            self.dibujar_avatar(screen, "aliens", self.alien.image, image_alien_rect)
        nombre_player_rect = (440, 40)
        karma_playern_rect = (400, 65)
        ataque_player_rect = (435, 65)
        defensa_player_rect = (375, 65)
        image_player_rect = (305, 27, 50,50)
        dibujar_stats(screen, self.activeGameState.nombre, "K: " + str(self.activeGameState.karma),
                     "A: " + str(self.activeGameState.ataque), "D: " + str(self.activeGameState.defensa), nombre_player_rect,
                      karma_playern_rect, ataque_player_rect, defensa_player_rect, 36, 15)

        if self.activeGameState.imagen!= None:
            self.dibujar_avatar(screen, "personajes", self.activeGameState.imagen, image_player_rect)


    def dibujar_avatar(self, screen, folder, imagen, rect):
        personaje = os.path.join('recursos', 'imagenes', folder, imagen)
        personaje_image = pygame.image.load(personaje)
        imagen_redimensionada = pygame.transform.scale(personaje_image, (50, 50))
        screen.blit(imagen_redimensionada, rect)