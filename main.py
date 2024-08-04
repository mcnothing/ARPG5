import pygame as pg
import input_handler as Input
import time
import sys
from state import Title
from settings import *


class Game:
    def __init__(self):
        pg.init()
        pg.display.set_caption('Outskirts')
        self.font = pg.font.Font(FONT_FILE, FONT_SIZE)
        self.running = True
        self.playing = True
        self.screen = pg.Surface(GAME_RESOLUTION) # Game Resolution
        self.window = pg.display.set_mode(SCREEN_RESOLUTION, vsync=1) # Screen resolution is game resolution scaled up to screen size
        self.clock = pg.Clock()
        self.joystick = pg.joystick.Joystick(0)
        self.state_stack = []
        self.prev_time = time.time()
        self.load_states()

    def main_loop(self):
        while self.playing:
            dt = (time.time() - self.prev_time) * 30
            self.prev_time = time.time()
            self.get_events()
            self.update(dt)
            self.render()
            self.clock.tick(FPS)
            if not self.running:
                pg.quit()
            
    def get_events(self):
        Input.handle_events()
        self.running = Input.running

    def update(self, dt):
        self.state_stack[-1].update(dt)        

    def render(self):
        self.state_stack[-1].render(self.screen)
        pg.transform.scale(self.screen, SCREEN_RESOLUTION, self.window)
        pg.display.flip()
        
    def load_states(self):
        self.title_screen = Title(self)
        self.state_stack.append(self.title_screen)

    def draw_text(self, surface, text, color, x, y) -> None:
        text_surface = self.font.render(text, False, color)
        text_rect = text_surface.get_rect()
        text_rect.center = (x, y)
        surface.blit(text_surface, text_rect)


if __name__ == '__main__':
    game = Game()
    while game.running:
        game.main_loop()
    pg.time.wait(250) #allow sound to finish playing
    pg.quit()
    sys.exit()
