import os

import pygame

from Scenes.Scene import Scene
import sys

from data.leermisiones import leer_personajes

class TitleScene(Scene):
    init = False

    def initScene(self):
        if self.init == False:
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

    def selectButton(self, mouse_pos):
        if self.right_arrow != None and self.right_arrow.get_rect().collidepoint(mouse_pos):
            self.posicionActual = self.posicionActual +1

        elif self.left_arrow != None and self.left_arrow.get_rect().collidepoint(mouse_pos):
            self.posicionActual = self.posicionActual - 1


    def update(self):
        pass

    def paintArrow(self, right, img):
        arrow = pygame.transform.flip(img, right, False)
        return arrow

    def render(self, screen):
        # screen.fill((255, 255, 255))

        # Obtiene la ruta al directorio del archivo actual.
        current_dir = os.path.dirname(os.path.abspath(__file__))

        # Construye la ruta a la imagen.
        image_path = os.path.join(current_dir, '..', 'recursos', 'imagenes', 'ui', 'background.png')
        rigth_arrow_path = os.path.join(current_dir, '..', 'recursos', 'imagenes', 'ui', 'rightarrow.png')

        left_arrow_path = os.path.join(current_dir, '..', 'recursos', 'imagenes', 'ui', 'leftarrow.png')
        if self.posicionActual > len(self.personajes):
            self.posicionActual = self.posicionActual -1
        elif  self.posicionActual < 0:
            self.posicionActual = 0
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
        karma = self.personajerow["karma"]
        ataque = self.personajerow["ataque"]
        defensa = self.personajerow["defensa"]

        self.addText(screen, nombre, descripcion, karma, ataque, defensa)
        super().render(screen)
        # Suponiendo que left_arrow es otra imagen que has cargado previamente
        # screen.blit(left_arrow, (500, 550))

        pygame.display.flip()
        pass

    def addText(self, screen, nombre, descripcion, karma, ataque, defensa):
        # Crear una fuente
        fuente = pygame.font.Font(None, 36)

        # Renderizar el texto con fondo
        fondo = fuente.render(nombre, True, "#0000ff")  # Renderizar el texto en un fondo azul

        # Obtener las dimensiones del fondo
        fondo_rect = fondo.get_rect()

        # Centrar el fondo en la ventana
        fondo_rect.center = (525, 350)
        screen.blit(fondo, fondo_rect)

        lineas = self.wraptext(descripcion, fuente, 500)
        for i, linea in enumerate(lineas):
            texto_renderizado = fuente.render(linea, True, "#0000ff")
            screen.blit(texto_renderizado, (225, 450 + i * fuente.get_height()))

        fondo = fuente.render("karma: " + str(karma), True, "#0000ff")  # Renderizar el texto en un fondo azul

        # Obtener las dimensiones del fondo
        fondo_rect = fondo.get_rect()

        # Centrar el fondo en la ventana
        fondo_rect.center = (825, 175)
        screen.blit(fondo, fondo_rect)

        fondo = fuente.render("ataque: " + str(ataque), True, "#0000ff")  # Renderizar el texto en un fondo azul

        # Obtener las dimensiones del fondo
        fondo_rect = fondo.get_rect()

        # Centrar el fondo en la ventana
        fondo_rect.center = (825, 150)
        screen.blit(fondo, fondo_rect)

        fondo = fuente.render("defensa: " + str(defensa), True, "#0000ff")  # Renderizar el texto en un fondo azul

        # Obtener las dimensiones del fondo
        fondo_rect = fondo.get_rect()

        # Centrar el fondo en la ventana
        fondo_rect.center = (825, 120)
        screen.blit(fondo, fondo_rect)

    def wraptext(self, texto, fuente, width):
        lineas = []
        palabras = texto.split()
        linea_actual = palabras[0]
        for palabra in palabras[1:]:
            if fuente.size(linea_actual + " " + palabra)[0] <= width:
                linea_actual += " " + palabra
            else:
                lineas.append(linea_actual)
                linea_actual = palabra
        lineas.append(linea_actual)
        return lineas
