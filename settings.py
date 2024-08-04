import pygame
from support import *

#game settings
FPS = 60
GAME_WIDTH = 640
GAME_HEIGHT = 360
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
FONT_SIZE = 14
EMPTY = pygame.Color(0,0,0,0)

TILE_SIZE = 16
BLANK_TILE = '-1'

ORIGIN = (0,0)
HUMAN_COLLISION_OFFSET = pygame.Vector2(0, -10)

GAME_RESOLUTION = (GAME_WIDTH, GAME_HEIGHT)
SCREEN_RESOLUTION = (SCREEN_WIDTH, SCREEN_HEIGHT)

#External File locations
FONT_FILE = 'assets/fonts/joystix.ttf'
CURSOR_FILE = 'assets/sprites/cursor.png'
PAUSE_MENU = 'assets/sprites/menu.png'

# SPRITE FILES
SPRITE_FOLDER = 'assets/sprites'

#Audio
MUSIC_VOLUME = 0.1
MUSIC_FOLDER = 'assets/music'
SOUNDS_FOLDER = 'assets/audio'

SOUNDS = {
    'CONFIRM' : 'confirmation_001',
    'CLICK' : 'click_001',
    'ERROR' : 'error_001',
    'FOOTSTEP' : 'footstep_004'
}



#######################################
##### CHARACTER PROGRESSION ###########
#######################################

XP_TO_LEVEL = {
    #current_level : goal_XP
    1 : 500,
    2 : 750,
    3 : 1250,
    4 : 2000,
    5 : 3250,
    6 : 5250,
    7 : 8500,
    8 : 13750,
    9 : 22250,
    10 : 36000
}