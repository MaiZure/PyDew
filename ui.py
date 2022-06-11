import random
import pygame
from ui_clock import Clock
from ui_statusbars import StatusBars
from ui_menu_ibar import InventoryBar
class UI:

    def __init__(self, game):
        print("Initializing UI")
        self.game = game

        self.ui_elements = []
        self.menu_elements = []
        self.tiny_numbers_rect=[]
        
        
        
    def init_second_stage(self):
        self.ui_elements.append(Clock(self.game,self))
        self.ui_elements.append(StatusBars(self.game,self))
        self.menu_elements.append(InventoryBar(self.game, self))
        self.ibar = self.menu_elements[0]
        
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
    
    def ui_render(self, screen):
        for element in self.ui_elements:
            element.render(screen)
            
    def menu_render(self, screen):
        for element in self.menu_elements:
            element.render(screen)