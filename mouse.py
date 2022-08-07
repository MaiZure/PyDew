import random
import pygame

class MouseHandler:

    def __init__(self, game, ui):
        print("Initializing MouseHander")
        self.game = game
        self.ui = ui
        
    def init_second_stage(self):
        pass
        
    def handle_input(self, event):
        pos = pygame.mouse.get_pos()
        print("Mouse click at "+str(pos))
        
        if self.ui.player_menu_enabled:
            self.ui.player_menu.handle_input(event)
            return

        if event.button == 1:
            if self.ui.ibar.ibar_clickrect.collidepoint(pos):
                self.ui.ibar.handle_mouse(event)
            self.game.player.handle_mouse(event)
        if event.button == 3:
            self.game.player.handle_mouse(event)        
        if event.button == 4 or event.button == 5:  # Mouse wheel up/down
            self.ui.ibar.handle_mouse(event)
        
        