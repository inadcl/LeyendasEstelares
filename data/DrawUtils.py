import pygame


def addAlienText(screen, nombre, karma, ataque, defensa, nombre_rect, karma_rect, ataque_rect, defensa_rect, text_size, stats_size):

    # Crear una fuente
    fuente = pygame.font.Font(None, text_size)

    # Renderizar el texto con fondo
    fondo = fuente.render(nombre, True, "#0000ff")  # Renderizar el texto en un fondo azul

    # Obtener las dimensiones del fondo
    fondo_rect = fondo.get_rect()

    # Centrar el fondo en la ventana
    fondo_rect.center = nombre_rect
    screen.blit(fondo, fondo_rect)

    fuente = pygame.font.Font(None, stats_size)
    fondo = fuente.render(karma, True, "#0000ff")  # Renderizar el texto en un fondo azul

    # Obtener las dimensiones del fondo
    fondo_rect = fondo.get_rect()

    # Centrar el fondo en la ventana
    fondo_rect.center = karma_rect
    screen.blit(fondo, fondo_rect)

    fondo = fuente.render(ataque, True, "#0000ff")  # Renderizar el texto en un fondo azul

    # Obtener las dimensiones del fondo
    fondo_rect = fondo.get_rect()

    # Centrar el fondo en la ventana
    fondo_rect.center = ataque_rect
    screen.blit(fondo, fondo_rect)

    fondo = fuente.render(defensa, True, "#0000ff")  # Renderizar el texto en un fondo azul

    # Obtener las dimensiones del fondo
    fondo_rect = fondo.get_rect()

    # Centrar el fondo en la ventana
    fondo_rect.center = defensa_rect
    screen.blit(fondo, fondo_rect)

def addText(screen, nombre, karma, ataque, defensa, nombre_rect, karma_rect, ataque_rect, defensa_rect, text_size):

    # Crear una fuente
    fuente = pygame.font.Font(None, text_size)

    # Renderizar el texto con fondo
    fondo = fuente.render(nombre, True, "#0000ff")  # Renderizar el texto en un fondo azul

    # Obtener las dimensiones del fondo
    fondo_rect = fondo.get_rect()

    # Centrar el fondo en la ventana
    fondo_rect.center = nombre_rect
    screen.blit(fondo, fondo_rect)

    fondo = fuente.render(karma, True, "#0000ff")  # Renderizar el texto en un fondo azul

    # Obtener las dimensiones del fondo
    fondo_rect = fondo.get_rect()

    # Centrar el fondo en la ventana
    fondo_rect.center = karma_rect
    screen.blit(fondo, fondo_rect)

    fondo = fuente.render(ataque, True, "#0000ff")  # Renderizar el texto en un fondo azul

    # Obtener las dimensiones del fondo
    fondo_rect = fondo.get_rect()

    # Centrar el fondo en la ventana
    fondo_rect.center = ataque_rect
    screen.blit(fondo, fondo_rect)

    fondo = fuente.render(defensa, True, "#0000ff")  # Renderizar el texto en un fondo azul

    # Obtener las dimensiones del fondo
    fondo_rect = fondo.get_rect()

    # Centrar el fondo en la ventana
    fondo_rect.center = defensa_rect
    screen.blit(fondo, fondo_rect)


def dibujarFondos(screen, rect_x, rect_y, rect_width, rect_height, color_interior, color_borde):
    pygame.draw.rect(screen, color_interior, (rect_x - 4, rect_y - 4, rect_width + 8, rect_height + 8))
    pygame.draw.rect(screen, color_borde, (rect_x, rect_y, rect_width, rect_height))