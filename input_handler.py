import pygame as pg
from pygame.locals import *

COMMANDS = [
    'AIM',
    'SHOOT',
    'HEAL',
    'SPECIAL',
    'LEFT',
    'RIGHT',
    'UP',
    'DOWN',
    'INTERACT',
    'MENU',
    'ATTACK',
    'DASH',
    'SWAP_WEAPON'
]

KEYBOARD_PRESSED = {
    pg.K_ESCAPE : 'MENU',
    pg.K_TAB : 'MENU',
    pg.K_RETURN : 'INTERACT',
    pg.K_e : 'ATTACK',
    pg.K_q : 'MENU',
    pg.K_r : 'SWAP_WEAPON',
    pg.K_w : 'UP',
    pg.K_UP : 'UP',
    pg.K_s : 'DOWN',
    pg.K_DOWN : 'DOWN',
    pg.K_a : 'LEFT',
    pg.K_LEFT : 'LEFT',
    pg.K_d : 'RIGHT',
    pg.K_RIGHT : 'RIGHT',
    pg.K_SPACE : 'DASH',
}

KEYBOARD_RELEASED = {
    pg.K_w : 'UP',
    pg.K_UP : 'UP',
    pg.K_s : 'DOWN',
    pg.K_DOWN : 'DOWN',
    pg.K_a : 'LEFT',
    pg.K_LEFT : 'LEFT',
    pg.K_d : 'RIGHT',
    pg.K_RIGHT : 'RIGHT',
}

CONTROLLER_BUTTONS = {          #Xbox       #PS4
    0 : 'DASH',                 #A          #X
    1 : 'SWAP_WEAPON',          #B          #Circle 
    2 : 'ATTACK',               #X          #Square
    3 : 'INTERACT',             #Y          #Triangle
    4 : 'HEAL',                 #LB         #Share
    5 : 'SPECIAL',              #RB         #PSX
    6 : 'INVENTORY',            #Back       #Options
    7 : 'MENU',                 #Start      #LS
    8 : None,                   #LS         #RS
    9 : None,                   #RS         #LB
    10 : None,                  #XBOX       #RB
    11 : None,                  #           #D-Up
    12 : None,                  #           #D-Down
    13 : None,                  #           #D-Left
    14 : None,                  #           #D-Right
    15 : None                   #           #Touch Pad Click
}

CONTROLLER_AXES = {
    0 : 'x1',       # LEFT STICK
    1 : 'y1',       # LEFT STICK
    2 : 'x2',       # RIGHT STICK
    3 : 'y2',       # RIGHT STICK
    5 : 'lt',       # LEFT TRIGGER
    6 : 'rt'        # RIGHT TRIGGER
}

### PS4/PS5 uses hat for DPAD
HAT_AXES = {
    (0,0) : 'none',
    (-1,0) : 'LEFT',
    (1,0) : 'RIGHT',
    (0,-1) : 'DOWN',
    (0,1) : 'UP',

    (-1,1) : 'UP',
    (1,-1) : 'DOWN',
    (-1,-1) : 'UP',
    (1,1) : 'DOWN'
}



actions = {key: False for key in COMMANDS}
running = True

def handle_events():
    global running
    for event in pg.event.get():
        if event.type == QUIT:
            running = False
        ### Flips the flag for the key true. Event handlers in the Game State flip it back after handling.
        if event.type == KEYDOWN:
            if event.key in KEYBOARD_PRESSED.keys():
                actions[KEYBOARD_PRESSED[event.key]] = True
        ### Flips the flag for certain keys false when released. Continuous values are handled by state.
        if event.type == KEYUP:
            if event.key in KEYBOARD_RELEASED.keys():
                actions[KEYBOARD_RELEASED[event.key]] = False    