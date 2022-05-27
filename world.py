import random
import pygame

class World:

    def __init__(self, game):
        print("Initializaing World")
        self.game = game
        self.new_map = True
        
        self.tiles = []
        self.set_random_season()        
        
        #TODO - Make these layer arrays
        self.bg_layer = game.map.get_layer_map("forest",0)
        self.bldg_layer = game.map.get_layer_map("forest",1)
        self.path_layer = game.map.get_layer_map("forest",2)
        self.front_layer = game.map.get_layer_map("forest",3)
        self.always_front_layer = game.map.get_layer_map("forest",4)
        
        self.map_width = game.map.get_layer_width("forest",0)
        self.map_height = game.map.get_layer_height("forest",0)
        
        # Create background surface to render map
        rect = pygame.Rect(0, 0, self.map_width*16, self.map_height*16) 
        self.bg = pygame.Surface(rect.size).convert()
        self.fg = pygame.Surface(rect.size, pygame.SRCALPHA).convert_alpha()
        self.generate_background_layers()
        self.generate_foreground_layers()
        
    def set_season(self, season):
        self.tiles = self.game.sprite.get_spritesheet_map_tiles(season)
        
    def set_random_season(self):
        season = random.choice(["spring","summer","fall","winter"]) + "_outdoors"
        self.set_season(season)
        
    def generate_background_layers(self):
        for j in range(0,self.map_height):
            for i in range(0,self.map_width):
                bg_tile = self.bg_layer[j*self.map_width+i]
                bldg_tile = self.bldg_layer[j*self.map_width+i]
                if bg_tile and bg_tile < len(self.tiles): 
                    self.bg.blit(self.tiles[bg_tile], (i*16,j*16))
                if bldg_tile and bldg_tile < len(self.tiles):
                    self.bg.blit(self.tiles[bldg_tile], (i*16,j*16))
                    
    def generate_foreground_layers(self):
        for j in range(0,self.map_height):
            for i in range(0,self.map_width):
                front_tile = self.front_layer[j*self.map_width+i]
                afront_tile = self.always_front_layer[j*self.map_width+i]
                if front_tile and front_tile < len(self.tiles): 
                    self.fg.blit(self.tiles[front_tile], (i*16,j*16))
                if afront_tile and afront_tile < len(self.tiles):
                    self.fg.blit(self.tiles[afront_tile], (i*16,j*16))
                    
    def init_active_map(self):
        self.game.player.set_map_width(self.map_width)
        self.game.player.set_map_height(self.map_height)
        self.new_map = False
        
    def tick(self):
        if self.new_map:
            self.init_active_map()
        
    def render_back(self, screen):
        top_left_x = min(max(self.game.player.x-screen.get_width()/2,0),self.map_width*16-screen.get_width())
        top_left_y = min(max(self.game.player.y-screen.get_height()/2,0),self.map_height*16-screen.get_height())
        screen.blit(self.bg, (0,0), (top_left_x,top_left_y,screen.get_width(),screen.get_height()))
        
    def render_front(self, screen):
        screen.fill(pygame.Color(0,0,0,0))
        top_left_x = min(max(self.game.player.x-screen.get_width()/2,0),self.map_width*16-screen.get_width())
        top_left_y = min(max(self.game.player.y-screen.get_height()/2,0),self.map_height*16-screen.get_height())
        screen.blit(self.fg, (0,0), (top_left_x,top_left_y,screen.get_width(),screen.get_height()))