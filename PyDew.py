import random
import pygame

from world import World
from player import Player
from config import Config
from spriteloader import SpriteLoader
from maploader import MapLoader
from mapobject import MapObject
from audio import Audio
from ui import UI
from mouse import MouseHandler
from item import Item


class PyDew:

    def __init__(self):
        pygame.init()
        self.version = "0.1.3.31"
        print("Hello PyDew "+str(self.version))
        self.config = Config()        
        self.final_screen = pygame.display.set_mode((self.config.screen_width, 
                                               self.config.screen_height),
                                               pygame.HWSURFACE|pygame.DOUBLEBUF)
        self.unscaled_screen = pygame.Surface((self.config.screen_width/self.config.screen_scaling, 
                                               self.config.screen_height/self.config.screen_scaling))
        self.ambient_surface = pygame.Surface((self.config.screen_width/self.config.screen_scaling, 
                                               self.config.screen_height/self.config.screen_scaling),
                                               pygame.SRCALPHA)
        self.bg_surface = pygame.Surface((self.config.screen_width/self.config.screen_scaling, 
                                               self.config.screen_height/self.config.screen_scaling))
        self.mid_surface = pygame.Surface((self.config.screen_width/self.config.screen_scaling, 
                                               self.config.screen_height/self.config.screen_scaling),
                                               pygame.SRCALPHA)
        self.fg_surface = pygame.Surface((self.config.screen_width/self.config.screen_scaling, 
                                               self.config.screen_height/self.config.screen_scaling),
                                               pygame.SRCALPHA)
        self.npc_surface = pygame.Surface((self.config.screen_width/self.config.screen_scaling, 
                                               self.config.screen_height/self.config.screen_scaling),
                                               pygame.SRCALPHA)
        self.ui_surface = pygame.Surface((self.config.screen_width/self.config.screen_scaling, 
                                               self.config.screen_height/self.config.screen_scaling),
                                               pygame.SRCALPHA)
        self.menu_surface = pygame.Surface((self.config.screen_width, self.config.screen_height),
                                               pygame.SRCALPHA)                       
        
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("PyDew "+str(self.version))
        
        self.sprite = SpriteLoader(self)
        self.map = MapLoader(self)
        self.world = World(self)
        self.player = Player(self)
        self.ui = UI(self)
        self.audio = Audio(self)
        self.mouse = MouseHandler(self,self.ui)
        
        self.paused = False
        
        self.run = False
        
        
    #do some more start stuff - like a main menu
    def start(self):
      self.run = True
      self.game_loop()
        
    #The game loop
    def game_loop(self):
        while self.run:
            self.check_input()
            
            if not self.paused:
                self.update()
            
            self.render()
            
            self.clock.tick(60) # ~60 FPS
        
        pygame.quit()
    
    #Check/Dispatch user input
    def check_input(self):
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                self.run = False
            if e.type == pygame.KEYUP:
                if e.key == pygame.K_t:
                    return
                    self.world.set_random_season();
                    self.world.regenerate_season = True # Make fxn
                if e.key == pygame.K_p:
                    self.world.init_map("forest")
            if e.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                print("Mouse click at "+str(pos) + " - " + str(self.ui.ibar.ibar_clickrect))
                if e.button == 1 & self.ui.ibar.ibar_clickrect.collidepoint(pos):
                    self.ui.ibar.handle_mouse(e)    # Move this elsewhere (not all left click goes to ibar
                if e.button == 4 or e.button == 5:  # Mouse wheel up/down
                    self.ui.ibar.handle_mouse(e)
        keys = pygame.key.get_pressed()
        
        if not self.paused:
            self.player.handle_input(keys)
        
    #Update game state
    def update(self):
        self.world.tick()
        self.ui.tick()
        
    #Draw some stuff
    def render(self):
        self.world.prerender(self.bg_surface)
        self.world.render_back(self.bg_surface)
        self.world.render_mid(self.mid_surface)
        self.world.render_front(self.fg_surface)
        self.ui.ui_render(self.ui_surface)
        self.ui.menu_render(self.menu_surface)
        
        for light in self.world.lights:
            light.render(self.ambient_surface)
            
        self.unscaled_screen.blit(self.bg_surface,(0,0))
        self.unscaled_screen.blit(self.mid_surface,(0,0))
        self.unscaled_screen.blit(self.fg_surface,(0,0))
        self.unscaled_screen.blit(self.ambient_surface,(0,0), special_flags=pygame.BLEND_SUB)
        self.unscaled_screen.blit(self.ui_surface,(0,0))
        
        scaled_screen = pygame.transform.scale(self.unscaled_screen,self.final_screen.get_rect().size)
                
        scaled_screen.blit(self.menu_surface, (0,0))
        
        self.final_screen.blit(scaled_screen,(0,0))
        pygame.display.update()


#Go!
if __name__ == "__main__":
    game = PyDew()
    game.start()
    