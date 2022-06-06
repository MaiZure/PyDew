import pygame

class InventoryBar:

    def __init__(self, game, ui):
        print("Initializing UI-IBar")
        self.game = game
        self.ui = ui
        
        self.spritesheet = game.sprite.get_tiles("MenuTiles")
        
        
        self.ibar_sprite = pygame.Surface((800,96), pygame.SRCALPHA).convert_alpha()
        self.ibar_enabled = True
        
        self.ibar_sprite.blit(self.spritesheet[16], (0,0), (0,0,64,64))
        self.ibar_sprite_x = self.game.menu_surface.get_width()- self.ibar_sprite.get_width()
        self.ibar_sprite_y = self.game.menu_surface.get_height() - self.ibar_sprite.get_height() - 2
            
    def tick(self):
        pass
    
    def render(self, screen):
        if self.ibar_enabled:
            print("blitting at (" + str(self.ibar_sprite_x)+","+str(self.ibar_sprite_y))
            screen.blit(self.ibar_sprite, (self.ibar_sprite_x,self.ibar_sprite_y))