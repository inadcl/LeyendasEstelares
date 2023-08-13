import asyncio
import os

import pygame

from Scenes.GameFlowScene import GameFlowScene
from Scenes.Scene import Scene
import sys

from data.DrawUtils import addText, dibujarFondos
from data.GameState import GameState
from data.leermisiones import leer_personajes
from data.stringutils import wraptext

pos_image = pygame.Rect(400,50,250,250)
pos_leftarrow = pygame.Rect(125,275,150,150)
pos_rightarrow = pygame.Rect(725,275,150,150)




class TitleScene(Scene):
    init = False
    activeGameState:GameState;

    def __init__(self, activeGameState=None):
        super().__init__()
        if activeGameState is not None:
            self.initScene(activeGameState)
        pass
    def initScene(self, activeGameState):
        super().initScene(activeGameState)
        self.activeGameState = activeGameState
        if self.init == False:
            self.oldtext = "Elige jugador."
            self.init = True
            self.personajes = leer_personajes()
            self.posicionActual = 0
        pass

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
                new_scene = self.selectCharacter(mouse_pos)

                if new_scene != None:
                        self.switch_on = True
                        self.add_new_scene(new_scene)
                        return None
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
        rigth_arrow_path = os.path.join(current_dir, '..', 'recursos', 'imagenes', 'ui', 'rightarrow.png')

        left_arrow_path = os.path.join(current_dir, '..', 'recursos', 'imagenes', 'ui', 'leftarrow.png')
        self.personajerow = self.personajes[self.posicionActual]

        personaje = os.path.join(current_dir, '..', 'recursos', 'imagenes', 'personajes', self.personajerow["image"])
        # Carga la imagen.
        background = pygame.image.load(image_path)
        self.right_arrow = pygame.image.load(rigth_arrow_path)
        self.left_arrow = pygame.image.load(left_arrow_path)
        personaje = pygame.image.load(personaje)
        # Carga la imagen.

        # Dibuja el fondo y las imágenes de las flechas en la pantalla.
        screen.blit(background, (0, 0))
        screen.blit(self.right_arrow, (700, 250))
        screen.blit(self.left_arrow, (100, 250))
        screen.blit(personaje, (400, 50))

        nombre = self.personajerow["nombre"]
        descripcion = self.personajerow["descripcion"]

        #super().readText(descripcion)
        karma = self.personajerow["karma"]
        ataque = self.personajerow["ataque"]
        defensa = self.personajerow["defensa"]

        self.dibujarFondos(screen)
        nombre_rect= (525, 350)
        karma_rect = (825, 175)
        ataque_rect =  (825, 150)
        defensa_rect = (825, 125)
        addText(screen, nombre, "Karma: " + str(karma), "Ataque: " + str(ataque), "Defensa: " + str(defensa), nombre_rect, karma_rect, ataque_rect, defensa_rect)
        self.addDesc(screen, descripcion)
        super().render(screen)
        # Suponiendo que left_arrow es otra imagen que has cargado previamente
        # screen.blit(left_arrow, (500, 550))
        color_gris = (128, 128, 128)
        #only for test positions:
        debugtest = None

        self.activeGameState.set_karma(karma)
        self.activeGameState.set_ataque(ataque)
        self.activeGameState.set_defensa(defensa)
        self.activeGameState.set_nombre(nombre)
        self.activeGameState.set_imagen(self.personajerow["image"])

        if self.oldtext is None or self.oldtext != descripcion:
            self.oldtext = descripcion
            super().callReader(descripcion)
        pass


    def dibujarFondos(self, screen):
        rect_x = 200
        rect_y = 425
        rect_width = 550
        rect_height = 300
        color_interior = "#5a5a5a"
        color_borde = "#a5a5a5"
        dibujarFondos(screen, rect_x, rect_y, rect_width, rect_height, color_interior, color_borde)

        rect_x = 425
        rect_y = 330
        rect_width = 200
        rect_height = 40
        pygame.draw.rect(screen, color_interior, (rect_x - 4, rect_y - 4, rect_width + 8, rect_height + 8))
        pygame.draw.rect(screen, color_borde, (rect_x, rect_y, rect_width, rect_height))
        rect_x = 745
        rect_y = 100
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
            screen.blit(texto_renderizado, (225, 450 + i * fuente.get_height()))


    def selectButton(self, mouse_pos):

        if self.right_arrow != None and pos_rightarrow.collidepoint(mouse_pos):
            print("right")

            if self.posicionActual == len(self.personajes)-1:
                self.posicionActual = 0
            else:
                self.posicionActual = self.posicionActual + 1

        elif self.left_arrow != None and pos_leftarrow.collidepoint(mouse_pos):
            print("left")
            if self.posicionActual == 0:
                self.posicionActual = len(self.personajes)-1
            else:
                self.posicionActual = self.posicionActual - 1
        elif pos_image.collidepoint(mouse_pos):
            print(self.posicionActual)

    def selectCharacter(self, mouse_pos):
        if  pos_image.collidepoint(mouse_pos):
            print("enter")
            nextScene = GameFlowScene()
            nextScene.initScene(self.activeGameState)
            return nextScene
        return None

