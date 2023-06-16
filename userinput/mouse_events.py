import random
import sys

import pygame

from jugador.jugador import Jugador
from pantallas.inicio import draw_button_by_state


def handle_mouse_click_general_actions(mission_button, exit_button, mouse_pos, misiones):
    if mission_button is not None and mission_button.collidepoint(mouse_pos):
        mision = random.choice(misiones)

        # Mostrar objeto seleccionado
        print(mision)

        # Eliminar objeto seleccionado de la lista
        if mision["repetible"]== False:
            misiones.remove(mision)
        return mision
    elif exit_button.collidepoint(mouse_pos):
        pygame.quit()
        sys.exit()
        return None
    return None

def hover_inicio_mouse_click(new_game_button, mouse_pos, screen):
        if new_game_button.collidepoint(mouse_pos):
                print("Hover on new game "+ str(mouse_pos[0]) +","+str(mouse_pos[1]))
                draw_button_by_state(screen, new_game_button, "Nuevo juego", True)
        else:
                print("Hover out of  new game "+ str(mouse_pos[0]) +","+ str(mouse_pos[1]))
                draw_button_by_state(screen, new_game_button, "Nuevo juego", False)
        pygame.display.flip()
