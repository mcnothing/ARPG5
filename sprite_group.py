from typing import Iterable, Iterator, Union, Any
import pygame
from settings import *
from pygame.sprite import AbstractGroup

class CameraGroupYSort(pygame.sprite.Group):
    def __init__(self, *sprites: Any | AbstractGroup | Iterable) -> None:
        super().__init__(*sprites)
        self.debug = False
        self.debug_color = pygame.Color(0,255,255,64)
        self.offset = pygame.math.Vector2()
        self.offset_x = GAME_WIDTH / 2
        self.offset_y = GAME_HEIGHT / 2

    def get_camera_target_position(self, target) -> None:
        self.offset.x = target.rect.centerx - self.offset_x
        self.offset.y = target.rect.centery - self.offset_y

    def custom_draw(self, screen: pygame.surface, player) -> None:
        self.get_camera_target_position(player)
        for sprite in sorted(self.sprites(), key = lambda sprite: sprite.rect.centery):
            sprite_offset = sprite.rect.topleft - self.offset
            screen.blit(sprite.image, sprite_offset)
            if self.debug:
                if hasattr(sprite, 'hitbox'):
                    hitbox_pos = sprite.hitbox.topleft - self.offset
                    hitbox_surface = pygame.Surface((14,12), pygame.SRCALPHA)
                    hitbox_surface.fill(self.debug_color)
                    hitbox_rect = pygame.FRect(hitbox_pos.x, hitbox_pos.y, sprite.hitbox.width, sprite.hitbox.height)
                    screen.blit(hitbox_surface, hitbox_rect)
                if hasattr(sprite, 'path'):
                    points = sprite.ai.path
                    x = points[0][0] - self.offset.x
                    y = points[0][1] - self.offset.y
                    w = points[-1][0] - points[0][0]
                    h = points[-1][0] - points[0][0]
                    rect = pygame.FRect((x, y), (w,h) )
                    pygame.draw.rect(screen, self.debug_color, rect, 1)

class CameraGroup(pygame.sprite.Group):
    def __init__(self, *sprites: Any | AbstractGroup | Iterable) -> None:
        super().__init__(*sprites)
        self.offset = pygame.math.Vector2()
        self.offset_x = 320
        self.offset_y = 180

    def get_camera_target_position(self, target) -> None:
        self.offset.x = target.rect.centerx - self.offset_x
        self.offset.y = target.rect.centery - self.offset_y

    def custom_draw(self, screen: pygame.surface, player) -> None:
        self.get_camera_target_position(player)
        for sprite in self.sprites():
            sprite_offset = sprite.rect.topleft - self.offset
            screen.blit(sprite.image, sprite_offset)