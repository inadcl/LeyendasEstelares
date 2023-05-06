import pygame
import sys

from pygame import Rect

new_game_button:Rect=None
load_game_button:Rect=None

def mostrar_pantalla_inicio(screen_width, screen_height, screen):

    # Define el tipo de letra y tamaño
    font = pygame.font.Font(None, 50)

    # Crea el mensaje de la pantalla de carga
    text = font.render("Juega una nueva partida o carga la anterior", True, (0, 0, 0))

    # Centra el mensaje en la pantalla de carga
    text_rect = text.get_rect()
    text_rect.center = (screen_width // 2, screen_height // 2)
    bg_color = (255, 255, 255)
    # Dibuja el mensaje en la pantalla de cargas
    screen.fill(bg_color)
    screen.blit(text, text_rect)
    return dibujar_botones(screen, screen_width, screen_height)



def dibujar_botones(screen, screen_width, screen_height):

    # Definir el tamaño y la posición de los botones
    button_width = 200
    button_height = 50
    button_padding = 20

    new_game_button = pygame.Rect(screen_width // 2 - button_width // 2,
                                  screen_height // 2 - button_height - button_padding, button_width, button_height)
    load_game_button = pygame.Rect(screen_width // 2 - button_width // 2, screen_height // 2 + button_padding,
                                   button_width, button_height)

    # Definir el texto de los botones
    font = pygame.font.Font(None, 36)

    new_game_text = font.render("Nuevo juego", True, (0, 0, 0))
    load_game_text = font.render("Cargar partida", True, (0, 0, 0))

    # Dibujar los botones en la pantalla de carga
    # Define el color de fondo de la pantalla de carga
    bg_color = (255, 255, 255)
    # Dibuja el mensaje en la pantalla de cargas
    pygame.draw.rect(screen, (200, 200, 200), new_game_button)
    pygame.draw.rect(screen, (200, 200, 200), load_game_button)
    screen.blit(new_game_text, new_game_button.center)
    screen.blit(load_game_text, load_game_button.center)


    return new_game_button, load_game_button

def handle_mouse_click(new_game_button, load_game_button,mouse_pos):
        if new_game_button.collidepoint(mouse_pos):
            print("Clicked on new game")

        if load_game_button.collidepoint(mouse_pos):
            print("Clicked on load game")


def hover_mouse_click(new_game_button, load_game_button, mouse_pos):
        if new_game_button.collidepoint(mouse_pos):
            print("hover on new game")

        if load_game_button.collidepoint(mouse_pos):
            print("hover on load game")