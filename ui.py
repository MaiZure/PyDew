import random
import pygame

class UI:

    def __init__(self, game):
        print("Initializing UI")
        self.game = game
        
        cursors = ".\\Tiles\\Cursors.png"
        
        self.spritesheet = game.sprite.get_spritesheet("cursors")
        
        rect = pygame.Rect(333, 431, 72, 58)
        self.clock_sprite = pygame.Surface(rect.size, pygame.SRCALPHA).convert_alpha()
        self.clock_sprite.blit(self.spritesheet, (0,0), rect)
        self.clock_sprite_x = self.game.config.base_display_width - self.clock_sprite.get_width() - 2

    
    def tick(self):
        pass
    
    def render(self, screen):
        screen.blit(self.clock_sprite, (self.clock_sprite_x,2))