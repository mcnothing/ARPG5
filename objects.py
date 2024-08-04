import pygame

hitbox_red = pygame.Color(192, 64, 64, 64)

class Weapon(pygame.sprite.Sprite):
    def __init__(self, player, groups):
        super().__init__(groups)
        hitbox = pygame.Surface((16,16))
        hitbox.fill(hitbox_red)
        self.image = hitbox
        self.get_pos(player)

    def get_pos(self, player):
        '''Get player facing to place the attack in the correct location'''
        direction = player.facing.split('_')[-1]
        if direction == 'right':
            self.rect = self.image.get_rect(midleft = player.hitbox.midright)# + pygame.math.Vector2(0, 16))
        elif direction == 'left':
            self.rect = self.image.get_rect(midright = player.hitbox.midleft)# + pygame.math.Vector2(0, 16))
        elif direction == 'down':
            self.rect = self.image.get_rect(midtop = player.hitbox.midbottom)# + pygame.math.Vector2(-10, 0))
        else:
            self.rect = self.image.get_rect(midbottom = player.hitbox.midtop)# + pygame.math.Vector2(-10, 0))