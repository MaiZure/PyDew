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
        self.hbar_px_per_hp = 168 / self.game.data.player_max_hp
        self.ebar_px_per_ep = 168 / self.game.data.player_max_ep
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
        
        
        
    def generate_energy_bar(self):
        self.ebar_sprite.blit(self.spritesheet, (0,0), self.e_rect)
        

    def tick(self):
        pass
    
    def render(self, screen):
        if self.ebar_enabled:
            screen.blit(self.ebar_sprite, (self.ebar_sprite_x,self.ebar_sprite_y))
        if self.hbar_enabled:
            screen.blit(self.hbar_sprite, (self.hbar_sprite_x,self.hbar_sprite_y))
            
    def render_scaled(self, screen):
        self.render_health_bar(screen)
        self.render_energy_bar(screen)
        
    def render_health_bar(self,screen):
        max_bar_height = 168
        half_height = int(max_bar_height/2)
        bar_height = int(max_bar_height - ((self.game.player.max_hp - self.game.player.hp) * self.hbar_px_per_hp))
        hbar_x = self.hbar_sprite_x*4+3*4
        hbar_y = self.hbar_sprite_y*4+13*4-2 + (max_bar_height - bar_height)
        col_rate = 255/half_height
        
        red = 255 if bar_height <= half_height else int(255 - (bar_height-half_height)*col_rate) 
        green = 255 if bar_height >= half_height else int(255 - (half_height-bar_height)*col_rate)
        
        p_color = (max(red,0),max(green,0),0)
        s_color = (int(p_color[0]/1.25), int(p_color[1]/1.25), p_color[2])
        
        health_rect = pygame.Rect(hbar_x,hbar_y,24,bar_height)
        pygame.draw.rect(screen,p_color, health_rect)
        health_rect = pygame.Rect(hbar_x,hbar_y,24,4)
        pygame.draw.rect(screen,s_color, health_rect)
       
        
    # This is mostly duplicated code -- factor out with fxn above
    def render_energy_bar(self,screen):
        max_bar_height = 168
        half_height = int(max_bar_height/2)
        bar_height = int(max_bar_height - ((self.game.player.max_ep - self.game.player.ep) * self.ebar_px_per_ep))
        ebar_x = self.ebar_sprite_x*4+3*4
        ebar_y = self.ebar_sprite_y*4+13*4-2 + (max_bar_height - bar_height)
        col_rate = 255/half_height
        
        red = 255 if bar_height <= half_height else int(255 - (bar_height-half_height)*col_rate) 
        green = 255 if bar_height >= half_height else int(255 - (half_height-bar_height)*col_rate)
        
        p_color = (max(red,0),max(green,0),0)
        s_color = (int(p_color[0]/1.25), int(p_color[1]/1.25), p_color[2])
        
        energy_rect = pygame.Rect(ebar_x,ebar_y,24,bar_height)
        pygame.draw.rect(screen,p_color, energy_rect)
        energy_rect = pygame.Rect(ebar_x,ebar_y,24,4)
        pygame.draw.rect(screen,s_color, energy_rect)
        