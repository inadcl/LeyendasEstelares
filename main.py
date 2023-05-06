# This is a sample Python script.
from typing import Tuple

from LeyendasEstelares.database.create_db import create_db

import pygame
import sys

from LeyendasEstelares.jugador.jugador import Jugador
from LeyendasEstelares.pantallas.inicio import mostrar_pantalla_inicio, handle_mouse_click, hover_mouse_click, \
    draw_exit_by_state
from LeyendasEstelares.pantallas.pantalladejuego import mostrarJuego

screen_width = 1024
screen_height = 768


# Press Mayús+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.

if __name__ == '__main__':
    global new_game_button
    global last_color
    global jugador
    jugador:Jugador = None
    last_mouse_position = (0, 0)
    create_db()
    pygame.init()

    # Define el tamaño de la pantalla de carga
    screen = pygame.display.set_mode((screen_width, screen_height), pygame.DOUBLEBUF)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                exit_button = draw_exit_by_state(screen)
                if jugador == None:
                    jugador = handle_mouse_click(mostrar_pantalla_inicio(screen_width, screen_height, screen), draw_exit_by_state(screen), mouse_pos)
                    if jugador!= None:
                        screen.fill((255, 255, 255))
                else:
                    handle_mouse_click(None, draw_exit_by_state(screen), mouse_pos)
            elif event.type == pygame.MOUSEMOTION:
                mouse_pos = pygame.mouse.get_pos()
                if jugador == None:
                    hover_mouse_click(mostrar_pantalla_inicio(screen_width, screen_height, screen), mouse_pos, screen)
            if jugador is not None and jugador.vivo:
                mostrarJuego(screen)
                exit_button = draw_exit_by_state(screen)
