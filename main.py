# This is a sample Python script.
from LeyendasEstelares.database.create_db import create_db

import pygame
import sys

from LeyendasEstelares.pantallas.inicio import mostrar_pantalla_inicio, handle_mouse_click, hover_mouse_click
from LeyendasEstelares.jugador.user import Usuario

screen_width = 1024
screen_height = 768
# Press Mayús+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.

usuario : Usuario = None

if __name__ == '__main__':
    global new_game_button
    global load_game_button
    create_db()
    pygame.init()

    # Define el tamaño de la pantalla de carga
    screen = pygame.display.set_mode((screen_width, screen_height))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if(new_game_button != None):
                    hover_mouse_click(new_game_button, load_game_button, mouse_pos)
            elif event.type == pygame.MOUSEMOTION:
                if usuario == None:
                    new_game_button, load_game_button = mostrar_pantalla_inicio(screen_width, screen_height, screen)
                    print(new_game_button)
                    pygame.display.flip()
                    mouse_pos = pygame.mouse.get_pos()
                    handle_mouse_click(new_game_button, load_game_button, mouse_pos)
