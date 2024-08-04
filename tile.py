import pygame

class Tile(pygame.sprite.Sprite):
    def __init__(self, image, pos, groups):
        super().__init__(groups)
        self.image = image
        self.rect = self.image.get_rect(midtop = pos)

    def update(self, dt, actions=None):
        super().update()