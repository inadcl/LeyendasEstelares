import pygame


class Misil:
    def __init__(self, position):
        self.image = pygame.Surface((20, 5))
        self.image.fill((255, 0, 0))  # Un misil rojo como ejemplo
        self.rect = self.image.get_rect(topleft=position)
        self.velocidad = 1000

    def update(self, dt):
        self.rect.x += self.velocidad * dt


    def render(self, screen):
        screen.blit(self.image, self.rect.topleft)