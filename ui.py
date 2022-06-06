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
        
    def tick(self):
        pass
    
    def ui_render(self, screen):
        for element in self.ui_elements:
            element.render(screen)
            
    def menu_render(self, screen):
        for element in self.menu_elements:
            element.render(screen)