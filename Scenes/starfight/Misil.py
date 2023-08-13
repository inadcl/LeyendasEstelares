import pygame


class Misil:
    def __init__(self, position):
        self.image = pygame.Surface((20, 5))
        self.image.fill((255, 0, 0))  # Un misil rojo como ejemplo
        self.rect = self.image.get_rect(topleft=position)
        self.velocidad = 1000
        self.live = True

    def update(self, dt, right):
        if right:
            self.rect.x += self.velocidad * dt
        else:
            self.rect.x -= self.velocidad * dt

    def render(self, screen):
        screen.blit(self.image, self.rect.topleft)