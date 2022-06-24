import random
import pygame
from ui_clock import Clock
from ui_statusbars import StatusBars
from ui_menu_ibar import InventoryBar
from ui_menu_player import PlayerMenu
class UI:

    def __init__(self, game):
        print("Initializing UI")
        self.game = game

        self.ui_elements = []
        self.menu_elements = []
        self.tiny_numbers_rect=[]
        self.player_menu_enabled = False
        #self.ibar = None
        
    @property
    def ibar(self): return self.menu_elements[0]
    @property
    def player_menu(self): return self.menu_elements[1]
    @property
    def clock(self): return self.ui_elements[0]
    @property
    def statusbars(self): return self.ui_elements[1]
    
    def init_second_stage(self):
        self.spritesheet = self.game.sprite.get_tiles("MenuTiles")
        self.ui_elements.append(Clock(self.game,self))
        self.ui_elements.append(StatusBars(self.game,self))
        self.menu_elements.append(InventoryBar(self.game, self))
        self.menu_elements.append(PlayerMenu(self.game, self))
        #self.ibar = self.menu_elements[0]
        
        #Get tiny inventory count numbers
        self.spritesheet = self.game.sprite.get_spritesheet("Cursors")
        rect = pygame.Rect(368,56,50,7)
        temp = pygame.Surface(rect.size, pygame.SRCALPHA).convert_alpha()
        temp.blit(self.spritesheet, (0,0), rect)
        self.tiny_numbers = pygame.Surface((150,21), pygame.SRCALPHA).convert_alpha()
        self.tiny_numbers = pygame.transform.scale(temp,self.tiny_numbers.get_rect().size)
        #self.tiny_numbers.blit(self.spritesheet, (0,0), rect)
        for i in range(10): self.tiny_numbers_rect.append(pygame.Rect(i*15,0,15,21))
        
        
    def tick(self):
        for element in self.menu_elements:
            element.tick()
        for element in self.ui_elements:
            element.tick()
    
    def ui_render(self, screen):
        for element in self.ui_elements:
            element.render(screen)
            
    def ui_render_text(self, screen):
        for element in self.ui_elements:
            if hasattr(element, "render_text"):
                element.render_text(screen)
            
    def menu_render(self, screen):
        screen.fill((0,0,0,0)) if not self.player_menu_enabled else screen.fill((0,0,0,128))
        for element in self.menu_elements:
            element.render(screen)
            
    def toggle_player_menu(self):
        self.activate_player_menu() if not self.game.paused else self.deactivate_player_menu()
            
    def activate_player_menu(self):
        self.game.paused = True
        self.ibar.ibar_enabled = False
        self.player_menu_enabled = True
              
    def deactivate_player_menu(self):
        
        self.player_menu_enabled = False
        self.ibar.ibar_enabled = True
        self.game.paused = False