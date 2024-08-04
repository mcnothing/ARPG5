import pygame as pg
import audio_handler as Audio
from settings import *

SPRITE_SIZE = 64

WALK = [0, 1, 2, 3, 4, 5]
RUN = [0, 1, 6, 3, 4, 7]

class SpriteSheet:
    def __init__(self, file_name):
        try:
            self.sheet = pg.image.load(file_name).convert_alpha()
        except pg.error as e:
            print(f'Unable to load spritesheet image: {file_name}')
            raise SystemExit(e)

    def image_at(self, rectangle):
        rect = pg.Rect(rectangle)
        image = pg.Surface(rect.size, pg.SRCALPHA)
        image.blit(self.sheet, (0, 0), rect)
        return image
    
    def images_at(self, rects):
        return [self.image_at(rect) for rect in rects]
    
    def load_strip(self, rect: pg.rect, count: int) -> list:
        tups = [(rect[0]+rect[2]*x, rect[1], rect[2], rect[3]) for x in range(count)]
        return self.images_at(tups)


class Animator:
    def __init__(self):
        self.frame = 0
        self.frame_trigger = False
        self.animation_speed = .20 # lower is slower
        self.anim_states = [
            'IDLE_DOWN', 'IDLE_UP', 'IDLE_RIGHT', 'IDLE_LEFT',
            'WALK_DOWN', 'WALK_UP', 'WALK_RIGHT', 'WALK_LEFT',
            'RUN_DOWN', 'RUN_UP', 'RUN_RIGHT', 'RUN_LEFT']
        self.animation_frames = {}
        self.load_images()
        self.image = self.animation_frames['IDLE_DOWN'][0]
        self.last_frame = 0
        
    def load_images(self):
        size_x = 16
        size_y = 24
        y_order = [1,0,1,2]
        directions = {'DOWN' : 4, 'UP' : 0, 'RIGHT' : 2, 'LEFT' : 6}
        #[4,0,2,6] D U R L
        sheet = SpriteSheet('assets/sprites/PrototypeCharacter24x16.png')
        for state in self.anim_states:
            dir = state.split('_')[-1]
            if 'IDLE' in state:
                rect = pg.Rect((directions[dir] * size_x, size_y, size_x, size_y))                
                self.animation_frames[state] = [sheet.image_at(rect)]
            if 'WALK' in state:
                self.animation_frames[state] = sheet.images_at([(directions[dir] * size_x, y * size_y, size_x, size_y) for y in y_order])
            if 'RUN' in state:
                self.animation_frames[state] = sheet.images_at([(directions[dir] * size_x, y * size_y, size_x, size_y) for y in y_order])


    def animate(self, state):
        #update frames on all layers
        self.frame += self.animation_speed
        if self.frame >= len(self.animation_frames[state]):
            self.frame = 0
        self.image = self.animation_frames[state][int(self.frame)]
        self.event(int(self.frame), state)
        return self.image
    
    def event(self, frame, state):
        if not 'IDLE' in state:
            key_frames = [0,3]
            if frame == self.last_frame:
                return
            if frame in key_frames: 
                self.last_frame = frame
                self.frame_trigger = True
            else:
                self.frame_trigger = False
            if self.frame_trigger:
                Audio.play_sound(SOUNDS['FOOTSTEP'])
