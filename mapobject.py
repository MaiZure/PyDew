import random
import pygame

class MapObject:
    """ 'type' is matched to 'path' TileIDs (caller must compute path base)"""
    def __init__(self, game, world, type, gx, gy):
        if type < 9 or type > 33:
            # This effectively removes the object as no reference is built
            return None
        
        self.game = game
        self.world = world
        self.gx = gx
        self.gy = gy
        self.x = self.gx*16
        self.y = self.gy*16
        self.sprite = game.sprite.get_spritesheet_tiles("paths")
        self.type = type
        # Object is valid -- register with world tracker
        world.current_map_path_objects.append(self)
        
    def render(self, screen):
        top_left_x = min(max(self.game.player.x-screen.get_width()/2,0),self.world.map_width*16-screen.get_width())
        top_left_y = min(max(self.game.player.y-screen.get_height()/2,0),self.world.map_height*16-screen.get_height())
        screen.blit(self.sprite[self.type], (self.x-top_left_x,self.y-top_left_y), (0,0,16,32))