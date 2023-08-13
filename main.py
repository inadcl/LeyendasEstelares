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

from data.leermisiones import leer_misiones, leer_mensaje_inicial
from jugador.jugador import Jugador
from pantallas.inicio import mostrar_pantalla_inicio
from pantallas.pantalladejuego import mostrarJuego, draw_mission_button, mostrar_imagen, mostrar_texto
from userinput.mouse_events import hover_inicio_mouse_click

screen_width = 1024
screen_height = 768


if __name__ == '__main__':
    global new_game_button
    global last_color
    global jugador
    jugador: Jugador = None
    last_mouse_position = (0, 0)
    create_db()
    pygame.init()

    mensaje_inicial = leer_mensaje_inicial()
    scene_manager = SceneManager(TitleScene(), GameFlowScene())
    screen = pygame.display.set_mode((screen_width, screen_height), pygame.DOUBLEBUF)
    activeGameState = GameState()
    scene_manager.initScene(activeGameState)
    clock = pygame.time.Clock()
    activeScene = scene_manager.current_scene
    while True:
        clock.tick(60)# Esto limitará tu bucle a 60 iteraciones por segundo
        activeGameState.clock = clock
        activeScene.current_scene = scene_manager.switch_scene(scene_manager.current_scene)
        scene_manager.process_input(pygame.event.get(), pygame.key.get_pressed(), None)
        scene_manager.update()
        scene_manager.render(screen, activeGameState)
        pygame.display.flip()