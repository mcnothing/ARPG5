from random import choice
from tile import Tile
from settings import *
from ui import UI
from actor import *
from objects import Weapon
from character_classes import EnemyClass, PlayerClass
from sprite_group import CameraGroupYSort, CameraGroup
from pytmx.util_pygame import load_pygame


class Level:
    def __init__(self, screen):
        self.screen = screen
        self.visible_sprites = CameraGroup()
        self.obstacles = CameraGroupYSort()
        self.actors = CameraGroupYSort()
        self.attack_sprites = pygame.sprite.Group()
        self.attackable_sprites = pygame.sprite.Group()
        self.talkers = pygame.sprite.Group()
        self.ui = UI(screen)
        self.player = None
        self.player_attack = None
        self.map = {'ground' : {}, 'boundary' : {}, 'upper' : {}}
        self.map_name = self.change_map()
        #self.change_map()
        
    def create_player(self):
        return 0

    def change_map(self):
        return choice(['assets/maps/ARPG5_1.tmx'])#, 'assets/maps/ARPG5_2.tmx'])

    def load_level(self, tmx_name):
        tmx_data = load_pygame(tmx_name)
        for layer in tmx_data.visible_layers:
            if hasattr(layer, 'tiles'):
                for x, y, surface in layer.tiles():
                    pos = (x * TILE_SIZE, y * TILE_SIZE)
                    if layer.name == 'Ground':
                        Tile(surface, pos, self.visible_sprites)
                    if layer.name == 'Obstacles':
                        Tile(surface, pos, self.obstacles)
                    if layer.name == 'Buildings':
                        Tile(surface, pos, self.actors)
        npc_path = []
        for obj in tmx_data.get_layer_by_name('Entities'):
            if obj.name == 'npc_path':
                npc_path = list(obj.points)
        for obj in tmx_data.get_layer_by_name('Entities'):
            if obj.name == 'player_start':
                self.player = Player(
                    pos=(obj.x, obj.y), 
                    colliders=self.obstacles, 
                groups=[self.actors], 
                attack_one=self.create_attack,
                attack_one_destroy=self.destroy_attack,
                max_health=100)
            if obj.name == 'enemy_start':
                enemy = Enemy(
                   pos=(obj.x, obj.y), 
                   player=self.player, 
                   ai_type='random', 
                   colliders=self.obstacles, 
                   groups=[self.actors, self.talkers, self.attackable_sprites], 
                   max_health=100,
                   enemy_class=EnemyClass(xp=150))
            if obj.name == 'npc_start':
                x = npc_path[0].x
                y = npc_path[0].y
                npc = NPC((x,y), self.player, 'follow', self.obstacles, [self.actors, self.talkers])
                npc.ai.set_path(npc_path)

    def create_map(self):
        self.load_level(self.map_name)
        return self.player

    def run(self, dt):
        self.actors.update(dt)
        self.attack_logic()

    def render(self):
        self.screen.fill((0,0,0))
        self.visible_sprites.custom_draw(self.screen, self.player)
        self.obstacles.custom_draw(self.screen, self.player)
        self.actors.custom_draw(self.screen, self.player)
        self.ui.display(self.player)

    def attack_logic(self):
        if self.attack_sprites:
            for attack in self.attack_sprites:
                collisions = [sprite for sprite in self.attackable_sprites if sprite.hitbox.colliderect(attack)]
                if collisions:
                    for victim in collisions:
                        victim.take_damage(45)

    def create_attack(self):
        if not self.player_attack:
            self.player_attack = Weapon(self.player, [self.actors, self.attack_sprites])
        
    def destroy_attack(self):
        if self.player_attack:
            self.player_attack.kill()
        self.player_attack = None
