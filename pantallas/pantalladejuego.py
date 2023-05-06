import os

import pygame

background_image = pygame.image.load(os.path.join("recursos", os.path.join(os.path.join("imagenes", "nave")
                                                  , "skin_nave.png")))


def mostrarJuego(screen):
    # Dibujar la imagen de fondo

    screen.blit(background_image, (0, 0))

    # Actualizar la pantalla
    pygame.display.flip()
