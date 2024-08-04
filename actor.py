import pygame
import time
import input_handler as Input
from health import Health
from settings import *
from sprite_sheet import Animator
from ai import AI
from dialogue import Dialogue

class Actor(pygame.sprite.Sprite):
    def __init__(self, parent, pos, collision_sprites, groups):
        super().__init__(groups)
        self.parent = parent
        self.collision_sprites = collision_sprites
        self.actions = {value: False for value in Input.COMMANDS}
        self.animator = Animator()
        self.image = self.animator.image
        self.rect = self.image.get_rect()
        self.hitbox = pygame.rect.FRect((0,0,14,12))
        self.hitbox.centerx, self.hitbox.centery = pos
        self.facing = 'IDLE_DOWN'
        #Movement
        self.direction = pygame.math.Vector2()
        self.walk_speed = 2
        self.sprint_speed = 4
        self.move_speed = self.walk_speed
    
    def move(self, dt):
        self.move_speed = self.walk_speed
        self.direction.x = self.actions['RIGHT'] - self.actions['LEFT']
        self.direction.y = self.actions['DOWN'] - self.actions['UP']
        if self.direction.magnitude() != 0:
            self.direction.normalize()
        self.hitbox.centerx += self.direction.x * self.move_speed * dt
        self.check_collision('x')
        self.hitbox.centery += self.direction.y * self.move_speed * dt
        self.check_collision('y')

    def check_collision(self, dir):
        if dir == 'x':
            for sprite in self.collision_sprites:
                if sprite.rect.colliderect(self.hitbox):
                    if self.direction.x > 0: #moving right
                        self.hitbox.right = sprite.rect.left
                    if self.direction.x < 0: #moving left
                        self.hitbox.left = sprite.rect.right
        if dir == 'y':
            for sprite in self.collision_sprites:
                if sprite.rect.colliderect(self.hitbox):
                    if self.direction.y > 0: #moving down
                        self.hitbox.bottom = sprite.rect.top
                    if self.direction.y < 0: #moving up
                        self.hitbox.top = sprite.rect.bottom
                    
    def update(self, dt):
        self.move(dt)
        self.update_state()
        self.image = self.animator.animate(self.facing)
        self.rect.center = self.hitbox.midbottom + HUMAN_COLLISION_OFFSET 

    def update_state(self):
        face = self.facing.split('_')
        heading = ['IDLE', '_', face[1]]
        if self.direction.y > 0:
            heading[-1] = 'DOWN'
            heading[0] = 'WALK'
        elif self.direction.y < 0:
            heading[-1] = 'UP'
            heading[0] = 'WALK'
        if self.direction.x > 0:
            heading[-1] = 'RIGHT'
            heading[0] = 'WALK'
        elif self.direction.x < 0:
            heading[-1] = 'LEFT'
            heading[0] = 'WALK'
        self.facing = ''.join(heading)

#######################################################
###########                                 ###########
###########         PLAYER CONTROL          ###########
###########                                 ###########
#######################################################

class Player(Actor):
    def __init__(self, pos, colliders, groups, attack_one, attack_one_destroy, max_health):
        super().__init__(self, pos, colliders, groups)
        self.interacting = False
        self.interact_area = pygame.Rect(0,0,64,64)
        self.interact_area.center = self.rect.center
        self.attack_one = attack_one
        self.attack_one_destroy = attack_one_destroy
        self.attacking = False
        self.attack_time = None
        self.attack_cooldown = .05
        #Properties
        self.health = Health(max_hp=max_health)
        self.inventory = {}
        self.player_class = {'class_name': 'warlock', 'level' : 1}
        self.xp = 465
        self.level = 1
        self.stats = {'XP': '0', 'HP': 100, 'RP' : 50}

    def update(self, dt,):
        if not self.interacting:
            self.handle_input()
            self.cooldown()
            super().update(dt)
            self.interact_area.center = self.rect.center

    def handle_input(self):
        for action in self.actions:            
            self.actions[action] = Input.actions[action]
        if Input.actions['ATTACK'] and not self.attacking:
            self.attacking = True
            self.attack_time = time.time()
            self.attack_one()

    def cooldown(self):
        current_time = time.time()
        if self.attacking:
            if current_time - self.attack_time >= self.attack_cooldown:
                self.attacking = False
                self.attack_one_destroy()

    def interact(self, talkers):
        for sprite in talkers:
            if sprite.hitbox.colliderect(self.interact_area):
                if not self.interacting:
                    self.interacting = True
                    sprite.interacting = True
                    return sprite
                else:
                    self.interacting = False
                    sprite.interacting = False
        return None

    def gain_xp(self, amount):
        self.xp += amount
        if self.xp >= XP_TO_LEVEL[self.level]:
            self.level += 1
            self.xp -= XP_TO_LEVEL[self.level -1]


#######################################################
###########                                 ###########
###########         ENEMY  CONTROL          ###########
###########                                 ###########
#######################################################

class Enemy(Actor):
    def __init__(self, pos, player, ai_type, colliders, groups, max_health, enemy_class):
        super().__init__(self, pos, colliders, groups)
        self.player = player
        self.ai = AI(self, ai_type)
        self.health = Health(max_hp=max_health)
        self.enemy_class = enemy_class
        self.vulnerable = True
        self.damage_time = None
        self.damage_cooldown = .05

    def update(self, dt, actions=None):
        self.ai.choose_action()
        self.cooldown()
        self.check_death()
        super().update(dt)

    def take_damage(self, amount):
        if self.vulnerable:
            self.damage_time = time.time()
            self.vulnerable = False
            self.health.take_damage(amount)

    def check_death(self):
        if self.health.current_hp <= 0:
            self.kill()
            #death sound
            #death animation
            #grant XP
            self.player.gain_xp(self.enemy_class.xp)


    def cooldown(self):
        current_time = time.time()
        if not self.vulnerable:
            if current_time - self.damage_time >= self.damage_cooldown:
                self.vulnerable = True
                

#######################################################
###########                                 ###########
###########         N P C  CONTROL          ###########
###########                                 ###########
#######################################################

class NPC(Actor):
    def __init__(self, pos, player, ai_type, colliders, groups):
        super().__init__(self, pos, colliders, groups)
        self.interacting = False
        self.player = player
        self.ai = AI(self, ai_type)
        #choose which topics this NPC can converse on.
        self.dialogue_choices = ['hello', 'bye', 'money']
        self.dialogue = Dialogue(self.dialogue_choices)

    def update(self, dt, actions=None):
        if not self.interacting:
            self.ai.perform()
            super().update(dt)
