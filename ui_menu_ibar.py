import pygame, random

class InventoryBar:

    def __init__(self, game, ui):
        print("Initializing UI-IBar")
        self.game = game
        self.ui = ui
        
        self.spritesheet = ui.spritesheet
        self.last_selection = -1
        self.selection = 0
        self.scaling = 4
        self.slot_pos = [[],[]] # bottom vs top positions
        self.ibar_row = 0
        
        self.ibar_sprite = pygame.Surface((800,96), pygame.SRCALPHA).convert_alpha()
        self.ibar_enabled = True
        self.redraw_inventory = True
        self.redraw_ibar_selection = True
        
        self.ibar_top = False
        self.ibar_sprite_x = int(self.game.menu_surface.get_width()/2 - self.ibar_sprite.get_width()/2)
        self.ibar_sprite_y_bottom = self.game.menu_surface.get_height() - self.ibar_sprite.get_height() - 2
        self.ibar_sprite_y_top = 2
        self.ibar_sprite_y = self.ibar_sprite_y_bottom
        
        self.tile_width = self.scaling*16
        self.ibar_clickrect = pygame.Rect(0,0,0,0)
        
        self.generate_ibar()
        
            
    def generate_ibar(self):
        left_bar = (0,16,16,32)
        right_bar = (44,16,20,32)
        top_bar = (16,0,32,16)
        bottom_bar = (12,44,32,16)
        
        
        self.ibar_sprite.blit(self.spritesheet[16], (0,0), (0,0,64,64))
        self.ibar_sprite.blit(self.spritesheet[16], (0,36), (0,0,64,64))
        self.ibar_sprite.blit(self.spritesheet[16], (0,35), left_bar)
        
        self.ibar_sprite.blit(self.spritesheet[16], (800-60,0), (0,0,64,64))
        self.ibar_sprite.blit(self.spritesheet[16], (800-60,36), (0,0,64,64))
        self.ibar_sprite.blit(self.spritesheet[16], (784,36), right_bar)
        
        for i in range(24):
            self.ibar_sprite.blit(self.spritesheet[16], (16+i*32,0), top_bar)
            self.ibar_sprite.blit(self.spritesheet[16], (16+i*32,80), bottom_bar)
        
        for i in range(12):
            slot_x = (4*self.scaling)+(self.tile_width*i)
            slot_y = (4*self.scaling)
            self.slot_pos[False].append((slot_x,slot_y))
            self.slot_pos[True].append((slot_x,slot_y))
            self.ibar_sprite.blit(self.spritesheet[9], (slot_x, slot_y), (0,0,64,64))
            self.ibar_sprite.blit(self.spritesheet[10], (slot_x, slot_y), (0,0,64,64))
        
        self.update_clickrect()
        self.redraw_inventory = True
        
    
    def handle_mouse(self, event):
        if event.button == 1:
            pos = pygame.mouse.get_pos()
            inv_tile_num = self.get_inventory_slot_num(pos)
            self.change_selection(inv_tile_num)
            return
        if event.button == 4:
            next_tile = self.selection - 1
            if next_tile < 0: next_tile = 11
            self.change_selection(next_tile)
        if event.button == 5:
            next_tile = self.selection + 1
            if next_tile > 11: next_tile = 0
            self.change_selection(next_tile)
        
    def tick(self):
        self.ibar_sprite_y = self.ibar_sprite_y_bottom
        self.ibar_top = False

        if int(self.game.player.y - self.game.world.top_left_y) > (self.game.bg_surface.get_height()/2+5):
            self.ibar_sprite_y = self.ibar_sprite_y_top
            self.ibar_top = True
        self.update_clickrect()  # Should update on CHANGE, not every frame
        
        pos = pygame.mouse.get_pos()
        if self.ibar_clickrect.collidepoint(pos):
            inv_tile_num = self.get_inventory_slot_num(pos)
            if self.game.player.inventory[inv_tile_num]:
                self.ui.item_hover = self.game.player.inventory[inv_tile_num]
            
        
    def change_selection(self, select):
        if select == self.selection: return
        self.last_selection = self.selection
        self.selection = select
        self.redraw_ibar_selection = True
        self.redraw_inventory = True
        
    def force_redraw(self):
        self.last_selection = self.selection
        self.redraw_ibar_selection = True
        self.redraw_inventory = True
    
    def render(self, screen):
        if not self.ibar_enabled:
            return
        
        if self.redraw_ibar_selection:
            self.redraw_ibar_selection = False           
            if self.last_selection > -1:
                self.ibar_sprite.blit(self.spritesheet[9], (16+self.tile_width*self.last_selection,16), (0,0,64,64))
                self.ibar_sprite.blit(self.spritesheet[10], (16+self.tile_width*self.last_selection,16), (0,0,64,64))
                self.last_selection = -1
            self.ibar_sprite.blit(self.spritesheet[56], (16+self.tile_width*self.selection,16), (0,0,64,64))
            
        # Probably don't need to redraw items on every frame eh?
        if self.redraw_inventory:
            self.redraw_inventory = False
            for i in range(self.ibar_row, self.ibar_row+12):
                item = self.game.player.inventory[i]
                if item:
                    item.render_inv(self.ibar_sprite, i)
                
        screen.blit(self.ibar_sprite, (self.ibar_sprite_x,self.ibar_sprite_y))
    
    def update_clickrect(self):
        self.ibar_clickrect = pygame.Rect(self.ibar_sprite_x+4*self.scaling,
            self.ibar_sprite_y+4*self.scaling, 12*16*self.scaling,16*self.scaling)
            
    def get_inventory_slot_num(self, pos):
        return int((pos[0] - self.ibar_clickrect[0]) / (16*self.scaling))