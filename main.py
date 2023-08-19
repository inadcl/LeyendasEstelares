# This is a sample Python script.
import os
from typing import Tuple

from Scenes.GameFlowScene import GameFlowScene
from Scenes.SceneManager import SceneManager
from Scenes.TitleScene import TitleScene
from data.GameState import GameState
from data.create_db import create_db

import pygame

from data.leermisiones import leer_mensaje_inicial
from jugador.jugador import Jugador
from pantallas import pantallasize

game_width = 1024
game_height = 768


if __name__ == '__main__':
    global new_game_button
    global last_color
    global jugador
    jugador: Jugador = None
    last_mouse_position = (0, 0)
    create_db()
    pygame.init()
    game_width = 1024
    game_height = 768
    screen_info = pygame.display.Info()
    screen_width = screen_info.current_w
    screen_height = screen_info.current_h
    scale_width = screen_width / game_width
    scale_height = screen_height / game_height
    scale = min(scale_width, scale_height)

    new_game_width = int(game_width * scale)
    new_game_height = int(game_height * scale)

    pantallasize.x_offset = (screen_width - new_game_width) // 2
    pantallasize.y_offset = (screen_height - new_game_height) // 2
    pantallasize.scale_width = scale_width
    pantallasize.scale_height = scale_height
    pantallasize.full_height = screen_info.current_h
    pantallasize.full_width = screen_info.current_w

    global full_width
    global full_height
    pygame.mixer.init()


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
        if scene_manager.current_scene != None and scene_manager.current_scene.restartGame():
            activeGameState = GameState()
            scene_manager = SceneManager(TitleScene(), GameFlowScene())
            scene_manager.initScene(activeGameState)

        activeScene.current_scene = scene_manager.switch_scene(scene_manager.current_scene)

        scene_manager.process_input(pygame.event.get(), pygame.key.get_pressed(), None)
        scene_manager.update()
        scene_manager.render(screen, activeGameState)
        pygame.display.flip()