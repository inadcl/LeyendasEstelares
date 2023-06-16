import sys

import pygame

from pantallas.inicio import draw_exit_by_state

screen_width = 1024
screen_height = 768

class Scene:
    def __init__(self):
        pass

    def initScene(self):
        pass

    def exitScene(self):
        pass
    def process_input(self, events, pressed_keys, button):
        for event in events:
            self.exitcheck(event)
            if event.type == pygame.MOUSEBUTTONDOWN:
                print("boton presionado")
                mouse_pos = pygame.mouse.get_pos()
                self.exitbutton(mouse_pos)

    def exitbutton(self, mouse_pos):
        if self.exit_button != None and self.exit_button.collidepoint(mouse_pos):
            pygame.quit()
            sys.exit()

    def exitcheck(self, event):
        if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                return None


    def update(self):
        pass

    def render(self, screen):
        self.exit_button = draw_exit_by_state(screen)
        return self.exit_button

    def switch_to_scene(self, next_scene):
        self.next = next_scene