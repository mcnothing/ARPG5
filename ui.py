import pygame
from support import *
from settings import *
from actor import Player

###
### Show the health, resource, and experience bars.
### Show the currently available abilities
### Show the equipped weapon/spell
### Show the current class and level?
### Show a character portrait?
### Show a minimap?

class UI:
    def __init__(self, screen):
        self.display_surface = screen
        self.font = pygame.font.Font(FONT_FILE, 12)
        self.health_bar_rect = pygame.Rect(30, GAME_HEIGHT - 12, 100, 10)
        self.resource_bar_rect = pygame.Rect(160, GAME_HEIGHT - 12, 100, 10)
        self.xp_bar_rect = pygame.Rect(290, GAME_HEIGHT - 12, 100, 10)
        self.character_class_text_rect = pygame.Rect(GAME_WIDTH - 80, GAME_HEIGHT - 12, 70, 10)
        
    def show_text(self, text, bg_rect):
        text_surface = self.font.render(text, False, 'white')
        text_rect = text_surface.get_rect(bottomright = bg_rect.bottomleft)
        self.display_surface.blit(text_surface, text_rect)

    def show_bar_title(self, title, bar):
        text_surface = self.font.render(title, False, 'white')
        text_rect = text_surface.get_rect(bottomright = bar.bottomleft)
        self.display_surface.blit(text_surface, text_rect)

    def show_vertical_bar(self, title, current, maximum, bg_rect, color):
        #bar title
        self.show_bar_title(title, bg_rect)
        #bar background
        pygame.draw.rect(self.display_surface, 'black', bg_rect)
        ratio = current / maximum
        width = bg_rect.width * ratio
        current_rect = bg_rect.copy()
        current_rect.width = width
        #bar content
        pygame.draw.rect(self.display_surface, color, current_rect)
        #bar outline
        pygame.draw.rect(self.display_surface, 'grey', bg_rect, 1)

    def display(self, player):
        self.show_vertical_bar('HP', player.health.current_hp, player.health.max_hp, self.health_bar_rect, 'firebrick2')
        self.show_vertical_bar('RP',35, player.stats['RP'], self.resource_bar_rect, 'dodgerblue')
        self.show_vertical_bar('XP', player.xp, XP_TO_LEVEL[player.level], self.xp_bar_rect, 'gold1')
        self.show_text(player.player_class['class_name'], self.character_class_text_rect)

        