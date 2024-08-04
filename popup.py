import pygame
from pygame.sprite import Group
from settings import *

class PopUp(pygame.sprite.Sprite):
    def __init__(self, *groups: Group) -> None:
        super().__init__(*groups)
        self.image = BUBBLE_IMAGE.convert_alpha()
        self.rect = self.image.get_rect()
        self.visible = False

    def draw(self) -> None:
        if self.visible:
            super().draw()