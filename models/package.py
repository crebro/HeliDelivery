import pygame

class Package:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.image = pygame.transform.scale(pygame.image.load('assets\\delivery.png'),( 50, 70))

    def moveDown(self, surface, surfaceWidth):
        if self.y < surfaceWidth//2-self.image.get_height():
            self.y += 1
            surface.blit(self.image, (self.x, self.y))
      