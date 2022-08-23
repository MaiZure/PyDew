import random
import pygame

class Crop:
    def __init__(self,game,data,tile):
        self.game = game
        self.world = game.world
        self.data = data
        self.tile = tile
        self.x = self.tile.gx * 16
        self.y = self.tile.gy * 16
        self.stage = 0
        self.index = data[0]
        self.stage_timers = data[1].split(" ")
        self.stage_time = int(self.stage_timers[self.stage])
        self.max_stage = len(self.stage_timers) + 1
        self.season = data[2]
        self.sprite_index_base = int(data[3]) * 8 # Each sprite sequence has up to 8 frames 
        self.harvest_index = data[4]
        self.regrow_time = int(data[5])
        self.harvest_method = data[6]
        self.extra_harvest = data[7]
        self.trellis = data[8]
        self.tint = data[9]
        
        self.sprite = self.game.sprite.get_tiles("crops")
        
        # Build stage index array
        self.stages = []
        self.stages.append(self.sprite_index_base + random.choice((0,1)))
        self.sprite_index = self.stages[self.stage]
        for i in range(len(self.stage_timers)):
            self.stages.append(self.sprite_index_base + i+2)
        self.final_stage_index = len(self.stages)-1
        self.regrow_stage_index = -1
        if self.regrow_time > 0:
            self.stages.append(self.sprite_index_base + i+3)
            self.regrow_stage_index = len(self.stages)-1
            
    def grow(self):
        self.stage_time -= 1
        if self.stage_time < 1:
            if self.stage < self.final_stage_index:
                self.stage += 1
            if self.stage < len(self.stage_timers):
                self.stage_time = int(self.stage_timers[self.stage-1])
            self.sprite_index = self.stages[self.stage]
        self.tile.render_tile()
        
    def harvest(self):
        if self.stage < self.final_stage_index: return
        
    def remove(self):
        key = (self.tile.map, (self.tile.gx, self.tile.gy))
        if key in self.world.crops:
            del self.world.crops[key]
        
    def render(self, back, mid, front):
        # Crop sprites are mostly 16x32. The bottom bottom 16x16 square represents the actual square
        
        # Seed stage only?
        back.blit(self.sprite[self.sprite_index], (self.x, self.y), (0,16,16,16))
        
        # Top half for now (should probably be mid/front for taller plants)
        mid.blit(self.sprite[self.sprite_index], (self.x, self.y-16), (0,0,16,16))
        
    