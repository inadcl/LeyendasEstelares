# This is a sample Python script.
import os
from typing import Tuple

from Scenes.GameFlowScene import GameFlowScene
from Scenes.SceneManager import SceneManager
from Scenes.TitleScene import TitleScene
from data.GameState import GameState
from data.create_db import create_db

import pyttsx3
import pygame
import sys

from data.leermisiones import leer_misiones
from jugador.jugador import Jugador
from pantallas.inicio import mostrar_pantalla_inicio
from pantallas.pantalladejuego import mostrarJuego, draw_mission_button, mostrar_imagen, mostrar_texto
from userinput.mouse_events import hover_inicio_mouse_click

screen_width = 1024
screen_height = 768


def sceneChanger(scene_manager):
    pass


if __name__ == '__main__':
    global new_game_button
    global last_color
    global jugador
    jugador: Jugador = None
    last_mouse_position = (0, 0)
    create_db()
    pygame.init()

    scene_manager = SceneManager(TitleScene(), GameFlowScene())
    screen = pygame.display.set_mode((screen_width, screen_height), pygame.DOUBLEBUF)
    gamestate = GameState()
    scene_manager.initScene(gamestate)
    while True:
        new_scene = scene_manager.process_input(pygame.event.get(), pygame.key.get_pressed(), None)
        if new_scene != None:
            scene_manager.switch_to_scene(new_scene)
        scene_manager.render(screen)
        pygame.display.flip()
        scene_manager.update()
        sceneChanger(scene_manager)

    # Define el tamaño de la pantalla de carga
    # screen = pygame.display.set_mode((screen_width, screen_height), pygame.DOUBLEBUF)
    # while True:
    #     for event in pygame.event.get():
    #         if event.type == pygame.QUIT:
    #             pygame.quit()
    #             sys.exit()
    #         elif event.type == pygame.MOUSEBUTTONDOWN:
    #             mouse_pos = pygame.mouse.get_pos()
    #             if jugador == None:
    #                 jugador = handle_inicio_mouse_click(mostrar_pantalla_inicio(screen_width, screen_height, screen),
    #                                                     draw_exit_by_state(screen), mouse_pos)
    #                 if jugador != None:
    #                     screen.fill((255, 255, 255))
    #             else:
    #
    #             if jugador is not None and jugador.vivo:
    #                 mostrarJuego(screen)
    #                 exit_button = draw_exit_by_state(screen)
    #                 mission_button = draw_mission_button(screen)
    #                 mision = handle_mouse_click_general_actions(mission_button, exit_button, mouse_pos, misiones)
    #                 if mision != None:
    #                     mostrar_imagen(screen, os.path.join("recursos", os.path.join("imagenes",
    #                                                                                  os.path.join("misiones",
    #                                                                                               mision["image"]))))
    #                     mostrarJuego(screen)
    #                     mostrar_texto(screen, mision["conversacion"])
    #         elif event.type == pygame.MOUSEMOTION:
    #             mouse_pos = pygame.mouse.get_pos()
    #             if jugador == None:
    #                 hover_inicio_mouse_click(mostrar_pantalla_inicio(screen_width, screen_height, screen), mouse_pos,
    #                                          screen)