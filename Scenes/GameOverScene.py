import asyncio
import os

import pygame

from Scenes.Scene import Scene

from data.DrawUtils import addText, dibujarFondos
from data.GameState import GameState
from data.resource_utils import generateSoundPath
from data.stringutils import wraptext
from pantallas import pantallasize





class GameOverScene(Scene):
    init = False
    activeGameState:GameState;

    def __init__(self, activeGameState):
        super().__init__()
        if activeGameState is not None:
            self.initScene(activeGameState)
        self.selected_sonido = pygame.mixer.Sound(
            generateSoundPath(os.path.dirname(os.path.abspath(__file__)), "ui", "selected.wav"))
        self.selected_sonido.set_volume(0.5)
        self.endGameOver = False

    def initScene(self, activeGameState):
        super().initScene(activeGameState)
        self.activeGameState = activeGameState
        if self.init == False:
            self.oldtext = ""
            self.init = True
            self.puntuacion = activeGameState
        pass

    def restartGame(self):
        if self.endGameOver:
            self.endGameOver = False
            return True
        return self.endGameOver

    def exitScene(self):
        self.init = False
        pass

    def process_input(self, events, pressed_keys, button):
        super().process_input(events, pressed_keys, button)
        # handle_inicio_mouse_click(mission_button, draw_exit_by_state(screen), pygame.mouse.get_pos())
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self.selectButton(mouse_pos)
                self.endGameOver = True
        return None

    def update(self):
        pass

    def paintArrow(self, right, img):
        arrow = pygame.transform.flip(img, right, False)
        return arrow

    def render(self, screen, activeGameState):
        self.activeGameState = activeGameState
        # screen.fill((255, 255, 255))

        # Obtiene la ruta al directorio del archivo actual.
        current_dir = os.path.dirname(os.path.abspath(__file__))

        # Construye la ruta a la imagen.
        image_path = os.path.join(current_dir, '..', 'recursos', 'imagenes', 'ui', 'background.png')
        background = pygame.image.load(image_path)

        # Dibuja el fondo y las imágenes de las flechas en la pantalla.
        screen.blit(background, (pantallasize.getWidthPosition(0),  pantallasize.getHeightPosition(0)))

        nombre = self.activeGameState.nombre
        #todo hacer el gameover inteligente, segun el karma uno u otro mensaje y añadir mas stats, ademas de leer desde json (traducible y modificable)
        descripcion =  "GameOver - Pulsa cualquier tecla para continuar"

        #super().readText(descripcion)
        karma = self.activeGameState.karma
        ataque = self.activeGameState.ataque
        defensa = self.activeGameState.defensa

        self.dibujarFondos(screen)
        nombre_rect= (pantallasize.getWidthPosition(525),  pantallasize.getHeightPosition(350))
        karma_rect = (pantallasize.getWidthPosition(525),  pantallasize.getHeightPosition(175))
        ataque_rect =  (pantallasize.getWidthPosition(525),  pantallasize.getHeightPosition(150))
        defensa_rect = (pantallasize.getWidthPosition(525),  pantallasize.getHeightPosition(125))
        addText(screen, nombre, "Karma: " + str(karma), "Ataque: " + str(ataque), "Defensa: " + str(defensa), nombre_rect, karma_rect, ataque_rect, defensa_rect, 36)
        #self.addDesc(screen, descripcion)
        super().render(screen)
        self.oldtext = descripcion
        super().callReader(descripcion)
        self.addDesc(screen, descripcion)

        pass


    def dibujarFondos(self, screen):
        rect_x = pantallasize.getWidthPosition(200)
        rect_y = pantallasize.getHeightPosition(425)
        rect_width = 550
        rect_height = 300
        color_interior = "#5a5a5a"
        color_borde = "#a5a5a5"
        dibujarFondos(screen, rect_x, rect_y, rect_width, rect_height, color_interior, color_borde)

        rect_x = pantallasize.getWidthPosition(425)
        rect_y = pantallasize.getHeightPosition(330)
        rect_width = 200
        rect_height = 40
        pygame.draw.rect(screen, color_interior, (rect_x - 4, rect_y - 4, rect_width + 8, rect_height + 8))
        pygame.draw.rect(screen, color_borde, (rect_x, rect_y, rect_width, rect_height))
        rect_x = pantallasize.getWidthPosition(445)
        rect_y = pantallasize.getHeightPosition(100)
        rect_width = 175
        rect_height = 100
        pygame.draw.rect(screen, color_interior, (rect_x - 4, rect_y - 4, rect_width + 8, rect_height + 8))
        pygame.draw.rect(screen, color_borde, (rect_x, rect_y, rect_width, rect_height))

    def addDesc(self, screen, descripcion):

        # Crear una fuente
        fuente = pygame.font.Font(None, 36)

        lineas = wraptext(descripcion, fuente, 500)
        for i, linea in enumerate(lineas):
            texto_renderizado = fuente.render(linea, True, "#0000ff")
            screen.blit(texto_renderizado, (pantallasize.getWidthPosition(225),  pantallasize.getHeightPosition(450 + i * fuente.get_height())))


    def selectButton(self, mouse_pos):
        pass

        # pos_image = pygame.Rect(pantallasize.getWidthPosition(400), pantallasize.getHeightPosition(50), 250, 250)
        # if pos_image.collidepoint(mouse_pos):
        #     self.selected_sonido.play()
        #     print(self.posicionActual)
        #     nextScene = TitleScene()
        #     nextScene.initScene(self.activeGameState)
        #     return nextScene