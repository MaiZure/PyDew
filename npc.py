import pygame, random

class NPC:
    def __init__(self, game):
        print("Initializing NPC")
        self.game = game
        
        self.name = "emily"
        self.sprite = game.sprite.get_tiles(self.name)
        self.gx = 64  #34
        self.gy = 13  #24
        self.x = self.gx*16 
        self.y = self.gy*16 
        
        self.dir = 0 # 0 = down, 1 = right, 2 = up, 3 = left
        self.frametimer = 0
        self.frame = 0
        self.walking = True
        self.m_up = self.m_down = self.m_right = self.m_left = False
        self.map_width = 0
        self.map_height = 0

    def handle_input(self, input):
        pass
        
    def tick(self):
        self.frametimer += 2 - self.walking
        self.frame = int((self.frametimer/20)%4)
        self.gx = int((self.x+8)/16)
        self.gy = int((self.y+8)/16)
        
        if (self.gx, self.gy) in self.game.world.edge_warp_points:
            self.game.world.warp_player(self.game.world.edge_warp_points[(self.gx, self.gy)])
                  
        if self.m_down: self.move_down()
        if self.m_right: self.move_right()
        if self.m_up: self.move_up()
        if self.m_left: self.move_left()     
        
    def render(self, screen):
        top_left_x = self.game.world.top_left_x
        top_left_y = self.game.world.top_left_y
        screen.blit(self.sprite[self.dir*4+self.frame], (self.x-top_left_x,self.y-16-top_left_y), (0,0,16,32))
        
    def move_down(self):
        self.dir = 0;
        gx = int((self.x+8)/16)
        gy = int((self.y+16)/16)
        if self.game.world.is_movable(gx,gy):
            self.y += 2-self.walking;
        self.m_down = False
        
    def move_right(self):
        self.dir = 1;
        gx = int((self.x+17)/16)
        gy = int((self.y+8)/16)
        if self.game.world.is_movable(gx,gy):
            self.x += 2-self.walking;
        self.m_right = False
        
    def move_up(self):
        self.dir = 2;
        gx = int((self.x+8)/16)
        gy = int((self.y+4)/16)
        if self.game.world.is_movable(gx,gy):
            self.y -= 2-self.walking;
        self.m_up = False
        
    def move_left(self):
        self.dir = 3;
        gx = int((self.x-1)/16)
        gy = int((self.y+8)/16)
        if self.game.world.is_movable(gx,gy):
            self.x -= 2-self.walking;
        self.m_left = False