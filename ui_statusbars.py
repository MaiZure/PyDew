import random
import pygame

class StatusBars:

    def __init__(self, game, ui):
        print("Initializing UI-StatusBars")
        self.game = game
        self.ui = ui
        
        self.spritesheet = game.sprite.get_spritesheet("Cursors")
        
        self.ebar_enabled = True
        self.hbar_enabled = True
        self.e_rect = pygame.Rect(256, 408, 12, 56)
        self.h_rect = pygame.Rect(268, 408, 12, 56)
        
        self.ebar_sprite = pygame.Surface(self.e_rect.size, pygame.SRCALPHA).convert_alpha()
        self.hbar_sprite = pygame.Surface(self.h_rect.size, pygame.SRCALPHA).convert_alpha()
        
        self.ebar_sprite_x = self.game.config.base_ui_display_width - self.ebar_sprite.get_width() - 2
        self.ebar_sprite_y = self.game.config.base_ui_display_height - self.ebar_sprite.get_height() - 2
        
        self.hbar_sprite_x = self.game.config.base_ui_display_width - self.hbar_sprite.get_width()*2 - 4
        self.hbar_sprite_y = self.game.config.base_ui_display_height - self.hbar_sprite.get_height() - 2
        
        self.generate_energy_bar()
        self.generate_health_bar()
        
        
    def generate_health_bar(self):
        self.hbar_sprite.blit(self.spritesheet, (0,0), self.h_rect)
        health_rect = pygame.Rect(3,12,6,42)
        pygame.draw.rect(self.hbar_sprite,(0,255,0), health_rect)
        
        
        
    def generate_energy_bar(self):
        self.ebar_sprite.blit(self.spritesheet, (0,0), self.e_rect)
        energy_rect = pygame.Rect(3,12,6,42)
        pygame.draw.rect(self.ebar_sprite,(0,255,0), energy_rect)
        

    def tick(self):
        pass
    
    def render(self, screen):
        if self.ebar_enabled:
            screen.blit(self.ebar_sprite, (self.ebar_sprite_x,self.ebar_sprite_y))
        if self.hbar_enabled:
            screen.blit(self.hbar_sprite, (self.hbar_sprite_x,self.hbar_sprite_y))