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


class PyDew:

    def __init__(self):
        pygame.init()
        self.version = "0.0.8.20"
        print("Hello PyDew "+str(self.version))
        self.config = Config()        
        self.final_screen = pygame.display.set_mode((self.config.screen_width, 
                                               self.config.screen_height),
                                               pygame.HWSURFACE|pygame.DOUBLEBUF)
        self.unscaled_screen = pygame.Surface((self.config.screen_width/self.config.screen_scaling, 
                                               self.config.screen_height/self.config.screen_scaling))
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
        self.menu_surface = pygame.Surface((self.config.screen_width/self.config.screen_scaling, 
                                               self.config.screen_height/self.config.screen_scaling),
                                               pygame.SRCALPHA)                       
        
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("PyDew "+str(self.version))
        
        self.sprite = SpriteLoader(self)
        self.map = MapLoader(self)
        self.world = World(self)
        self.player = Player(self)
        self.ui = UI(self)
        self.audio = Audio(self)
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
        #self.player.render(self.bg_surface)   # Use NPC surface?
        self.world.render_mid(self.mid_surface)
        self.world.render_front(self.fg_surface)
        self.ui.render(self.ui_surface)
        
        self.unscaled_screen.blit(self.bg_surface,(0,0))
        self.unscaled_screen.blit(self.mid_surface,(0,0))
        self.unscaled_screen.blit(self.fg_surface,(0,0))
        self.unscaled_screen.blit(self.ui_surface,(0,0))
       
        scaled_screen = pygame.transform.scale(self.unscaled_screen,self.final_screen.get_rect().size)
        
        self.final_screen.blit(scaled_screen,(0,0))
        pygame.display.update()


#Go!
if __name__ == "__main__":
    game = PyDew()
    game.start()
    