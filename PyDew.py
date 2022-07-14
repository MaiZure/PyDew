import random
import pygame
import ctypes 

from world import World
from player import Player
from config import Config
from spriteloader import SpriteLoader
from maploader import MapLoader
from fontloader import FontLoader
from mapobject import MapObject
from audio import Audio
from ui import UI
from mouse import MouseHandler
from item import ItemLoader
from savedata import SaveData
from dataloader import DataLoader


class PyDew:
    def __init__(self):
        ctypes.windll.user32.SetProcessDPIAware()  # Inform PyGame of real DPI (avoid OS-level scaling)
        pygame.init()
        self.version = "0.2.1.82"
        print("Hello PyDew "+str(self.version))
        self.config = Config()
        self.save = SaveData()
        self.final_screen = pygame.display.set_mode((self.config.screen_width, 
                                               self.config.screen_height),
                                               pygame.HWSURFACE|pygame.DOUBLEBUF)
        self.unscaled_screen = pygame.Surface((self.config.screen_width/self.config.screen_scaling, 
                                               self.config.screen_height/self.config.screen_scaling)).convert_alpha()
        self.unscaled_ui_screen = pygame.Surface((self.config.screen_width/self.config.ui_scaling, 
                                               self.config.screen_height/self.config.ui_scaling),
                                               pygame.SRCALPHA).convert_alpha()
        self.scaled_screen = pygame.Surface((self.config.screen_width, self.config.screen_height),
                                               pygame.SRCALPHA).convert_alpha()
        self.scaled_ui_screen = pygame.Surface((self.config.screen_width, self.config.screen_height),
                                               pygame.SRCALPHA).convert_alpha()
        self.ambient_surface = pygame.Surface((self.config.screen_width/self.config.screen_scaling, 
                                               self.config.screen_height/self.config.screen_scaling),
                                               pygame.SRCALPHA).convert_alpha()
        self.bg_surface = pygame.Surface((self.config.screen_width/self.config.screen_scaling, 
                                               self.config.screen_height/self.config.screen_scaling)).convert()
        self.mid_surface = pygame.Surface((self.config.screen_width/self.config.screen_scaling, 
                                               self.config.screen_height/self.config.screen_scaling),
                                               pygame.SRCALPHA).convert_alpha()
        self.fg_surface = pygame.Surface((self.config.screen_width/self.config.screen_scaling, 
                                               self.config.screen_height/self.config.screen_scaling),
                                               pygame.SRCALPHA).convert_alpha()
        self.npc_surface = pygame.Surface((self.config.screen_width/self.config.screen_scaling, 
                                               self.config.screen_height/self.config.screen_scaling),
                                               pygame.SRCALPHA).convert_alpha()
        self.ui_surface = pygame.Surface((self.config.screen_width/self.config.ui_scaling, 
                                               self.config.screen_height/self.config.ui_scaling),
                                               pygame.SRCALPHA).convert_alpha()
        self.menu_surface = pygame.Surface((self.config.screen_width, self.config.screen_height),
                                               pygame.SRCALPHA).convert_alpha()

        
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("PyDew "+str(self.version))
        
        self.sprite = SpriteLoader(self)
        self.data = DataLoader(self)
        self.map = MapLoader(self)
        self.font = FontLoader(self)
        self.item = ItemLoader(self)
        self.world = World(self)    
        self.player = Player(self)
        self.ui = UI(self)
        self.audio = Audio(self)
        self.mouse = MouseHandler(self,self.ui)
        
        self.paused = False    
        self.run = False
        
        self.sprite.init_second_stage()
        self.data.init_second_stage()
        self.map.init_second_stage()
        self.font.init_second_stage()
        self.item.init_second_stage()
        self.world.init_second_stage()
        self.player.init_second_stage()
        self.ui.init_second_stage()
        self.audio.init_second_stage()
        self.mouse.init_second_stage()
        
        
    #do some more start stuff - like a main menu
    def start(self):
        self.run = True
        self.game_loop()
        
    #The game loop
    def game_loop(self):
        while self.run:
            self.check_input()
            
            self.update()
            
            self.render()
            
            self.clock.tick(self.config.fps) # ~60 FPS
        
        pygame.quit()
    
    #Check/Dispatch user input
    def check_input(self):
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                self.run = False
            if e.type == pygame.KEYUP:
                if e.key == pygame.K_t:
                    return
                    #self.world.set_random_season()
                    #self.world.regenerate_season = True # Make fxn
                if e.key == pygame.K_p:
                    self.world.init_map("forest")
                if e.key == pygame.K_v:
                    self.world.litterbug()
                if e.key == pygame.K_l:
                    self.world.speed_time = not self.world.speed_time
                if e.key == pygame.K_ESCAPE:
                    self.ui.toggle_player_menu()
                if e.key == pygame.K_TAB: 
                    self.player.cycle_inventory()
            if e.type == pygame.MOUSEBUTTONDOWN:
                self.mouse.handle_input(e)
        keys = pygame.key.get_pressed()

        if not self.paused:
            self.player.handle_input(keys)
        
    # Update game state
    def update(self):
        if not self.paused:
            self.world.tick()
        self.ui.tick()

    # Draw some stuff
    def render(self):
        if not self.paused:
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
        self.unscaled_ui_screen.blit(self.ui_surface,(0,0))

        pygame.transform.scale(self.unscaled_screen,self.final_screen.get_rect().size, self.scaled_screen)
        pygame.transform.scale(self.unscaled_ui_screen,self.final_screen.get_rect().size, self.scaled_ui_screen)
        
        self.scaled_screen.blit(self.scaled_ui_screen,(0,0))    
        self.scaled_screen.blit(self.menu_surface, (0,0))
        
        # Post scaling rendering (text, some UI elements like health bars, clock hand rotation [future])
        self.ui.ui_render_scaled(self.scaled_screen)

        self.final_screen.blit(self.scaled_screen,(0,0))
        pygame.display.update()


#Go!
if __name__ == "__main__":
    game = PyDew()
    game.start()
    