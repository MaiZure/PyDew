import random
import pygame
from light import Light

class MapObject:
    """ 'type' is matched to 'path' TileIDs (caller must compute path base)"""
    def __init__(self, game, world, type, gx, gy):
        if type < 8 or type > 33:
            # This effectively removes the object as no reference is built
            return None
        
        if type == 8:
            Light(game, world, type, gx, gy)
            return
            
        self.game = game
        self.world = world
        self.gx = gx
        self.gy = gy
        self.tile_num = world.get_tile_num(self.gx,self.gy)
        self.collision_width = 1
        self.collision_height = 1
        self.sprite_width = 1
        self.sprite_height = 1
        self.x = self.gx*16
        self.y = self.gy*16
        self.sprite = game.sprite.get_tiles("paths")
        self.large_sprite = None
        self.large_sprite_mid = None
        self.large_sprite_front = None
        self.ogx = 0
        self.ogy = 0
        self.hp = 0
        self.type = type
        self.reverse = False
        
        # Object is valid -- register with world tracker
        world.current_map_path_objects.append(self)
        
    def init_second_stage(self):
        if self.collision_height and self.collision_width:
            self.world.collision_map[self.tile_num] = 1
        self.reverse = random.choice((True,False))
        spr_name = ""
        if self.type == 9: spr_name = "spr_oak"
        if self.type == 10: spr_name = "spr_maple"
        if self.type == 11: spr_name = "spr_pine"
        if self.type == 13: spr_name = "spr_weed"
        if self.type == 14: spr_name = "spr_weed"
        if self.type == 15: spr_name = "spr_weed"
        if self.type == 16: spr_name = "spr_rock_small"
        if self.type == 17: spr_name = "spr_rock_small"
        if self.type == 18: spr_name = "spr_stick" #Not a large sprite -- fix later
        if self.type == 19: spr_name = "spr_log"
        if self.type == 20: spr_name = "spr_rock_large"
        if self.type == 21: spr_name = "spr_stump_large"
        if self.type == 24: spr_name = "spr_bush_large"
        if self.type == 25: spr_name = "spr_bush_medium"
        if self.type == 26: spr_name = "spr_bush_small"
        if spr_name:
            if self.reverse:
                self.large_sprite = self.game.sprite.get_large_sprite(spr_name)
            else:
                self.large_sprite = self.game.sprite.get_large_sprite_reverse(spr_name)
                
            self.large_sprite_mid = self.large_sprite[0]
            self.large_sprite_front = self.large_sprite[1]
            self.set_large_collision_box(spr_name)
            self.ogx, self.ogy = self.game.sprite.get_large_sprite_origin(spr_name)
         
    def set_large_collision_box(self, spr_name):
        # Collisions start from the front/bottom of a sprite and work backward
        self.collision_width = self.game.sprite.get_collision_width(spr_name)
        self.collision_height = self.game.sprite.get_collision_height(spr_name)
        for j in range(self.collision_height):
            for i in range(self.collision_width):
                tile_num = self.world.get_tile_num(self.gx+i,self.gy-j)
                self.world.collision_map[tile_num] = 1
            
    def render_mid(self, screen):
        if not self.game.world.is_visible(self.gx, self.gy): return
        top_left_x = self.game.world.top_left_x
        top_left_y = self.game.world.top_left_y
        if self.large_sprite:
            screen.blit(self.large_sprite_mid, (self.x-top_left_x-self.ogx*16,self.y-top_left_y-self.ogy*16), (0,0,3*16,6*16))
        else:
            screen.blit(self.sprite[self.type], (self.x-top_left_x,self.y-top_left_y), (0,0,16,16))
            
    def render_front(self, screen):
        top_left_x = self.game.world.top_left_x
        top_left_y = self.game.world.top_left_y
            
        if self.large_sprite:
            screen.blit(self.large_sprite_front, (self.x-self.ogx*16,self.y-self.ogy*16), (0,0,3*16,6*16))
        else:
            screen.blit(self.sprite[self.type], (self.x,self.y), (0,0,16,16))