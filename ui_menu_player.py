import pygame, random

class PlayerMenu:

    def __init__(self, game, ui):
        print("Initializing Player Menu")
        self.game = game
        self.ui = ui
        
        self.spritesheet = ui.spritesheet
        self.scaling = 4
        
        self.menu_sprite = pygame.Surface((800,96), pygame.SRCALPHA).convert_alpha()        
        self.menu_sprite_x = int(self.game.menu_surface.get_width()/2- self.menu_sprite.get_width()/2)
        self.menu_sprite_y_top = 2
        
        self.tile_width = self.scaling*16
        self.menu_clickrect = pygame.Rect(0,0,0,0)
        
        self.generate_menus()
        
            
    def generate_menus(self):
        pass
        
    
    def handle_mouse(self, event):
        if event.button == 1:
            pass
        
    def tick(self):
        pass
    
    def render(self, screen):
        if not self.ui.player_menu_enabled:
            return
    
    def update_clickrect(self):
        pass