import random
import pygame

from world import World
from player import Player
from config import Config


pygame.init()


class PyDew:

    def __init__(self):
        self.version = "0.0.1.3"
        print("Hello PyDew "+str(self.version))
        self.config = Config()        
        self.final_screen = pygame.display.set_mode((self.config.screen_width, 
                                               self.config.screen_height),
                                               pygame.HWSURFACE|pygame.DOUBLEBUF)
        self.screen = pygame.Surface((self.config.screen_width/self.config.screen_scaling, 
                                               self.config.screen_height/self.config.screen_scaling),
                                               pygame.HWSURFACE|pygame.DOUBLEBUF).convert_alpha()
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("PyDew "+str(self.version))
        
        self.world = World(self)
        self.player = Player(self)
        
        self.run = False
        
    #do some more start stuff - like a main menu
    def start(self):
      self.run = True
      self.game_loop()
        
    #The game loop
    def game_loop(self):
        while self.run:
            self.check_input()
            self.update()
            self.render()
            self.clock.tick(60)
        pygame.quit()
    
    #Check/Dispatch user input
    def check_input(self):
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                self.run = False
        keys = pygame.key.get_pressed()
        self.player.handle_input(keys)
        
    #Update game state
    def update(self):
        self.player.tick()
        
    #Draw some stuff
    def render(self):
        self.world.render(self.screen)
        self.player.render(self.screen)
        
        scaled_screen = pygame.transform.scale(self.screen,self.final_screen.get_rect().size)
        self.final_screen.blit(scaled_screen,(0,0))
        pygame.display.flip()


#Go!
if __name__ == "__main__":
    game = PyDew()
    game.start()
    