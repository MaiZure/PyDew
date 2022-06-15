import pygame, random

class PlayerMenu:

    def __init__(self, game, ui):
        print("Initializing Player Menu")
        self.game = game
        self.ui = ui
        
        self.spritesheet = ui.spritesheet
        self.tabs = self.game.sprite.get_tiles("Cursors")[1012:1020]
        self.tabs = self.game.sprite.rescale_tiles(self.tabs,4)
        self.scaling = 4
        self.menu_top_left_x = 0
        self.menu_top_left_y = 0
        self.active_menu = 0
        self.tab_bar = None
        
        self.inventory_menu_sprite = pygame.Surface((self.game.menu_surface.get_width(),self.game.menu_surface.get_height()), pygame.SRCALPHA).convert_alpha()
        
        self.tile_width = self.scaling*16
        self.menu_clickrect = pygame.Rect(0,0,0,0)
        
        self.menu = None
        self.generate_menus() 
            
    def generate_menus(self):
        self.generate_menu_tabs()
        self.generate_inventory_menu()
        self.generate_skill_menu()
        self.generate_relationship_menu()
        self.generate_craft_menu()
        self.generate_item_menu()
        self.generate_settings_menu()
        self.generate_quit_menu()
        
    def generate_menu_tabs(self):
        # BAD - Tabs need to be individual
        count = len(self.tabs)
        tab_width = self.tabs[0].get_width()
        size = (tab_width*count,self.tabs[0].get_height())
        self.tab_bar = pygame.Surface(size,pygame.SRCALPHA)
        for i in range(count):
            self.tab_bar.blit(self.tabs[i],(i*tab_width,0))      
        
    def generate_inventory_menu(self):
        frame_width = 14
        frame_height = 9
        mid_point = int(frame_height/2)
        self.menu = self.generate_menu_frame(frame_width,frame_height)
        self.menu_top_left_x = int(self.game.menu_surface.get_width()/2 - self.menu.get_width()/2)
        self.menu_top_left_y = int(self.game.menu_surface.get_height()/2 - self.menu.get_height()/2)
              
        self.menu.blit(self.spritesheet[4],(0,mid_point*64))
        self.menu.blit(self.spritesheet[7],(frame_width*64-64,mid_point*64))
        
        # Cross Bar
        for i in range(1,frame_width-1):
            self.menu.blit(self.spritesheet[6],(i*64,mid_point*64))
        
        # Inventory Blocks
        for i in range(12):
            inv_sprite = 10
            self.menu.blit(self.spritesheet[inv_sprite],(64+i*64,52))
            
            if self.game.player.inventory_limit < 24: inv_sprite = 57
            self.menu.blit(self.spritesheet[inv_sprite],(64+i*64,132))
            
            if self.game.player.inventory_limit < 36: inv_sprite = 57
            self.menu.blit(self.spritesheet[inv_sprite],(64+i*64,196)) 
            
        # Text
        self.game.font.set_font("spritefont1")
        self.game.font.draw_text(self.game.data.farm_name+" Farm", self.menu, (448, 324))
    
    def generate_skill_menu(self):
        pass
    
    def generate_relationship_menu(self):
        pass
        
    def generate_craft_menu(self):
        pass
        
    def generate_item_menu(self):
        pass
        
    def generate_settings_menu(self):
        pass
        
    def generate_quit_menu(self):
        pass
        
    def generate_menu_frame(self,x,y):
        w = x * 64
        h = y * 64
        menu = pygame.Surface((w,h), pygame.SRCALPHA).convert_alpha()
        top_left_frame = 0
        top_right_frame = 3
        bottom_left_frame = 12
        bottom_right_frame = 15
        horizonal_top_frame = 2
        horizonal_bottom_frame = 14
        vertical_left_frame = 8
        vertical_right_frame = 11
        bg_frame = 9
        
        menu.blit(pygame.transform.scale(self.spritesheet[bg_frame],(w-64,h-64)), (32,32))
        menu.blit(self.spritesheet[top_left_frame],(0,0))
        menu.blit(self.spritesheet[bottom_left_frame],(0,h-64))
        menu.blit(self.spritesheet[top_right_frame],(w-64,0))
        menu.blit(self.spritesheet[bottom_right_frame],(w-64,h-64))
        
        
        for i in range(1,x-1):
            menu.blit(self.spritesheet[horizonal_top_frame],(i*64,0))
            menu.blit(self.spritesheet[horizonal_bottom_frame],(i*64,h-64))
            if i < y-1:
                menu.blit(self.spritesheet[vertical_left_frame],(0,i*64))
                menu.blit(self.spritesheet[vertical_right_frame],(w-64,i*64))
            
        return menu
        
        
    def handle_mouse(self, event):
        if event.button == 1:
            pass
        
    def tick(self):
        pass
    
    def render(self, screen):
        if not self.ui.player_menu_enabled:
            return
            
        screen.blit(self.menu,(self.menu_top_left_x,self.menu_top_left_y))
        screen.blit(self.tab_bar,(self.menu_top_left_x+72,self.menu_top_left_y-48)) #-40 for down tab
    
    def update_clickrect(self):
        pass