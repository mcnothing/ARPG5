import pygame as pg
import audio_handler as Audio
import input_handler as Input
from settings import *
from level import Level


class State:
    def __init__(self, game):
        self.game = game
        self.prev_state = None

    def update(self, dt):
        pass

    def render(self, surface):
        pass

    def enter_state(self):
        if len(self.game.state_stack) > 0:
            self.prev_state = self.game.state_stack[-1]
        self.game.state_stack.append(self)

    def exit_state(self):
        self.game.state_stack.pop()


class Title(State):
    def __init__(self, game):
        super().__init__(game)
        Audio.load_music_track('TITLE_SCREEN')
        Audio.play_music_track(True)

    def update(self, dt):
        if Input.actions['INTERACT']:
            Input.actions['INTERACT'] = False
            print('ENTER')
            new_state = MainMenu(self.game)
            new_state.enter_state()

    def draw_title_info(self, display):
        self.game.draw_text(display, 'WELCOME TO GAME!', (0,0,0), 320, 180)
        self.game.draw_text(display, 'Press Start to Begin!', (64,64,64), 320, 220)

    def render(self, display):
        display.fill((255,255,255))
        self.draw_title_info(display)
        

class MainMenu(State):
    def __init__(self, game):
        super().__init__(game)
        self.menu = ['NEW GAME', 'RESUME', 'LOAD GAME', 'SAVE GAME', 'OPTIONS', 'QUIT']
        self.menu_header = 'MAIN MENU'
        self.cursor_image = pg.image.load(CURSOR_FILE)
        self.cursor_rect = self.cursor_image.get_rect()
        self.cursor_y = 180
        self.cursor_rect.x = 260
        self.index = 0

    def update(self, dt):
        self.update_cursor()
        if Input.actions['INTERACT']:
            Input.actions['INTERACT'] = False
            self.select_option()
        elif Input.actions['SWAP_WEAPON']:
            Input.actions['SWAP_WEAPON'] = False
            Audio.play_sound(SOUNDS['CONFIRM'])
            new_state = QuitMenu(self.game)
            new_state.enter_state()
        
    def render(self, display):
        display.fill((200, 200, 200))
        self.draw_menu(display)
        display.blit(self.cursor_image, self.cursor_rect)

    def select_option(self):
        if self.menu[self.index] == 'NEW GAME':
            Audio.play_sound(SOUNDS['CONFIRM'])
            new_state = GameState(self.game) # eventually, need a character creation state between main menu and gameworld
            new_state.enter_state()
        elif self.menu[self.index] == 'RESUME':
            Audio.play_sound(SOUNDS['ERROR'])
        elif self.menu[self.index] == 'LOAD GAME':
            Audio.play_sound(SOUNDS['CONFIRM'])
            new_state = LoadGameMenu(self.game)
            new_state.enter_state()
        elif self.menu[self.index] == 'SAVE GAME':
            Audio.play_sound(SOUNDS['CONFIRM'])
            new_state = SaveGameMenu(self.game)
            new_state.enter_state()
        elif self.menu[self.index] == 'OPTIONS':
            Audio.play_sound(SOUNDS['CONFIRM'])
            new_state = OptionsMenu(self.game)
            new_state.enter_state()
        elif self.menu[self.index] == 'QUIT':
            Audio.play_sound(SOUNDS['CONFIRM'])
            new_state = QuitMenu(self.game)
            new_state.enter_state()

    def update_cursor(self):
        if Input.actions['DOWN']:
            Input.actions['DOWN'] = False
            Audio.play_sound(SOUNDS['CLICK'])
            self.index = (self.index + 1) % len(self.menu)
        elif Input.actions['UP']:
            Input.actions['UP'] = False
            Audio.play_sound(SOUNDS['CLICK'])
            self.index = (self.index - 1) % len(self.menu)
        self.cursor_rect.y = self.cursor_y + (self.index * 20)
    
    # draw main menu
    def draw_menu(self, display):
        self.game.draw_text(display, self.menu_header, (0,0,0,), 320, 150)
        for y, option in enumerate(self.menu):
            self.game.draw_text(display, option, (0,0,0,), 320, (180 + (y * 20)))


class LoadGameMenu(MainMenu):
    def __init__(self, game):
        super().__init__(game)
        self.menu = ['Fake Save Game 1', 'Fake Save Game 2', 'Fake Save Game 3', 'BACK']
        self.menu_header = 'LOAD GAME'

    def select_option(self):
        if self.menu[self.index] == 'BACK':
            Audio.play_sound(SOUNDS['CONFIRM'])
            self.game.state_stack.pop()


class SaveGameMenu(MainMenu):
    def __init__(self, game):
        super().__init__(game)
        self.menu = ['NEW SAVE', 'Fake Save Game 1', 'Fake Save Game 2', 'Fake Save Game 3', 'BACK']
        self.menu_header = 'SAVE GAME'

    def select_option(self):
        if self.menu[self.index] == 'BACK':
            Audio.play_sound(SOUNDS['CONFIRM'])
            self.game.state_stack.pop()


class OptionsMenu(MainMenu):
    def __init__(self, game):
        super().__init__(game)
        self.menu = ['SOUND', 'MUSIC', 'BACK']
        self.menu_header = 'OPTIONS'

    def select_option(self):
        if self.menu[self.index] == 'BACK':
            Audio.play_sound(SOUNDS['CONFIRM'])
            self.game.state_stack.pop()
        elif self.menu[self.index] == 'SOUND':
            Audio.play_sound(SOUNDS['CONFIRM'])
            Audio.toggle_sound()
        elif self.menu[self.index] == 'MUSIC':
            Audio.play_sound(SOUNDS['CONFIRM'])
            Audio.toggle_music()


