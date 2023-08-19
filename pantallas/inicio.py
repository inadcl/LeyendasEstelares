
import pygame
from pantallas import pantallasize

global last_mouse


def crear_boton(screen_width, screen_height):
    button_width = 200
    button_height = 50
    button_padding = 20

    new_game_button = pygame.Rect(pantallasize.getWidthPosition(screen_width // 2 - button_width // 2),
                                  pantallasize.getHeightPosition(screen_height // 2 - button_height - button_padding), button_width, button_height)

    return new_game_button


def draw_exit_by_state(screen):

    button =  crear_boton(210, 210)
    normal_button_color = "#95584B"

    font = pygame.font.Font(None, 36)
    button_text = font.render("Exit", True, (0, 0, 0))
    pygame.draw.rect(screen, normal_button_color, button)
    screen.blit(button_text, button.topleft)
    return button

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
    #pygame.display.flip()
    return button

