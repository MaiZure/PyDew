import pygame

class Player:
    def __init__(self, game):
        print("Initializaing Player")
        self.game = game

        self.sprite = game.sprite.get_spritesheet_tiles("emily")
        self.x = 34*16 #self.game.config.screen_width/2
        self.y = 24*16 #self.game.config.screen_height/2
        self.dir = 0
        self.frametimer = 0
        self.frame = 0
        self.walking = False
        self.m_up = self.m_down = self.m_right = self.m_left = False
        self.map_width = 0
        self.map_height = 0

    def handle_input(self, input):
        if input[pygame.K_s]: self.m_down = True
        if input[pygame.K_d]: self.m_right = True
        if input[pygame.K_w]: self.m_up = True
        if input[pygame.K_a]: self.m_left = True
        self.walking = input[pygame.K_LSHIFT]
        
    def tick(self):
        self.frametimer += 1 + self.walking
        self.frame = int((self.frametimer/20)%4)
        
        if self.m_down: self.move_down()
        if self.m_right: self.move_right()
        if self.m_up: self.move_up()
        if self.m_left: self.move_left()
        
    def set_map_width(self,w) -> None:
        assert w >= 0 <= 120
        self.map_width = w
    
    def set_map_height(self,h) -> None:
        assert h >= 0 <= 120
        self.map_height = h
        
    def render(self, screen):
        top_left_x = min(max(self.game.player.x-screen.get_width()/2,0),self.map_width*16-screen.get_width())
        top_left_y = min(max(self.game.player.y-screen.get_height()/2,0),self.map_height*16-screen.get_height())
        screen.blit(self.sprite[self.dir*4+self.frame], (self.x-top_left_x,self.y-16-top_left_y), (0,0,16,32))
        
    def move_down(self):
        self.dir = 0;
        self.y += 2-self.walking;
        self.m_down = False
        
    def move_right(self):
        self.dir = 1;
        self.x += 2-self.walking;
        self.m_right = False
        
    def move_up(self):
        self.dir = 2;
        self.y -= 2-self.walking;
        self.m_up = False
        
    def move_left(self):
        self.dir = 3;
        self.x -= 2-self.walking;
        self.m_left = False