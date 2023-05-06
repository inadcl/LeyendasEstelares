from turtledemo import clock

import pygame
import sys

from pygame import Rect
from pygame.locals import Color

global last_mouse
def mostrar_pantalla_inicio(screen_width, screen_height, screen):
    # Define el tipo de letra y tamaño
    font = pygame.font.Font(None, 50)

    # Crea el mensaje de la pantalla de carga
    text = font.render("Juega una nueva partida o carga la anterior", True, (0, 0, 0))

    # Centra el mensaje en la pantalla de carga
    text_rect = text.get_rect()
    text_rect.center = (screen_width // 2, screen_height // 2 - (screen_height * 0.2))
    bg_color = (255, 255, 255)
    # Dibuja el mensaje en la pantalla de cargas
    screen.fill(bg_color)
    screen.blit(text, text_rect)

    pygame.display.flip()
    return crear_boton(screen, screen_width, screen_height)


def crear_boton(screen, screen_width, screen_height):
    button_width = 200
    button_height = 50
    button_padding = 20

    new_game_button = pygame.Rect(screen_width // 2 - button_width // 2,
                                  screen_height // 2 - button_height - button_padding, button_width, button_height)
    # draw_button_by_state(screen, new_game_button, "Nuevo juego", False)

    return new_game_button


def draw_button_by_state(screen, button, text, hover):
    bg_button_color = (200, 200, 200)
    normal_button_color = "#95584B"

    font = pygame.font.Font(None, 36)
    button_text = font.render(text, True, (0, 0, 0))
    if hover:
        pygame.draw.rect(screen, bg_button_color, button)
    else:
        pygame.draw.rect(screen, normal_button_color, button)
    screen.blit(button_text, button.topleft)
    pygame.display.flip()
    return button


def handle_mouse_click(new_game_button, mouse_pos, screen):
    if new_game_button.collidepoint(mouse_pos):
        print("Clicked on new game")


def hover_mouse_click(new_game_button, mouse_pos, screen):
        if new_game_button.collidepoint(mouse_pos):
                print("Hover on new game "+ str(mouse_pos[0]) +","+str(mouse_pos[1]))
                draw_button_by_state(screen, new_game_button, "Nuevo juego", True)
        else:
                print("Hover out of  new game "+ str(mouse_pos[0]) +","+ str(mouse_pos[1]))
                draw_button_by_state(screen, new_game_button, "Nuevo juego", False)
        pygame.display.flip()

