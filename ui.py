import random
import pygame
from ui_clock import Clock
from ui_statusbars import StatusBars

class UI:

    def __init__(self, game):
        print("Initializing UI")
        self.game = game

        self.ui_elements = []
        self.ui_elements.append(Clock(game,self))
        self.ui_elements.append(StatusBars(game,self))
    
    def tick(self):
        pass
    
    def render(self, screen):
        for element in self.ui_elements:
            element.render(screen)