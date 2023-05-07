import os

import pygame

from LeyendasEstelares.pantallas.inicio import crear_boton

background_image = pygame.image.load(os.path.join("recursos", os.path.join(os.path.join("imagenes", "nave")
                                                  , "skin_nave.png")))


def mostrarJuego(screen):
    # Dibujar la imagen de fondo

    screen.blit(background_image, (0, 0))

    # Actualizar la pantalla
    pygame.display.flip()


def mostrar_imagen(screen, imagen):
    # Dibujar la imagen de fondo

    background_image = pygame.image.load(imagen)
    screen.blit(background_image, (0, 0))

    # Actualizar la pantalla
    pygame.display.flip()

def mostrar_texto(screen, texto):
    # Dibujar la imagen de fondo

    background_color = (255, 255, 255)  # Blanco
    text_color = (0, 0, 0)  # Negro

    # Fuente y tamaño de fuente
    font_size = 24
    font = pygame.font.Font(None, font_size)

    # Texto
    text = texto
    text_surface = font.render(text, True, text_color)

    # Posición del texto
    text_rect = text_surface.get_rect()
    text_rect.centerx = 500
    text_rect.bottom = 600  # 10 píxeles desde la parte inferior

    rect_width = 900
    rect_height = int(768 * 0.25)  # 25% de la altura de la ventana

    # Posición del rectángulo
    rect_x = 0
    rect_y = 768 - rect_height

    # Dibuja el fondo y el rectángulo
    pygame.draw.rect(screen, background_color, (rect_x, rect_y, rect_width, rect_height))

    # Dibuja el fondo y el texto
    screen.blit(text_surface, text_rect)
    # Actualizar la pantalla
    pygame.display.flip()

def draw_mission_button(screen):

    screen_width = 710
    screen_height = 1350
    button =  crear_boton(screen_width, screen_height)
    normal_button_color = "#95584B"

    font = pygame.font.Font(None, 36)
    button_text = font.render("Mision", True, (0, 0, 0))
    pygame.draw.rect(screen, normal_button_color, button)
    screen.blit(button_text, button.topleft)
    pygame.display.flip()
    return button
