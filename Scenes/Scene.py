import subprocess
import sys

import pygame

from data.GameState import GameState
from pantallas.inicio import draw_exit_by_state

screen_width = 1024
screen_height = 768

class Scene:
    lastTextReaded=""
    activeGameState:GameState;
    def callReader(self, text):
        if (self.lastTextReaded != text and text != None):
            try:
                self.closeReader()
            except:
                print("trying to stop last speak instance")
            self.lastTextReaded = text
            from subprocess import call
            self.readingProcess = subprocess.Popen(["python", "speak.py", text])
    def __init__(self):
        self.readingProcess = None
        self.lastTextReaded= ""
        self.switch_on = False
        pass

    def initScene(self, activeGameState):
        self.activeGameState = activeGameState
        pass


    def exitScene(self):
        pass

    def closeReader(self):
        if self.readingProcess != None:
            self.readingProcess.terminate()
            self.readingProcess.wait()
    def process_input(self, events, pressed_keys, button):
        for event in events:
            self.exitcheck(event)
            if event.type == pygame.MOUSEBUTTONDOWN:
                print("boton presionado")
                mouse_pos = pygame.mouse.get_pos()
                self.closeReader()
                self.exitbutton(mouse_pos)
        return False

    def exitbutton(self, mouse_pos):
        if self.exit_button != None and self.exit_button.collidepoint(mouse_pos):
            pygame.quit()
            sys.exit()

    def exitcheck(self, event):
        if event.type == pygame.QUIT:
                self.closeReader()
                pygame.quit()
                sys.exit()
                return None


    def update(self):
        pass

    def render(self, screen):
        self.exit_button = draw_exit_by_state(screen)
        return self.exit_button

    def add_new_scene(self, next_scene):
        self.next_scene = next_scene

    def get_new_scene(self):
        if not self.switch_on:
            return None

        return self.next_scene