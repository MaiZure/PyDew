import random
import pygame

class Light:
    def __init__(self, game, world, type, gx, gy):
        self.game = game
        self.world = world
        
        self.surf = pygame.Surface((160, 160), pygame.SRCALPHA)
        self.gx = gx
        self.gy = gy
        self.x = gx * 16
        self.y = gy * 16
        world.lights.append(self)
        self.surf.fill(pygame.Color(0,0,0,0))
        #self.game.ambient_surface.set_colorkey((16,16,16))
        for i in range(64,0, -1):
            pygame.draw.circle(self.surf, (5,5,5,max(255-i*4,0)), (80,80), i)
        
    def render(self, screen):
        if not self.world.is_visible(self.gx,self.gy): return
        top_left_x = self.game.world.top_left_x
        top_left_y = self.game.world.top_left_y
            
        screen.blit(self.surf, (self.x-top_left_x-72, self.y-top_left_y-72), (0,0,160,160))
        