import random
import pygame

class Clock:

    def __init__(self, game, ui):
        print("Initializing UI-Clock")
        self.game = game
        self.ui = ui
        
        self.spritesheet = self.game.sprite.get_spritesheet("Cursors")
        
        self.time_x = 0
        self.time_y = 0
        self.clock_sprite_x = 0
        self.clock_sprite_y = 0
        self.clock_sprite = None
        self.text_layer = None
        self.update_time = False
        
        self.clock_rect = pygame.Rect(333, 432, 72, 57)
        self.generate_clock()
        self.update_text()
        
    
    def generate_clock(self):
        self.clock_sprite = pygame.Surface(self.clock_rect.size, pygame.SRCALPHA).convert_alpha()
        self.clock_sprite.blit(self.spritesheet, (0,0), self.clock_rect)
        self.clock_sprite_x = self.game.config.base_ui_display_width - self.clock_sprite.get_width() - 2
        self.clock_sprite_y = 2
        
    def update_text(self):
        self.text_layer = pygame.Surface((self.clock_rect.size[0]*4,self.clock_rect.size[1]*4), pygame.SRCALPHA)  
        self.time_x = 168#1000
        self.time_y = 42#88
        
        time = self.get_time_text()
        self.game.font.set_font("SpriteFont1")
        self.game.font.draw_text(time, self.text_layer, (self.time_x, self.time_y), scaling_cut = 1, justify="right")
        
        #self.text_layer = pygame.transform.scale(self.text_layer, (self.text_layer.get_width(),self.text_layer.get_height()))
        
        
    def get_time_text(self) -> str:
        minute = self.game.world.minute
        hour = self.game.world.hour
        meridian = "am" if hour < 12 else "pm"
        
        minute_text = "00" if minute == 0 else str(minute)
        hour_text = str(hour) if hour < 13 else str(hour-12)
        return hour_text + ":"+minute_text+" "+meridian
        
    def get_day_text(self) -> str:
        day = str(self.game.config.day)
        weekday = ["","Mon.","Tue.","Wed.", "Thu.", "Fri.", "Sat.", "Sun."][self.game.config.weekday]
        
        
    
    def tick(self):
        if self.update_time:
            self.update_text()
            self.update_time = False
            
    def trigger_update(self):
        self.update_time = True
    
    def render(self, screen):
        screen.blit(self.clock_sprite, (self.clock_sprite_x, self.clock_sprite_y))
        
    def render_text(self, screen):
        screen.blit(self.text_layer, (1235,72))
        