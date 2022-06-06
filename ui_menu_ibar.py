import pygame

class InventoryBar:

    def __init__(self, game, ui):
        print("Initializing UI-IBar")
        self.game = game
        self.ui = ui
        
        self.spritesheet = game.sprite.get_tiles("MenuTiles")
        self.last_selection = -1
        self.selection = 0
        
        
        self.ibar_sprite = pygame.Surface((800,96), pygame.SRCALPHA).convert_alpha()
        self.ibar_enabled = True
        
        
        self.tile_width = self.spritesheet[9].get_width()
        
        left_bar = (0,16,16,32)
        right_bar = (44,16,20,32)
        top_bar = (16,0,32,16)
        bottom_bar = (12,44,32,16)
        
        self.ibar_sprite.blit(self.spritesheet[16], (0,0), (0,0,64,64))
        self.ibar_sprite.blit(self.spritesheet[16], (0,36), (0,0,64,64))
        self.ibar_sprite.blit(self.spritesheet[16], (0,35), left_bar)
        
        self.ibar_sprite.blit(self.spritesheet[16], (800-60,0), (0,0,64,64))
        self.ibar_sprite.blit(self.spritesheet[16], (800-60,36), (0,0,64,64))
        self.ibar_sprite.blit(self.spritesheet[16], (784,36), right_bar)     # right bar
        
        for i in range(24):
            self.ibar_sprite.blit(self.spritesheet[16], (16+i*32,0), top_bar)
            self.ibar_sprite.blit(self.spritesheet[16], (16+i*32,80), bottom_bar)
        
        tile_width = self.spritesheet[9].get_width()
        for i in range(12):
            self.ibar_sprite.blit(self.spritesheet[9], (16+tile_width*i,16), (0,0,64,64))
            self.ibar_sprite.blit(self.spritesheet[10], (16+tile_width*i,16), (0,0,64,64))
        
        self.ibar_sprite_x = int(self.game.menu_surface.get_width()/2- self.ibar_sprite.get_width()/2)
        self.ibar_sprite_y = self.game.menu_surface.get_height() - self.ibar_sprite.get_height() - 2
            
    def tick(self):
        pass
        
    def change_selection(self, select):
        if select == self.selection: return
        self.last_selection = self.selection
        self.selection = select
    
    def render(self, screen):
        if self.ibar_enabled:
            self.ibar_sprite.blit(self.spritesheet[56], (16+self.tile_width*self.selection,16), (0,0,64,64))
            if self.last_selection > -1:
                self.ibar_sprite.blit(self.spritesheet[9], (16+self.tile_width*self.last_selection,16), (0,0,64,64))
                self.ibar_sprite.blit(self.spritesheet[10], (16+self.tile_width*self.last_selection,16), (0,0,64,64))
                self.last_selection = -1
            screen.blit(self.ibar_sprite, (self.ibar_sprite_x,self.ibar_sprite_y))
            