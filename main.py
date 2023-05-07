# This is a sample Python script.
import os
from typing import Tuple

from LeyendasEstelares.data.create_db import create_db

import pygame
import sys

from LeyendasEstelares.data.leermisiones import leer_misiones
from LeyendasEstelares.jugador.jugador import Jugador
from LeyendasEstelares.pantallas.inicio import mostrar_pantalla_inicio, \
    draw_exit_by_state
from LeyendasEstelares.pantallas.pantalladejuego import mostrarJuego, draw_mission_button, mostrar_imagen, mostrar_texto
from LeyendasEstelares.userinput.mouse_events import hover_inicio_mouse_click, handle_inicio_mouse_click, \
    handle_mouse_click_general_actions

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
    jugador: Jugador = None
    last_mouse_position = (0, 0)
    create_db()
    misiones = leer_misiones()
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
                    jugador = handle_inicio_mouse_click(mostrar_pantalla_inicio(screen_width, screen_height, screen),
                                                        draw_exit_by_state(screen), mouse_pos)
                    if jugador != None:
                        screen.fill((255, 255, 255))
                else:
                    mission_button = draw_mission_button(screen)
                    handle_inicio_mouse_click(mission_button, draw_exit_by_state(screen), mouse_pos)

                if jugador is not None and jugador.vivo:
                    mostrarJuego(screen)
                    exit_button = draw_exit_by_state(screen)
                    mission_button = draw_mission_button(screen)
                    mision = handle_mouse_click_general_actions(mission_button, exit_button, mouse_pos, misiones)
                    if mision != None:
                        mostrar_imagen(screen, os.path.join("recursos", os.path.join("imagenes",
                                                                                     os.path.join("misiones",
                                                                                                  mision["image"]))))
                        mostrarJuego(screen)
                        mostrar_texto(screen, mision["conversacion"])
            elif event.type == pygame.MOUSEMOTION:
                mouse_pos = pygame.mouse.get_pos()
                if jugador == None:
                    hover_inicio_mouse_click(mostrar_pantalla_inicio(screen_width, screen_height, screen), mouse_pos,
                                             screen)