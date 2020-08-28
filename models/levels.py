import pygame

class Level1:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.image = pygame.image.load('assets\\level1.png')
        self.packagesToDeliver = 10
        self.deliveryRange = (1414, 1577)

    def drawSelf(self, surface):
        surface.blit(self.image, (self.x, self.y))