class QuitMenu(MainMenu):
    def __init__(self, game):
        super().__init__(game)
        self.menu = ['NO', 'YES']
        self.menu_header = 'REALLY QUIT?'

    def select_option(self):
        if self.menu[self.index] == 'NO':
            Audio.play_sound(SOUNDS['CONFIRM'])
            self.game.state_stack.pop()
        if self.menu[self.index] == 'YES':
            Audio.play_sound(SOUNDS['CONFIRM'])
            self.game.playing = False
            self.game.running = False


class GameState(State):
    def __init__(self, game):
        super().__init__(game)
        self.level = Level(self.game.screen)
        self.player = self.level.create_map()        
        Audio.music.stop()
        
    def update(self, dt):
        # Check if the game was paused 
        if Input.actions['MENU']:
            Input.actions['MENU'] = False
            new_state = PauseMenu(self.game)
            new_state.enter_state()
        if Input.actions['INTERACT']:
            Input.actions['INTERACT'] = False
            target = self.player.interact(self.level.talkers)
            if target is not None:
                new_state = ConversationState(self.game, self.player, target)
                new_state.enter_state()
        if Input.actions['DASH']:
            Input.actions['DASH'] = False
            self.level.actors.debug = not self.level.actors.debug
        self.level.run(dt)
        
    def render(self, display):
        self.level.render()
        

class PauseMenu(State):
    def __init__(self, game) -> None:
        self.game = game
        super().__init__(game)
        # Set the menu
        self.menu_img = pg.image.load(PAUSE_MENU)
        self.menu_rect = self.menu_img.get_rect()
        self.menu_rect.center = (GAME_WIDTH *.85, GAME_HEIGHT *.4)
        # Set the cursor and menu states
        self.menu_options = {0 :'Party', 1 : 'Items', 2 :'Magic', 3 : 'Exit'}
        self.index = 0
        self.cursor_img = pg.image.load(CURSOR_FILE)
        self.cursor_rect = self.cursor_img.get_rect()
        self.cursor_pos_y = self.menu_rect.y + 38
        self.cursor_rect.x, self.cursor_rect.y = self.menu_rect.x + 10, self.cursor_pos_y

    def update(self, dt):
        self.update_cursor()
        if Input.actions['INTERACT']:  #'e'
            Input.actions['INTERACT'] = False
            self.transition_state()
        if Input.actions['SWAP_WEAPON']:  #'q'
            Input.actions['SWAP_WEAPON'] = False
            self.exit_state()
        

    def render(self, display):
        # render the gameworld behind the menu, which is right before the pause menu on the stack
        # self.game.state_stack[-2].render(display)
        self.prev_state.render(display)
        self.game.draw_text(display, 'Paused', (0,0,0), 320, 180)
        display.blit(self.menu_img, self.menu_rect)
        display.blit(self.cursor_img, self.cursor_rect)

    def transition_state(self):
        if self.menu_options[self.index] == 'Party': 
            new_state = PartyMenu(self.game)
            new_state.enter_state()
        elif self.menu_options[self.index] == 'Items': 
            pass # TO-DO
        elif self.menu_options[self.index] == 'Magic': 
            pass # TO-DO
        elif self.menu_options[self.index] == 'Exit': 
            while len(self.game.state_stack) > 2:
                self.game.state_stack.pop()

    def update_cursor(self):
        if Input.actions['DOWN']:
            Input.actions['DOWN'] = False
            self.index = (self.index + 1) % len(self.menu_options)
        elif Input.actions['UP']:
            Input.actions['UP'] = False
            self.index = (self.index - 1) % len(self.menu_options)
        self.cursor_rect.y = self.cursor_pos_y + (self.index * 32)


class ConversationState(State):
    def __init__(self, game, player, target):
        super().__init__(game)
        self.font = pg.font.Font(FONT_FILE, FONT_SIZE)
        self.player = player
        self.target = target
        self.dialog_rect = pg.Rect(180, GAME_HEIGHT- 112, 200, 100)
        self.dialogue_index = 0
        self.dialogue = self.target.dialogue.get_topic('hello')

    def update(self, dt):
        if Input.actions['INTERACT']:
            self.player.interacting = False
            self.target.interacting = False
            self.exit_state()
        if Input.actions['DASH']:
            Input.actions['DASH'] = False
            self.next_line()
        

    def render(self, display):
        self.prev_state.render(display)
        self.game.draw_text(display, 'conversing!', (0,0,0), 320, 180)
        self.show_dialog(self.dialog_rect, display)
        
    def next_line(self):
        print
        self.dialogue_index += 1
        if self.dialogue_index >= len(self.dialogue):
            self.dialogue_index = 0

    def show_dialog(self, bg_rect, display):
        if self.player.interacting:
            #dialog background
            pg.draw.rect(display, 'black', bg_rect)
            #dialog outline
            pg.draw.rect(display, 'grey', bg_rect, 1)
            #wrap text onto background rect
            text = self.dialogue[self.dialogue_index]
            wrap_text(display, text, 'white', bg_rect, self.font)


class PartyMenu(State):
    def __init__(self, game):
        super().__init__(game)
        self.game = game
        
    def update(self, dt):
        if Input.actions['SWAP_WEAPON']:
            Input.actions['SWAP_WEAPON'] = False
            self.exit_state()
        

    def render(self, display):
        display.fill((255,255,255))
        self.game.draw_text(display, 'PARTY MENU GOES HERE', (0,0,0), GAME_WIDTH / 2, GAME_HEIGHT / 2 )
