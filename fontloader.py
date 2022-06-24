import pygame, json, zlib, base64, os

class FontLoader:
    def __init__(self, game):
        print("Initializing Fonts")
        
        self.game = game
        
        # Load all font in to a library (dictionary)
        self.font = {}
        self.current_font = None
        self.spritesheet = None
        self.current_color = (0,0,0)
        
    def init_second_stage(self):
        self.load_fonts()
        self.current_font = "spritefont1"
        self.spritesheet = self.game.sprite.get_tiles(self.current_font)
        
    def load_fonts(self) -> None:
        path = ".\\Font\\"
        files = os.listdir(path)
        for file in files:
            split = file.split(".")
            name = (split[0]).lower()
            ext = (split[1]).lower()
            if ext == "json":
                self.font[name] = json.load(open(path+file, encoding="ansi"))
                
    def get_character_map(self):
        return self.font[self.current_font]["content"]["characterMap"]
        
    def get_char_index(self, char):
        map = self.get_character_map()
        if char in map:
            return map.index(char)
            
    def get_char_glyph_data(self, char):
        index = self.get_char_index(char)
        return self.font[self.current_font]["content"]["glyphs"][index]
    
    def get_char_cropping(self, char):
        index = self.get_char_index(char)
        return self.font[self.current_font]["content"]["cropping"][index]
    
    def get_char_kerning(self, char):
        index = self.get_char_index(char)
        return self.font[self.current_font]["content"]["kerning"][index]
        
    def set_font(self, name):
        if not name in self.font: return
        self.current_font = name
        self.spritesheet = self.game.sprite.get_tiles(self.current_font)
    
    def get_char_width(self,char):
        return int(self.get_char_glyph_data(char)["width"])
    
    def get_char_height(self,char):
        return int(self.get_char_glyph_data(char)["height"])
    
    def get_line_width(self,char_list):
        width = 0
        for char in char_list:
            crop_wid = self.get_char_cropping(char)["x"]
            char_wid = self.get_char_width(char)
            char_kern = self.get_char_kerning(char)["x"]
            width += max(char_wid, crop_wid) + char_kern 
        return width
     
    def get_line_height(self, char_list):
        height = 0
        for char in char_list:
            #height = max(height, self.get_char_height(char))
            height = max(height, self.get_char_cropping(char)["height"])
        return height
        
    def draw_text(self, str, screen, pos, scaling_cut = 1, justify = "left"):
        chars = [c for c in str]
        width = self.get_line_width(chars)
        height = self.get_line_height(chars)
        cut = scaling_cut
        
        surf = pygame.Surface((width,height), pygame.SRCALPHA)
        current_x = 0
        current_y = 0
        for char in chars:
            current_y = self.get_char_cropping(char)["y"]
            char_data = self.get_char_glyph_data(char)
            crop_wid = self.get_char_cropping(char)["x"]
            rect = (char_data["x"], char_data["y"], char_data["width"], char_data["height"])
            surf.blit(self.spritesheet[0], (current_x, current_y), rect)
            current_x += max(rect[2], crop_wid) + self.get_char_kerning(char)["x"]
        
        # Scale
        if scaling_cut > 1:
            surf = pygame.transform.scale(surf, (int(surf.get_width()/scaling_cut),int(surf.get_height()/scaling_cut)))
        
        colored_text = surf.copy()
        shadow_text = surf.copy()
        
        # Colorize Black
        color_mask = pygame.Surface(surf.get_size()).convert_alpha()
        color_mask.fill(self.current_color)
        colored_text.blit(color_mask, (0,0), special_flags = pygame.BLEND_RGBA_MIN)
        
        # Shadow
        color_mask.fill((210,150,115))
        shadow_text.blit(color_mask, (0,0), special_flags = pygame.BLEND_RGBA_MIN)     
        
        # Main Draw
        x = pos[0]
        y = pos[1]
        if justify == "right": 
            x = pos[0]-width
        if justify == "center":
            x = pos[0]-width/2

        screen.blit(shadow_text, (x-2, y+2))
        screen.blit(colored_text, (x, y))