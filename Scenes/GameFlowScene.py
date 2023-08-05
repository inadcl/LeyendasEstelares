import os
import random

import pygame

from Scenes.Scene import Scene, screen_width, screen_height
from data.DrawUtils import addText, dibujarFondos
from data.leermisiones import leer_misiones, leer_mensaje_inicial
from data.stringutils import debugRect, wraptext


class GameFlowScene(Scene):
    def __init__(self, activeGameState=None):
        self.current_dir = os.path.dirname(os.path.abspath(__file__))
        self.folder= 'ui'
        self.filename='background.png'
        self.readingProcess = None
        self.lastTextReaded= ""
        self.oldtext = ""
        self.misionActual = None
        self.opcionA = None
        self.opcionB = None
        self.renderRequired = True
        if activeGameState is not None:
            self.initScene(activeGameState)

    def addInitialDesc(self, screen, mensaje_inicial):

        # Crear una fuente
        fuente = pygame.font.Font(None, 20)

        lineas = wraptext(mensaje_inicial, fuente, 500)
        for i, linea in enumerate(lineas):
            texto_renderizado = fuente.render(linea, True, "#0000ff")
            screen.blit(texto_renderizado, (225, 450 + i * fuente.get_height()))


        if self.oldtext is None or self.oldtext != mensaje_inicial:
            self.oldtext = mensaje_inicial
            super().callReader(mensaje_inicial)

    def addDescription(self, screen, mensaje_inicial, opcionA, opcionB):

        # Crear una fuente
        fuente = pygame.font.Font(None, 20)

        lineas = wraptext(mensaje_inicial, fuente, 500)
        for i, linea in enumerate(lineas):
            texto_renderizado = fuente.render(linea, True, "#0000ff")
            screen.blit(texto_renderizado, (225, 450 + i * fuente.get_height()))


        if self.oldtext is None or self.oldtext != mensaje_inicial:
            self.oldtext = mensaje_inicial
            super().callReader(mensaje_inicial)

        if opcionA != None and "texto" in opcionA.keys():
            texto_renderizado = fuente.render(opcionA["texto"], True, "#0000ff")
            screen.blit(texto_renderizado, (325, 725))
        if opcionB != None and "texto" in opcionB.keys():
            texto_renderizado = fuente.render(opcionB["texto"], True, "#0000ff")
            screen.blit(texto_renderizado, (525, 725))
        #add input buttons


    def initScene(self, activeGameState):
        super().initScene(activeGameState)
        self.activeGameState = activeGameState
        print("Scene loaded")
        pass
    def process_input(self, events, pressed_keys, button):
        super().process_input(events, pressed_keys, button)
        # handle_inicio_mouse_click(mission_button, draw_exit_by_state(screen), pygame.mouse.get_pos())
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self.selectButton(mouse_pos)
        return None

    def selectButton(self, mouse_pos):

        print(mouse_pos)
        if pygame.Rect(25,375,150,150).collidepoint(mouse_pos):
            print("right")
            randMisionPosition = random.randint(0, len(self.activeGameState.misiones)-1)
            randMission = self.activeGameState.misiones[randMisionPosition]
            if not randMission["repetible"]:
                self.activeGameState.misiones.remove(randMission)
            #todo draw mission
            self.misionActual = randMission
            self.conversacionActual = self.misionActual["conversacion"]
            self.opcionA = self.misionActual["opciones"][0]
            self.opcionB = self.misionActual["opciones"][1]
            self.folder = "misiones"
            self.filename = self.misionActual["image"]
            self.renderRequired=True


        if self.opcionA != None and pygame.Rect(325,725,100,40).collidepoint(mouse_pos):
            self.renderRequired=True
            print("opcionA")
            if "consecuencias" in self.opcionA["accion"].keys():
                self.opcionA["accion"]["texto"] +  "\n" + self.opcionA["accion"]["consecuencias"]
            self.conversacionActual = self.opcionA["accion"]["texto"]
            if "karma" in self.opcionA["accion"].keys():
                self.activeGameState.tratar_karma(self.opcionA["accion"]["karma"])
            if "opciones" in self.opcionA["accion"].keys():
                self.opcionB = self.opcionA["accion"]["opciones"][1]
                self.opcionA = self.opcionA["accion"]["opciones"][0]
            else:
                self.opcionA = None
                self.opcionB = None
        if self.opcionB != None and pygame.Rect(525, 725, 100, 40).collidepoint(mouse_pos):
            self.renderRequired=True
            print("opcionB")
            if "consecuencias" in self.opcionB["accion"].keys():
                self.opcionB["accion"]["texto"] +  "\n" + self.opcionA["accion"]["consecuencias"]
            self.conversacionActual = self.opcionB["accion"]["texto"]
            if "karma" in self.opcionB["accion"].keys():
                self.activeGameState.tratar_karma(self.opcionB["accion"]["karma"])
            if "opciones" in self.opcionB["accion"].keys():
                self.opcionA = self.opcionB["accion"]["opciones"][0]
                self.opcionB = self.opcionB["accion"]["opciones"][1]
            else:
                self.opcionA = None
                self.opcionB = None



    def update(self):
        pass

    def generateImagePath(self, folder, filename):
        return os.path.join(self.current_dir, '..', 'recursos', 'imagenes', folder, filename)

    def render(self, screen, activeGameState):
        if not self.renderRequired:
            return
        else:
            self.renderRequired = False
            self.activeGameState = activeGameState
            screen.fill((255, 255, 255))
            image_path = self.generateImagePath(self.folder, self.filename)
            background = pygame.image.load(image_path)
            screen.blit(background, (0, 0))
            self.dibujarNave(screen)
            self.dibujarFondos(screen)
            self.dibujarUI(screen)



            # Actualizar la pantalla

            image_path = self.activeGameState.imagen
            self.dibujarPersonaje(screen, image_path)
            self.dibujarAlien(screen, "ruido.png")

            nombre_rect= (900, 740)
            karma_rect = (970, 625)
            ataque_rect =  (970, 650)
            defensa_rect = (970, 675)
            addText(screen, self.activeGameState.nombre, "K: " + str(self.activeGameState.karma), "A: " + str(self.activeGameState.ataque), "D: " + str(self.activeGameState.defensa), nombre_rect, karma_rect, ataque_rect, defensa_rect)
            message = ""
    #        self.misionActual = leer_misiones()[self.misionActual]
            if self.misionActual == None:
                self.addInitialDesc(screen, leer_mensaje_inicial())
            else:
                self.addDescription(screen, self.conversacionActual, self.opcionA, self.opcionB)
            super().render(screen)
            #posicion avatar
            pass

    def dibujarFondos(self, screen):
        #descripcion
        rect_x = 200
        rect_y = 425
        rect_width = 550
        rect_height = 300
        color_interior = "#5a5a5a"
        color_borde = "#a5a5a5"
        dibujarFondos(screen, rect_x, rect_y, rect_width, rect_height, color_interior, color_borde)

        #avatar
        rect_x = 770
        rect_y = 550
        rect_width = 240
        rect_height = 210
        dibujarFondos(screen, rect_x, rect_y, rect_width, rect_height, color_interior, color_borde)

        #alien
        rect_x = 25
        rect_y = 575
        rect_width = 150
        rect_height = 150
        dibujarFondos(screen, rect_x, rect_y, rect_width, rect_height, color_interior, color_borde)

        #dado
        rect_x = 850
        rect_y = 375
        rect_width = 150
        rect_height = 150
        dibujarFondos(screen, rect_x, rect_y, rect_width, rect_height, color_interior, color_borde)

        #salto
        rect_x = 25
        rect_y = 375
        rect_width = 150
        rect_height = 150
        dibujarFondos(screen, rect_x, rect_y, rect_width, rect_height, color_interior, color_borde)


        #opciones dialogo
        pos_rightarrow = pygame.Rect(525, 725, 100, 40)
        #debugRect(screen,color_interior, pos_rightarrow)
        rect_x = 525
        rect_y = 725
        rect_width = 100
        rect_height = 40
        dibujarFondos(screen, rect_x, rect_y, rect_width, rect_height, color_interior, color_borde)

        #opcion2 option
        #pos_rightarrow = pygame.Rect(325, 725, 100, 40)
        #debugRect(screen,color_interior, pos_rightarrow)
        rect_x = 325
        rect_y = 725
        rect_width = 100
        rect_height = 40
        dibujarFondos(screen, rect_x, rect_y, rect_width, rect_height, color_interior, color_borde)
    def dibujarNave(self, screen):
        background_image = pygame.image.load(os.path.join("recursos", os.path.join(os.path.join("imagenes", "nave")
                                                                                   , "skin_nave.png")))
        screen.blit(background_image, (0, 0))
        avatar_image = pygame.image.load(os.path.join("recursos", os.path.join(os.path.join("imagenes", "nave")
                                                                                   , "skin_nave.png")))
        screen.blit(background_image, (0, 0))
        pygame.Rect(775, 575, 150, 150)
        pass

    def dibujarPersonaje(self, screen, imagen):
        personaje = os.path.join('recursos', 'imagenes', 'personajes', imagen)
        personaje_image = pygame.transform.scale(pygame.image.load(personaje), (150,150))
        screen.blit(personaje_image, pygame.Rect(775, 575, 150, 150))

    def dibujarUI(self, screen):
        personaje = os.path.join('recursos', 'imagenes', 'ui', "turbo.png")
        personaje_image = pygame.transform.scale(pygame.image.load(personaje), (150,150))
        screen.blit(personaje_image, pygame.Rect(25, 375, 150, 150))

        personaje = os.path.join('recursos', 'imagenes', 'ui', "dado.png")
        personaje_image = pygame.transform.scale(pygame.image.load(personaje), (150,150))
        screen.blit(personaje_image, pygame.Rect(850, 375, 150, 150))
    def dibujarAlien(self, screen, imagen):
        personaje = os.path.join('recursos', 'imagenes', 'personajes', imagen)
        numeros = [90, 180, 270, 360]

        numero_aleatorio = 0
        if imagen == "ruido.png":
            numero_aleatorio = random.choice(numeros)
        personaje_image = pygame.transform.rotate(pygame.transform.scale(pygame.image.load(personaje), (150, 150)), numero_aleatorio)
        screen.blit(personaje_image, pygame.Rect(25, 575, 150, 150))
