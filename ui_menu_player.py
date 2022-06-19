import pygame, random

class PlayerMenu:

    def __init__(self, game, ui):
        print("Initializing Player Menu")
        self.game = game
        self.ui = ui
        
        self.scaling = 4
        self.spritesheet = ui.spritesheet
        self.cursors = self.game.sprite.get_spritesheet("Cursors")
        self.tabs = self.game.sprite.get_tiles("Cursors")[1012:1020]
        self.tabs = self.game.sprite.rescale_tiles(self.tabs,self.scaling)
        self.menu_top_left_x = 0
        self.menu_top_left_y = 0
        
        self.bg = []
        self.bg.append(self.game.sprite.get_tiles("daybg")[0])
        
        rect = pygame.Rect(0, 428, 160, 10)
        skill_symbols_sheet = pygame.Surface(rect.size, pygame.SRCALPHA).convert_alpha()
        skill_symbols_sheet.blit(self.cursors, (0,0), rect)
        
        self.skill_symbols = []
        for i in range(16):
            rect = pygame.Rect(i*10, 0, 10, 10)
            surf = pygame.Surface((10,10), pygame.SRCALPHA)
            surf.blit(skill_symbols_sheet, (0,0), rect)
            surf = pygame.transform.scale(surf, (40,40))
            self.skill_symbols.append(surf)
            
        self.pip_small = []
        self.pip_large = []
        
        rect = pygame.Rect(129, 338, 7, 9)
        surf = pygame.Surface(rect.size, pygame.SRCALPHA).convert_alpha()
        surf.blit(self.cursors, (0,0), rect)
        surf = pygame.transform.scale(surf, (7*self.scaling,9*self.scaling))
        self.pip_small.append(surf.copy())
        surf = pygame.Surface(rect.size, pygame.SRCALPHA).convert_alpha()
        rect = pygame.Rect(137, 338, 7, 9)
        surf.blit(self.cursors, (0,0), rect)
        surf = pygame.transform.scale(surf, (7*self.scaling,9*self.scaling))
        self.pip_small.append(surf.copy())
        
        rect = pygame.Rect(145, 338, 13, 9)
        surf = pygame.Surface(rect.size, pygame.SRCALPHA).convert_alpha()
        surf.blit(self.cursors, (0,0), rect)
        surf = pygame.transform.scale(surf, (13*self.scaling,9*self.scaling))
        self.pip_large.append(surf.copy())
        surf = pygame.Surface(rect.size, pygame.SRCALPHA).convert_alpha()
        rect = pygame.Rect(159, 338, 13, 9)
        surf.blit(self.cursors, (0,0), rect)
        surf = pygame.transform.scale(surf, (13*self.scaling,9*self.scaling))
        self.pip_large.append(surf.copy())
        
        self.active_menu = 0
        self.tab_bar = None
        self.tab_selected = 0
        
        self.inventory_menu_sprite = pygame.Surface((self.game.menu_surface.get_width(),self.game.menu_surface.get_height()), pygame.SRCALPHA).convert_alpha()
        self.skill_menu_sprite = pygame.Surface((self.game.menu_surface.get_width(),self.game.menu_surface.get_height()), pygame.SRCALPHA).convert_alpha()
        
        self.tile_width = self.scaling*16
        self.menu_clickrect = pygame.Rect(0,0,0,0)
        self.tabs_clickrect = pygame.Rect(0,0,0,0)
        
        self.menu = None
        self.generate_menus() 
    
    @property
    def tabs_top_left_x(self): return self.menu_top_left_x+72
    @property
    def tabs_top_left_y(self): return self.menu_top_left_y-48
    @property
    def tab_width(self): return self.tabs[0].get_width()
    
    def update_tab_clickrect(self):
        self.tabs_clickrect = pygame.Rect(self.tabs_top_left_x,
            self.tabs_top_left_y,
            self.tabs[0].get_width()*len(self.tabs),
            self.tabs[0].get_height())
            
    def generate_menus(self):
        self.generate_menu_tabs()
        self.generate_inventory_menu()
        
        # Draw them all to their own surfaces then just swap...eventually (maybe?)
        #self.generate_skill_menu()
        #self.generate_map_menu()
        #self.generate_relationship_menu()
        #self.generate_craft_menu()
        #self.generate_item_menu()
        #self.generate_option_menu()
        #self.generate_quit_menu()
        self.update_tab_clickrect()
        
    def generate_menu_tabs(self):
        count = len(self.tabs)
        tab_width = self.tabs[0].get_width()
        size = (tab_width*count,self.tabs[0].get_height()+8) #+8 for selected tab
        self.tab_bar = pygame.Surface(size,pygame.SRCALPHA)
        for i in range(count):
            yoff = 8 if i == self.tab_selected else 0
            self.tab_bar.blit(self.tabs[i],(i*tab_width,yoff))
            
    def change_tab(self, new_tab):
        if self.tab_selected == new_tab:
            return
            
        # No need to regenerate? Just swap out display surface
        if new_tab == 0: self.generate_inventory_menu()
        if new_tab == 1: self.generate_skill_menu()
        if new_tab == 2: self.generate_relationship_menu()
        if new_tab == 3: self.generate_map_menu()
        if new_tab == 4: self.generate_craft_menu()
        if new_tab == 5: self.generate_item_menu()
        if new_tab == 6: self.generate_option_menu()
        if new_tab == 7: self.generate_quit_menu()
        
        self.tab_selected = new_tab
               
        self.generate_menu_tabs()
        
    def generate_inventory_menu(self):
        frame_width = 14
        frame_height = 9
        mid_point = int(frame_height/2)
        self.menu = self.generate_menu_frame(frame_width,frame_height)
        self.menu_top_left_x = int(self.game.menu_surface.get_width()/2 - self.menu.get_width()/2)
        self.menu_top_left_y = int(self.game.menu_surface.get_height()/2 - self.menu.get_height()/2)

        # Cross Bar
        self.menu.blit(self.spritesheet[4],(0,mid_point*64))
        self.menu.blit(self.spritesheet[7],(frame_width*64-64,mid_point*64))
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
            
        #Player Equip Slots
        self.menu.blit(self.spritesheet[41],(52,312))
        self.menu.blit(self.spritesheet[41],(52,376))
        self.menu.blit(self.spritesheet[40],(52,440))
        self.menu.blit(self.bg[0],(124,312))  # Portrait 
        self.menu.blit(self.spritesheet[42],(260,312))
        self.menu.blit(self.spritesheet[69],(260,376))
        self.menu.blit(self.spritesheet[68],(260,440))
            
        # Text
        self.game.font.set_font("spritefont1")
        self.game.font.draw_text(self.game.data.farm_name+" Farm", self.menu, (580, 324), justify="center")
        self.game.font.draw_text("Current Funds: 500g", self.menu, (580, 388), justify="center")
        self.game.font.draw_text("Total Earnings: 0g", self.menu, (580, 452), justify="center")
        
    def generate_skill_menu(self):
        frame_width = 14
        frame_height = 9
        mid_point = int(frame_height/2)
        self.menu = self.generate_menu_frame(frame_width,frame_height)
        
        
        # Portrait
        self.menu.blit(self.bg[0],(56,68))  
        
        # Text
        self.game.font.set_font("smallfont")
        self.game.font.draw_text("Farming", self.menu, (328, 64), justify = "right")
        self.game.font.draw_text("Mining", self.menu, (328, 120), justify = "right")
        self.game.font.draw_text("Foraging", self.menu, (328, 172), justify = "right")
        self.game.font.draw_text("Fishing", self.menu, (328, 224), justify = "right")
        self.game.font.draw_text("Combat", self.menu, (328, 276), justify = "right")
        
        # Skill symbols
        self.menu.blit(self.skill_symbols[1],(336,56))
        self.menu.blit(self.skill_symbols[3],(336,112))
        self.menu.blit(self.skill_symbols[6],(336,164))
        self.menu.blit(self.skill_symbols[2],(336,216))
        self.menu.blit(self.skill_symbols[12],(336,268))
        
        # Skill pips
        for x in range(4):
            self.menu.blit(self.pip_small[x+1 <= self.game.data.farming_skill],(392 + 36*x,56))
            self.menu.blit(self.pip_small[x+1 <= self.game.data.mining_skill],(392 + 36*x,112))
            self.menu.blit(self.pip_small[x+1 <= self.game.data.foraging_skill],(392 + 36*x,164))
            self.menu.blit(self.pip_small[x+1 <= self.game.data.fishing_skill],(392 + 36*x,216))
            self.menu.blit(self.pip_small[x+1 <= self.game.data.combat_skill],(392 + 36*x,268))
            
        self.menu.blit(self.pip_large[5 <= self.game.data.farming_skill],(536, 56))
        self.menu.blit(self.pip_large[5 <= self.game.data.mining_skill],(536, 112))
        self.menu.blit(self.pip_large[5 <= self.game.data.foraging_skill],(536, 164))
        self.menu.blit(self.pip_large[5 <= self.game.data.fishing_skill],(536, 216))
        self.menu.blit(self.pip_large[5 <= self.game.data.combat_skill],(536, 268))
        
        self.menu.blit(self.pip_large[10 <= self.game.data.farming_skill],(740, 56))
        self.menu.blit(self.pip_large[10 <= self.game.data.mining_skill],(740, 112))
        self.menu.blit(self.pip_large[10 <= self.game.data.foraging_skill],(740, 164))
        self.menu.blit(self.pip_large[10 <= self.game.data.fishing_skill],(740, 216))
        self.menu.blit(self.pip_large[10 <= self.game.data.combat_skill],(740, 268))
            
        for x in range(4):
            self.menu.blit(self.pip_small[x+6 <= self.game.data.farming_skill],(596 + 36*x,56))
            self.menu.blit(self.pip_small[x+6 <= self.game.data.mining_skill],(596 + 36*x,112))
            self.menu.blit(self.pip_small[x+6 <= self.game.data.foraging_skill],(596 + 36*x,164))
            self.menu.blit(self.pip_small[x+6 <= self.game.data.fishing_skill],(596 + 36*x,216))
            self.menu.blit(self.pip_small[x+6 <= self.game.data.combat_skill],(596 + 36*x,268))
            
    def generate_relationship_menu(self):
        frame_width = 15
        frame_height = 9
        mid_point = int(frame_height/2)
        self.menu = self.generate_menu_frame(frame_width,frame_height)
        
    def generate_craft_menu(self):
        frame_width = 14
        frame_height = 9
        cross_bar = 4.5
        self.menu = self.generate_menu_frame(frame_width,frame_height)
        
        # Cross Bar
        self.menu.blit(self.spritesheet[4],(0,cross_bar*64))
        self.menu.blit(self.spritesheet[7],(frame_width*64-64,cross_bar*64))
        for i in range(1,frame_width-1):
            self.menu.blit(self.spritesheet[6],(i*64,cross_bar*64))
            
        # Inventory Blocks
        for i in range(12):
            inv_sprite = 10
            self.menu.blit(self.spritesheet[inv_sprite],(64+i*64,332))
            
            if self.game.player.inventory_limit < 24: inv_sprite = 57
            self.menu.blit(self.spritesheet[inv_sprite],(64+i*64,396))
            
            if self.game.player.inventory_limit < 36: inv_sprite = 57
            self.menu.blit(self.spritesheet[inv_sprite],(64+i*64,460)) 
    
    def generate_map_menu(self):
        pass
        
    def generate_item_menu(self):
        frame_width = 13
        frame_height = 9
        mid_point = int(frame_height/2)
        self.menu = self.generate_menu_frame(frame_width,frame_height)
        
    def generate_option_menu(self):
        frame_width = 14
        frame_height = 9
        mid_point = int(frame_height/2)
        self.menu = self.generate_menu_frame(frame_width,frame_height)
        
    def generate_quit_menu(self):
        frame_width = 13
        frame_height = 9
        mid_point = int(frame_height/2)
        self.menu = self.generate_menu_frame(frame_width,frame_height)
        
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
        
        
    def handle_input(self, event):
        pos = pygame.mouse.get_pos()
        if event.button == 1:
            if self.tabs_clickrect.collidepoint(pos):
                new_tab = int((pos[0]-self.tabs_top_left_x)/self.tab_width)
                self.change_tab(new_tab)
                return
        
    def tick(self):
        pass
    
    def render(self, screen):
        if not self.ui.player_menu_enabled:
            return
            
        screen.blit(self.menu,(self.menu_top_left_x,self.menu_top_left_y))
        screen.blit(self.tab_bar,(self.tabs_top_left_x,self.tabs_top_left_y))
    