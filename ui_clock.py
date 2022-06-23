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
        
        self.generate_clock()
        
    
    def generate_clock(self):
        rect = pygame.Rect(333, 431, 72, 58)
        self.clock_sprite = pygame.Surface(rect.size, pygame.SRCALPHA).convert_alpha()
        self.clock_sprite.blit(self.spritesheet, (0,0), rect)
        self.clock_sprite_x = self.game.config.base_display_width - self.clock_sprite.get_width() - 2
        self.clock_sprite_y = 2
        self.time_x = 110
        self.time_y = 24
        
        time = self.get_time_text()
        #WIP
        #self.game.font.set_font("smallfont")
        #self.game.font.draw_text(time, self.clock_sprite, (self.time_x, self.time_y), scaling_cut = 2, justify="right")
        
    def get_time_text(self) -> str:
        minute = self.game.world.minute
        hour = self.game.world.hour
        meridian = "am" if hour < 12 else "pm"
        
        minute_text = "00" if minute == 0 else str(minute)
        hour_text = str(hour) if hour < 12 else str(hour-12)
        return hour_text + ":"+minute_text+" "+meridian
        
    def get_day_text(self) -> str:
        day = str(self.game.config.day)
        weekday = ["","Mon.","Tue.","Wed.", "Thu.", "Fri.", "Sat.", "Sun."][self.game.config.weekday]
        
        
    
    def tick(self):
        pass
    
    def render(self, screen):
        screen.blit(self.clock_sprite, (self.clock_sprite_x, self.clock_sprite_y))
        
        