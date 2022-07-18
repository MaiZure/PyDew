import random
import pygame
from light import Light
from item import *

class MapObject:
    """ 'type' is matched to 'path' TileIDs (caller must compute path base)"""
    def __init__(self, game, world, type, gx, gy):
        if type < 8 or type > 28:
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
        self.hp = 1
        self.type = type
        self.reverse = False
        self.action_list = ()
        self.spr_name = ""
        self.loot = []
        
        
        # Object is valid -- register with world tracker
        world.current_map_path_objects.append(self)   # Linear list tracker
        world.objects[(world.current_map,gx,gy)] = self                 # gx,gy O(1) lookup by position
        
    def init_second_stage(self):
        self.set_constants(self.type)
        
        if self.collision_height and self.collision_width:
            self.world.collision_map[self.tile_num] = 1
        self.reverse = random.choice((True,False))
             
        if self.spr_name:
            if self.reverse:
                self.large_sprite = self.game.sprite.get_large_sprite(self.spr_name)
            else:
                self.large_sprite = self.game.sprite.get_large_sprite_reverse(self.spr_name)
                
            self.large_sprite_mid = self.large_sprite[0]
            self.large_sprite_front = self.large_sprite[1]
            self.set_large_collision_box(self.spr_name)
            self.ogx, self.ogy = self.game.sprite.get_large_sprite_origin(self.spr_name)
         
    def set_large_collision_box(self, spr_name, value=1):
        # Collisions start from the front/bottom of a sprite and work backward
        self.collision_width = self.game.sprite.get_collision_width(spr_name)
        self.collision_height = self.game.sprite.get_collision_height(spr_name)
        for j in range(self.collision_height):
            for i in range(self.collision_width):
                tile_num = self.world.get_tile_num(self.gx+i,self.gy+j)
                self.world.collision_map[tile_num] = value
                
    def destroy(self):       
        self.world.current_map_path_objects.pop(self.world.current_map_path_objects.index(self))
        del self.world.objects[(self.world.current_map,self.gx,self.gy)]
        
        # Maybe an object shouldn't ALWAYS clear collisions...?
        tile_num = self.world.get_tile_num(self.gx,self.gy)
        self.world.collision_map[tile_num] = 0
        self.set_large_collision_box(self.spr_name, 0)
       
        
        # Generate items from destruction
        for loot in self.loot:
            name = loot[0]
            max_count = loot[1]
            item = Resource(self.game, name)
            item.create_at(self.gx*16+random.randint(-8,8),self.gy*16+random.randint(-8,8))
            item.count = random.randint(1,max_count)
            
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
            
    def set_constants(self,type):
        if self.type == 9: 
            self.spr_name = "spr_oak"
            self.action_list = ("axe", "bomb", "tap")
            self.hp = 300
            self.loot = [("wood",2),("wood",2),("wood",2)]
        if self.type == 10: 
            self.spr_name = "spr_maple";
            self.action_list = ("axe", "bomb", "tap")
            self.hp = 300
            self.loot = [("wood",2),("wood",2),("wood",2)]
        if self.type == 11: 
            self.spr_name = "spr_pine"
            self.action_list = ("axe", "bomb", "tap")
            self.hp = 300
            self.loot = [("wood",2),("wood",2),("wood",2)]
        if self.type == 13: 
            self.spr_name = "spr_weed"
            self.action_list = ("axe", "scythe", "bomb")
        if self.type == 14: 
            self.spr_name = "spr_weed"
            self.action_list = ("axe", "scythe", "bomb")
        if self.type == 15: 
            self.spr_name = "spr_weed"
            self.action_list = ("axe", "scythe", "bomb")
        if self.type == 16:
            self.spr_name = "spr_rock_small"
            self.action_list = ("pickaxe", "bomb")
            self.loot = [("stone",2)]
        if self.type == 17:
            self.spr_name = "spr_rock_small"; 
            self.action_list = ("pickaxe", "bomb")
            self.loot = [("stone",2)]
        if self.type == 18: 
            self.spr_name = "spr_stick"
            self.action_list = ("axe", "scythe", "bomb")
            self.loot = [("wood",2)]
        if self.type == 19: 
            self.spr_name = "spr_log"
            self.action_list = ("axe")
            self.loot = [("wood",2), ("hardwood",2), ("hardwood",2), ("hardwood",2)]
            self.hp = 100
        if self.type == 20:
            self.spr_name = "spr_rock_large"
            self.action_list = ("pick")
            self.hp = 100
            self.loot = [("stone",2), ("stone",2), ("stone",2)]
        if self.type == 21:
            self.spr_name = "spr_stump_large"
            self.action_list = ("axe")
            self.hp = 100
            self.loot = [("wood",2), ("hardwood",2), ("hardwood",2), ("hardwood",2)]
        if self.type == 22:
            self.collision_width = 0
            self.collision_height = 0
        if self.type == 23:
            self.spr_name = "spr_little_tree"
            self.action_list = ("axe")
            self.hp = 1
            self.loot = [("wood",2)]
        if self.type == 24:
            self.spr_name = "spr_bush_large";
        if self.type == 25: 
            self.spr_name = "spr_bush_medium";
        if self.type == 26: 
            self.spr_name = "spr_bush_small";
            
class Farmhouse:
    def __init__(self, game, world):        
        self.game = game
        self.world = world
        self.gx = 58
        self.gy = 8
        self.x = self.gx*16
        self.y = self.gy*16
        self.always_front_layer_height = 3
        self.sprite = game.sprite.get_tiles("houses")
        self.spr_name = ""
        self.level = 0
        
    def render_back(self, screen):
        print("Drawing House BG")
        w = self.sprite[self.level].get_width()
        h = self.sprite[self.level].get_height()
        spr_top = self.always_front_layer_height*16
        screen.blit(self.sprite[self.level], (self.x,self.y+spr_top), (0,spr_top,w,h-(self.always_front_layer_height*16)))
        
    def render_front(self,screen):
        w = self.sprite[self.level].get_width()
        h = self.sprite[self.level].get_height()
        screen.blit(self.sprite[self.level], (self.x,self.y), (0,0,w,self.always_front_layer_height*16))