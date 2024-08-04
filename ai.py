import time
import pygame
from random import choice

class AI:
    def __init__(self, parent, ai_type):
        self.parent = parent
        self.ai_type = ai_type
        self.action_choice_time = time.time()
        self.action_choice_cooldown = 3
        self.target = None
        self.path_index = 0
        self.distance = 0
        self.ai_actions = {
            'follow' : self.follow_path,
            'random' : self.choose_action
        }

    def choose_action(self):
        '''Random walk and wait behavior'''
        current_time = time.time()
        if current_time - self.action_choice_time >= self.action_choice_cooldown:
            option = choice([0, 1, 2, 2,2,2])
            for direction in self.parent.actions.keys():
                self.parent.actions[direction] = False
            match option:
                case 0:
                    self.parent.actions[choice(['UP', 'DOWN', 'LEFT', 'RIGHT'])] = True
                case 1:
                    self.parent.actions[choice(['UP', 'DOWN'])] = True
                    self.parent.actions[choice(['LEFT', 'RIGHT'])] = True
                case 2:
                    for direction in self.parent.actions.keys():
                        self.parent.actions[direction] = False
            self.action_choice_time = current_time

    def perform(self):
        self.ai_actions[self.ai_type]()

    def set_path(self, path):
        self.path = path

    def get_distance(self):
        c = pygame.math.Vector2(self.parent.hitbox.center)
        t = pygame.math.Vector2(self.target)
        return (c - t).length()

    def follow_path(self):
        if self.path is not None:
            self.target = self.path[self.path_index]
            if self.get_distance() < 2:
                self.path_index +=1 
                if self.path_index >= len(self.path):
                    self.path_index = 0
            else:
                self.move_towards()

    def move_towards(self):
        actions = self.parent.actions
        for a in actions:
            actions[a] = False
        c = pygame.math.Vector2(self.parent.hitbox.center)
        t = pygame.math.Vector2(self.target)
        if c.x - t.x > 1:
            actions['LEFT'] = True
        if c.x - t.x < -1:
            actions['RIGHT'] = True
        if c.y - t.y > 1:
            actions['UP'] = True
        if c.y - t.y < -1:
            actions['DOWN'] = True
        
        

        

