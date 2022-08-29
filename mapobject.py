import random
import pygame
from light import Light
from item import *

class MapObject:
    """ 'type' is matched to 'path' TileIDs (caller must compute path base)"""
    def __init__(self, game, world, tile, type, gx, gy):
        self.type = type
        if type < 8 or type > 26:
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
        self.tile = tile
        self.collision_width = 1
        self.collision_height = 1
        self.sprite_width = 1
        self.sprite_height = 1
        self.x = self.gx*16
        self.y = self.gy*16
        self.draw_off_x = 0
        self.draw_off_y = 0
        self.sprite = game.sprite.get_tiles("paths")
        self.large_sprite = None
        self.large_sprite_mid = None
        self.large_sprite_front = None
        self.large_sprite_all = None
        self.ogx = 0
        self.ogy = 0
        self.hp = 1
        self.reverse = False
        self.init = False
        self.action_list = ()
        self.spr_name = ""
        self.loot = []
        
        # Object is valid -- register with world tracker
        world.current_map_path_objects.append(self)   # Linear list tracker
        
    def init_sprite(self):
        if self.reverse:
            self.large_sprite = self.game.sprite.get_large_sprite(self.spr_name)
        else:
            self.large_sprite = self.game.sprite.get_large_sprite_reverse(self.spr_name)
            
        self.large_sprite_mid = self.large_sprite[0]
        self.large_sprite_front = self.large_sprite[1]
        self.large_sprite_all = self.large_sprite[2]
        
    def init_second_stage(self):
        if self.init: return
        self.set_constants(self.type)

        self.reverse = random.choice((True,False))
        
        if self.type == 22:
            self.draw_off_x = self.game.sprite.get_draw_off_x(self.spr_name) + random.randint(-4,4)
            self.draw_off_y = self.game.sprite.get_draw_off_y(self.spr_name)  + random.randint(-4,4)
            
        if self.spr_name:
            self.init_sprite()
            self.set_large_collision_box(self.spr_name)
            # add the large object to the O(1) object tracker
            self.world.objects[(self.world.current_map,(self.gx,self.gy))] = self
            self.ogx, self.ogy = self.game.sprite.get_large_sprite_origin(self.spr_name)

        self.init = True
            
    def get_large_sprite(self):
        return self.large_sprite_all
        
    def set_large_collision_box(self, spr_name, value=1):
        if self.tile.map != self.world.current_map: return
        # Collisions start from the front/bottom of a sprite and work backward
        self.collision_width = self.game.sprite.get_collision_width(spr_name)
        self.collision_height = self.game.sprite.get_collision_height(spr_name)
        for j in range(self.collision_height):
            for i in range(self.collision_width):
                key = (self.world.current_map,(self.gx+i,self.gy+j))
                key_tile = (self.gx+i, self.gy+j)
                tile = self.world.map_tiles[self.world.current_map][key_tile]
                if value:  # add the large object to the O(1) object tracker
                    self.world.objects[key] = self # O(1) lookup by position
                    tile.collision = True
                else:      # Remove the large object from O(1) object tracker
                    tile.collision = False
                    if key in self.world.objects and self.world.objects[key] == self:
                        del self.world.objects[key]
                    
    def destroy(self):
        if self.type == 22:
            if random.randint(1,2) == 1: return
        if self in self.world.current_map_path_objects:
            self.world.current_map_path_objects.pop(self.world.current_map_path_objects.index(self))
        del self.world.objects[(self.tile.map,(self.gx,self.gy))]
        
        # Maybe an object shouldn't ALWAYS clear collisions...?
        tile_num = self.world.get_tile_num(self.gx,self.gy)
        self.set_large_collision_box(self.spr_name, 0)
        
        # Remove from tile (eventually multiple objects per tile?)
        self.tile.object = None
        self.world.redraw_objects = True
        
        self.world.redraw_front = True
              
        # Generate items from destruction
        for loot in self.loot:
            name = loot[0]
            max_count = loot[1]
            item = Resource(self.game, name)
            item.create_at(self.gx*16+random.randint(-8,8),self.gy*16+random.randint(-8,8))
            item.count = random.randint(1,max_count)
            
    def render_mid(self, screen):
        if self.large_sprite:
            screen.blit(self.large_sprite_mid, (self.x-self.ogx*16,self.y-self.ogy*16), (0,0,3*16,6*16))
        else: #unused for now
            screen.blit(self.sprite[self.type], (self.x,self.y), (0,0,16,16))
            
    def render_front(self, screen):
        if self.large_sprite:
            screen.blit(self.large_sprite_front, (self.x-self.ogx*16,self.y-self.ogy*16), (0,0,3*16,6*16))
        else: #unused for now
            screen.blit(self.sprite[self.type], (self.x,self.y), (0,0,16,16))
            
    def render_all(self, screen):
        if self.large_sprite:
            screen.blit(self.large_sprite_all, (self.x+self.draw_off_x-self.ogx*16,self.y+self.draw_off_y-self.ogy*16), (0,0,3*16,6*16))
        else: #unused for now
            screen.blit(self.sprite[self.type], (self.x,self.y), (0,0,16,16))
            
    def set_constants(self,type):
        if self.type == 9: 
            self.spr_name = "spr_oak"
            self.action_list = ("axe", "bomb", "tap")
            self.hp = 300
            self.loot = [("wood",2),("wood",2),("wood",2)]
            self.seasons = [True,True,True,True]
        if self.type == 10: 
            self.spr_name = "spr_maple";
            self.action_list = ("axe", "bomb", "tap")
            self.hp = 300
            self.loot = [("wood",2),("wood",2),("wood",2)]
            self.seasons = [True,True,True,True]
        if self.type == 11: 
            self.spr_name = "spr_pine"
            self.action_list = ("axe", "bomb", "tap")
            self.hp = 300
            self.loot = [("wood",2),("wood",2),("wood",2)]
            self.seasons = [True,True,True,True]
        if self.type == 13: 
            self.spr_name = "spr_weed1"
            #self.tiles = 
            self.action_list = ("axe", "scythe", "slash", "bomb")
            self.seasons = [True,True,True,False]
        if self.type == 14: 
            self.spr_name = "spr_weed2"
            self.action_list = ("axe", "scythe", "slash", "bomb")
            self.seasons = [True,True,True,False]
        if self.type == 15: 
            self.spr_name = "spr_weed3"
            self.action_list = ("axe", "scythe", "slash", "bomb")
            self.seasons = [True,True,True,False]
        if self.type == 16:
            self.spr_name = "spr_rock_small"
            self.action_list = ("pickaxe", "bomb")
            self.loot = [("stone",2)]          
            self.seasons = [True,True,True,True]
        if self.type == 17:
            self.spr_name = "spr_rock_small"; 
            self.action_list = ("pickaxe", "bomb")
            self.loot = [("stone",2)]
            self.seasons = [True,True,True,True]
        if self.type == 18: 
            self.spr_name = "spr_stick"
            self.action_list = ("axe", "scythe", "bomb")
            self.loot = [("wood",2)]
            self.seasons = [True,True,True,True]
        if self.type == 19: 
            self.spr_name = "spr_log"
            self.action_list = ("axe")
            self.loot = [("wood",2), ("hardwood",2), ("hardwood",2), ("hardwood",2)]
            self.hp = 100
            self.seasons = [True,True,True,True]
        if self.type == 20:
            self.spr_name = "spr_rock_large"
            self.action_list = ("pickaxe")
            self.hp = 100
            self.loot = [("stone",2), ("stone",2), ("stone",2)]
            self.seasons = [True,True,True,True]
        if self.type == 21:
            self.spr_name = "spr_stump_large"
            self.action_list = ("axe")
            self.hp = 100
            self.loot = [("wood",2), ("hardwood",2), ("hardwood",2), ("hardwood",2)]
            self.seasons = [True,True,True,True]
        if self.type == 22:
            self.spr_name = "spr_grass"
            self.action_list = ("slash")
            self.collision_width = 0
            self.collision_height = 0
            self.seasons = [True,True,True,False]
        if self.type == 23:
            self.spr_name = "spr_little_tree"
            self.action_list = ("axe", "slash")
            self.hp = 1
            self.loot = [("wood",2)]
            self.seasons = [True,True,True,True]
        if self.type == 24:
            self.spr_name = "spr_bush_large";
            self.seasons = [True,True,True,True]
        if self.type == 25: 
            self.spr_name = "spr_bush_medium";
            self.seasons = [True,True,True,True]
        if self.type == 26: 
            self.spr_name = "spr_bush_small";
            self.seasons = [True,True,True,True]
            
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
        w = self.sprite[self.level].get_width()
        h = self.sprite[self.level].get_height()
        spr_top = self.always_front_layer_height*16
        screen.blit(self.sprite[self.level], (self.x,self.y+spr_top), (0,spr_top,w,h-(self.always_front_layer_height*16)))
        
    def render_front(self,screen):
        w = self.sprite[self.level].get_width()
        h = self.sprite[self.level].get_height()
        screen.blit(self.sprite[self.level], (self.x,self.y), (0,0,w,self.always_front_layer_height*16))