import os
import random

import pygame

from Scenes.MiniGameManager import MiniGameManager
from Scenes.Scene import Scene, screen_width, screen_height
from data.DrawUtils import addText, dibujarFondos
from data.leermisiones import leer_misiones, leer_mensaje_inicial
from data.stringutils import debugRect, wraptext

#TODO
# hover en el boton de navegar cuando sea accesible
# hover en  de navegar cuando sea accesible
# Añadir eventos con combtaes


class GameFlowScene(Scene):
    def __init__(self, activeGameState=None):
        self.current_dir = os.path.dirname(os.path.abspath(__file__))
        self.folder = 'ui'
        self.filename = 'background.png'
        self.readingProcess = None
        self.lastTextReaded = ""
        self.oldtext = ""
        self.misionActual = None
        self.opcionA = None
        self.opcionB = None
        self.alien = None
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
            texto_renderizado = fuente.render("    "+opcionA["texto"], True, "#0000ff")
            screen.blit(texto_renderizado, (250, 735))
        if opcionB != None and "texto" in opcionB.keys():
            texto_renderizado = fuente.render("    "+opcionB["texto"], True, "#0000ff")
            screen.blit(texto_renderizado, (525, 735))

        # add input buttons

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
                return self.selectButton(mouse_pos)
        return None

    def selectButton(self, mouse_pos):

        print(mouse_pos)
        if pygame.Rect(25, 375, 150, 150).collidepoint(mouse_pos):
            if self.opcionA == None and self.opcionB == None:
                print("selected: new mission")
                randMisionPosition = random.randint(0, len(self.activeGameState.misiones) - 1)
                randMission = self.activeGameState.misiones[randMisionPosition]
                if not randMission["repetible"]:
                    self.activeGameState.misiones.remove(randMission)
                # asignamos la nueva mision
                self.misionActual = randMission
                self.conversacionActual = self.misionActual["conversacion"]
                self.opcionA = self.misionActual["opciones"][0]
                self.opcionB = self.misionActual["opciones"][1]
                self.folder = "misiones"
                self.filename = self.misionActual["image"]
                if "alien" in self.misionActual.keys():
                    self.alien = self.misionActual["alien"]
                else:
                    self.alien = None
                self.renderRequired = True

        if self.opcionA != None and pygame.Rect(250, 725, 200, 40).collidepoint(mouse_pos):
            self.renderRequired = True
            print("opcionA selected")
            if "minijuego" in self.opcionA["accion"].keys():
                self.minijuego=self.opcionA["accion"]["minijuego"]
                if self.minijuego == "starfight":
                    self.next_scene = MiniGameManager(self, "starfight", self.misionActual["alien"], self.activeGameState)
                    if self.next_scene != None:
                        self.switch_to_scene(self.next_scene)
                        return self.next_scene
            else:
                self.aplicar_opcion(self.opcionA)
        if self.opcionB != None and pygame.Rect(525, 725, 200, 40).collidepoint(mouse_pos):
            self.renderRequired = True
            print("opcionB")
            if "minijuego" in self.opcionB["accion"].keys():
                self.minijuego=self.opcionB["accion"]["minijuego"]
                if self.minijuego == "starfight":
                    self.next_scene = MiniGameManager(self, "starfight", self.misionActual["alien"], self.activeGameState)
                    if self.next_scene != None:
                        self.switch_to_scene(self.next_scene)
                        return self.next_scene
            else:
                self.aplicar_opcion(self.opcionB)

    def aplicar_opcion(self, opcionSeleccionada):
        if "consecuencias" in opcionSeleccionada["accion"].keys():
            opcionSeleccionada["accion"]["texto"] + "\n" + opcionSeleccionada["accion"]["consecuencias"]
        self.conversacionActual = opcionSeleccionada["accion"]["texto"]
        if "karma" in opcionSeleccionada["accion"].keys():
            self.activeGameState.tratar_karma(opcionSeleccionada["accion"]["karma"])
        if "defensa" in opcionSeleccionada["accion"].keys():
            self.activeGameState.tratar_defensa(opcionSeleccionada["accion"]["defensa"])
        if "ataque" in opcionSeleccionada["accion"].keys():
            self.activeGameState.tratar_ataque(opcionSeleccionada["accion"]["ataque"])
        if "opciones" in opcionSeleccionada["accion"].keys():
            opcionA = opcionSeleccionada["accion"]["opciones"][0]
            opcionB = opcionSeleccionada["accion"]["opciones"][1]
            self.opcionA = opcionA
            self.opcionB = opcionB
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
            if self.alien == None:
                self.dibujarAlien(screen, 'personajes', "ruido.png")
            else:
                self.dibujarAlien(screen, "aliens", self.alien["image"])

            nombre_rect = (900, 740)
            karma_rect = (970, 625)
            ataque_rect = (970, 650)
            defensa_rect = (970, 675)
            addText(screen, self.activeGameState.nombre, "K: " + str(self.activeGameState.karma),
                    "A: " + str(self.activeGameState.ataque), "D: " + str(self.activeGameState.defensa), nombre_rect,
                    karma_rect, ataque_rect, defensa_rect)
            message = ""
            #        self.misionActual = leer_misiones()[self.misionActual]
            if self.misionActual == None:
                self.addInitialDesc(screen, leer_mensaje_inicial())
            else:
                self.addDescription(screen, self.conversacionActual, self.opcionA, self.opcionB)
            super().render(screen)
            # posicion avatar
            pass

    def dibujarFondos(self, screen):
        # descripcion
        rect_x = 200
        rect_y = 425
        rect_width = 550
        rect_height = 300
        color_interior = "#5a5a5a"
        color_borde = "#a5a5a5"
        dibujarFondos(screen, rect_x, rect_y, rect_width, rect_height, color_interior, color_borde)

        # avatar
        rect_x = 770
        rect_y = 550
        rect_width = 240
        rect_height = 210
        dibujarFondos(screen, rect_x, rect_y, rect_width, rect_height, color_interior, color_borde)

        # alien
        rect_x = 25
        rect_y = 575
        rect_width = 150
        rect_height = 150
        dibujarFondos(screen, rect_x, rect_y, rect_width, rect_height, color_interior, color_borde)

        # dado
        rect_x = 850
        rect_y = 375
        rect_width = 150
        rect_height = 150
        dibujarFondos(screen, rect_x, rect_y, rect_width, rect_height, color_interior, color_borde)

        # salto
        rect_x = 25
        rect_y = 375
        rect_width = 150
        rect_height = 150
        dibujarFondos(screen, rect_x, rect_y, rect_width, rect_height, color_interior, color_borde)

        # opciones dialogo
        if self.opcionA != None:
            rect_x = 525
            rect_y = 725
            rect_width = 200
            rect_height = 40
            dibujarFondos(screen, rect_x, rect_y, rect_width, rect_height, color_interior, color_borde)

        # opcion2 option
        if self.opcionB != None:
            rect_x = 250
            rect_y = 725
            rect_width = 200
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
        personaje_image = pygame.transform.scale(pygame.image.load(personaje), (150, 150))
        screen.blit(personaje_image, pygame.Rect(775, 575, 150, 150))

    def dibujarUI(self, screen):
        personaje = os.path.join('recursos', 'imagenes', 'ui', "turbo.png")
        personaje_image = pygame.transform.scale(pygame.image.load(personaje), (150, 150))
        screen.blit(personaje_image, pygame.Rect(25, 375, 150, 150))

        personaje = os.path.join('recursos', 'imagenes', 'ui', "dado.png")
        personaje_image = pygame.transform.scale(pygame.image.load(personaje), (150, 150))
        screen.blit(personaje_image, pygame.Rect(850, 375, 150, 150))

    def dibujarAlien(self, screen, folder, imagen):
        personaje = os.path.join('recursos', 'imagenes', folder, imagen)
        numeros = [90, 180, 270, 360]

        numero_aleatorio = 0
        if imagen == "ruido.png":
            numero_aleatorio = random.choice(numeros)
        personaje_image = pygame.transform.rotate(pygame.transform.scale(pygame.image.load(personaje), (150, 150)),
                                                  numero_aleatorio)
        screen.blit(personaje_image, pygame.Rect(25, 575, 150, 150))
