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
        self.season_rect = pygame.Rect(406, 441+(self.game.data.season*8), 12, 8)
        self.weather_rect = pygame.Rect(329+(self.game.data.weather*12), 421, 12, 8)
        self.arrow_rect = pygame.Rect(324,477,7,19) # Double length of surface to set origin for rotation
        
        self.season_icon = None
        self.season_icon_x = 53
        self.season_icon_y = 16
        
        self.weather_icon = None
        self.weather_icon_x = 29
        self.weather_icon_y = 16
        
        self.arrow = None
        self.arrow_x = 22
        self.arrow_y = 19
        
        self.generate_clock()
        

        
        
        self.update_text()
    
    def generate_clock(self):
        self.clock_sprite = pygame.Surface(self.clock_rect.size, pygame.SRCALPHA).convert_alpha()
        self.clock_sprite.blit(self.spritesheet, (0,0), self.clock_rect)
        self.clock_sprite_x = self.game.config.base_ui_display_width - self.clock_sprite.get_width() - 2
        self.clock_sprite_y = 2
        self.season_icon = pygame.Surface(self.season_rect.size)
        self.season_icon.blit(self.spritesheet, (0,0), self.season_rect)
        self.clock_sprite.blit(self.season_icon, (self.season_icon_x, self.season_icon_y))
        self.weather_icon = pygame.Surface(self.weather_rect.size)
        self.weather_icon.blit(self.spritesheet, (0,0), self.weather_rect)
        self.clock_sprite.blit(self.weather_icon, (self.weather_icon_x, self.weather_icon_y))
        
        arrow_surf_size = (self.arrow_rect[0], (self.arrow_rect[1]*2)-2)
        self.arrow = pygame.Surface(arrow_surf_size, pygame.SRCALPHA).convert_alpha()
        self.arrow.blit(self.spritesheet, (0,0), self.arrow_rect)
        #self.arrow = pygame.transform.rotate(self.arrow,3)
        
        
    def update_text(self):
        self.text_layer = pygame.Surface((self.clock_rect.size[0]*4,self.clock_rect.size[1]*4), pygame.SRCALPHA)  
        self.day_x = 192
        self.day_y = 14
        
        self.time_x = 256#1000
        self.time_y = 106#88
        
        
        
        time = self.get_time_text()
        day = self.get_day_text()
        self.game.font.set_font("SpriteFont1")
        
        #Day of season
        self.game.font.draw_text(day, self.text_layer, (self.day_x, self.day_y), scaling_cut = 1, justify="center")
        
        #Time of day
        self.game.font.draw_text(time, self.text_layer, (self.time_x, self.time_y), scaling_cut = 1, justify="right")
        
        
    def get_time_text(self) -> str:
        minute = self.game.world.minute
        hour = self.game.world.hour
        meridian = "am" if hour < 12 else "pm"
        
        minute_text = "00" if minute == 0 else str(minute)
        hour_text = str(hour) if hour < 13 else str(hour-12)
        return hour_text + ":"+minute_text+" "+meridian
        
    def get_weekday_text(self, day_num = 0) -> str:
        day_num = self.game.data.day-1 if day_num == 0 else day_num-1
        day_index = day_num % 7 
        return ["Mon.","Tue.","Wed.", "Thu.", "Fri.", "Sat.", "Sun."][day_index]  
        
    def get_day_text(self) -> str:
        weekday = self.get_weekday_text()
        day_num = str(self.game.data.day)
        return weekday + " " + day_num
    
    def tick(self):
        if self.update_time:
            self.update_text()
            self.update_time = False
            
    def trigger_update(self):
        self.update_time = True
    
    def render(self, screen):
        screen.blit(self.clock_sprite, (self.clock_sprite_x, self.clock_sprite_y))
        screen.blit(self.arrow, (self.clock_sprite_x+self.arrow_x-3, self.clock_sprite_y+self.arrow_y-16))
        
    def render_text(self, screen):
        screen.blit(self.text_layer, (self.clock_sprite_x*4,self.clock_sprite_y*4))
        