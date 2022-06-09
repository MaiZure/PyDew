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
        self.ui_elements.append(Clock(game,self))
        self.ui_elements.append(StatusBars(game,self))
    
        self.menu_elements = [InventoryBar(game, self)]
        self.ibar = self.menu_elements[0]
        
        self.spritesheet = game.sprite.get_spritesheet("Cursors")
        
        self.tiny_numbers_rect=[]
        rect = pygame.Rect(368,58,50,7)
        self.tiny_numbers = pygame.Surface(rect.size, pygame.SRCALPHA).convert_alpha()
        self.tiny_numbers.blit(self.spritesheet, (0,0), rect)
        for i in range(10): self.tiny_numbers_rect.append(pygame.Rect(i*5,0,5,7))
        
    def tick(self):
        for element in self.menu_elements:
            element.tick()
    
    def ui_render(self, screen):
        for element in self.ui_elements:
            element.render(screen)
            
    def menu_render(self, screen):
        for element in self.menu_elements:
            element.render(screen)