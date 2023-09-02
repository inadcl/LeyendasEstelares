import os

import pygame

from Scenes.Scene import Scene
from Scenes.starfight.AlienNave import AlienNave
from Scenes.starfight.Nave import Nave
from data import GameState
from data.DrawUtils import dibujar_stats, dibujarFondos
from data.resource_utils import generateSoundPathLevel2
from pantallas import pantallasize


class Starfight(Scene):
    def __init__(self, gameflowscene, alien, activeGameState: GameState):
        super().__init__()
        TIEMPO_DE_DISPARO = 1000
        self.readingProcess = None
        self.current_dir = os.path.dirname(os.path.abspath(__file__))
        self.gameflowscene = gameflowscene
        self.alien = alien
        self.renderRequired = True
        if activeGameState is not None:
            self.initScene(activeGameState)
        self.nave = Nave(pantallasize.getWidthPosition(100), pantallasize.getHeightPosition(100))
        self.alienship = AlienNave(pantallasize.getWidthPosition(900), pantallasize.getHeightPosition(500))
        self.contador = False
        self.puedo_disparar = False
        self.game_over = False
        self.game_win = False
        self.disparo_hit_explosion = pygame.mixer.Sound(
            generateSoundPathLevel2(os.path.dirname(os.path.abspath(__file__)), "starfight", "explosion.wav"))
        self.disparo_hit_explosion.set_volume(0.5)
        self.misilescount = 0
        self.ultimomisil = 0
        self.shoot_timer_event = pygame.USEREVENT + 2
        pygame.time.set_timer(self.shoot_timer_event, TIEMPO_DE_DISPARO)

    def initScene(self, activeGameState):
        super().initScene(activeGameState)
        self.activeGameState = activeGameState
        print("Scene loaded")
        pass

    def process_input(self, events, pressed_keys, button):
        super().process_input(events, pressed_keys, button)
        # handle_inicio_mouse_click(mission_button, draw_exit_by_state(screen), pygame.mouse.get_pos())
        for event in events:
            if event.type == self.shoot_timer_event:
                self.puedo_disparar = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:  # Lanzar misil con la tecla espacio
                    if self.puedo_disparar:
                        self.nave.lanzar_misil()
                        self.puedo_disparar = False
                elif event.key == pygame.K_UP or event.key == pygame.K_w:  # Si se presiona la flecha hacia arriba
                    self.nave.mover_arriba()
                elif event.key == pygame.K_DOWN or event.key == pygame.K_s:  # Si se presiona la flecha hacia abajo
                    self.nave.mover_abajo()
        return None

    def update(self):
        self.renderRequired = True
        if self.game_over or self.game_win:
            for misil in self.nave.misiles:
                self.nave.misiles.remove(misil)
            for misil in self.alienship.misiles:
                self.alienship.misiles.remove(misil)
        if self.game_over:
            return False
        if self.game_win:
            return True

        for misil in self.nave.misiles:
            if misil.live and misil.rect.colliderect(self.alienship.rect):
                self.alien.defensa = self.alien.defensa - self.activeGameState.ataque
                if self.alien.defensa <= 0:
                    # todo check sonido
                    self.disparo_hit_explosion.play()
                    print("enemigo derrotado")
                    self.game_win = True
                else:
                    if misil != None:
                        misil.live = False

        for misil in self.alienship.misiles:
            if misil.live and misil.rect.colliderect(self.nave.rect):
                self.activeGameState.disminuir_defensa(self.alien.ataque)
                if self.activeGameState.defensa <= 0:
                    self.disparo_hit_explosion.play()
                    print("Jugador muerto")
                    self.game_over = True
                else:
                    if misil != None:
                        misil.live = False

        self.nave.update(self.activeGameState.get_delta_time())
        self.alienship.update(self.activeGameState.get_delta_time())

        return None

    def generateImagePath(self, folder, filename):
        return os.path.join(self.current_dir, '..', 'recursos', 'imagenes', folder, filename)

    def render(self, screen, activeGameState):
        self.renderRequired = True
        if not self.renderRequired or self.game_win or self.game_over:
            return
        else:
            self.renderRequired = False
            self.activeGameState = activeGameState

            # Set the background color to black
            screen.fill((128, 128, 128))
            # Dibuja el fondo del área de juego
            game_surface = pygame.Surface((1024, 768))
            game_surface.fill((0, 0, 0))
            screen.blit(game_surface, (pantallasize.getWidthPosition(0), pantallasize.getHeightPosition(0)))

            # Refresh the display
            pygame.display.flip()
            super().render(screen)
            # posicion avatar

        self.uirender(screen)
        self.nave.render(screen)
        self.alienship.render(screen)
        pygame.display.flip()

    def uirender(self, screen):

        # alien
        rect_x = pantallasize.getWidthPosition(300)
        rect_y = pantallasize.getHeightPosition(20)
        rect_width = 560
        rect_height = 65
        color_interior = "#5a5a5a"
        color_borde = "#a5a5a5"
        dibujarFondos(screen, rect_x, rect_y, rect_width, rect_height, color_interior, color_borde)

        nombre_alien_rect = (pantallasize.getWidthPosition(800), pantallasize.getHeightPosition(40))
        karma_alien_rect = (pantallasize.getWidthPosition(760), pantallasize.getHeightPosition(65))
        ataque_alien_rect = (pantallasize.getWidthPosition(795), pantallasize.getHeightPosition(65))
        defensa_alien_rect = (pantallasize.getWidthPosition(835), pantallasize.getHeightPosition(65))
        image_alien_rect = (pantallasize.getWidthPosition(700), pantallasize.getHeightPosition(27), 50, 50)
        if self.alien != None and self.alien.nombre != None:
            dibujar_stats(screen, self.alien.nombre, "K: " + str(self.alien.karma),
                          "A: " + str(self.alien.ataque), "D: " + str(self.alien.defensa), nombre_alien_rect,
                          karma_alien_rect, ataque_alien_rect, defensa_alien_rect, 36, 15)

        if self.alien.image != None:
            self.dibujar_avatar(screen, "aliens", self.alien.image, image_alien_rect)
        nombre_player_rect = (pantallasize.getWidthPosition(440), pantallasize.getHeightPosition(40))
        karma_playern_rect = (pantallasize.getWidthPosition(400), pantallasize.getHeightPosition(65))
        ataque_player_rect = (pantallasize.getWidthPosition(435), pantallasize.getHeightPosition(65))
        defensa_player_rect = (pantallasize.getWidthPosition(375), pantallasize.getHeightPosition(65))
        image_player_rect = (pantallasize.getWidthPosition(305), pantallasize.getHeightPosition(27), 50, 50)
        dibujar_stats(screen, self.activeGameState.nombre, "K: " + str(self.activeGameState.karma),
                      "A: " + str(self.activeGameState.ataque), "D: " + str(self.activeGameState.defensa),
                      nombre_player_rect,
                      karma_playern_rect, ataque_player_rect, defensa_player_rect, 36, 15)

        if self.activeGameState.imagen != None:
            self.dibujar_avatar(screen, "personajes", self.activeGameState.imagen, image_player_rect)

    def dibujar_avatar(self, screen, folder, imagen, rect):
        personaje = os.path.join('recursos', 'imagenes', folder, imagen)
        personaje_image = pygame.image.load(personaje)
        imagen_redimensionada = pygame.transform.scale(personaje_image, (50, 50))
        screen.blit(imagen_redimensionada, rect)
