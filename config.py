

class Config:
    def __init__(self):
        print("Initializing Config")
        
        self.screen_width = 1440  #1920 is typical
        self.screen_height = 810  #1080 is typical
        self.screen_scaling = 3   #4 is typical
        self.fps = 60
        
        self.base_display_width = int(self.screen_width / self.screen_scaling)
        self.base_display_height = int(self.screen_height / self.screen_scaling)
        self.base_display_tile_width = int(self.base_display_width/16)
        self.base_display_tile_height = int(self.base_display_height/16)
        
        