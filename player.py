import pygame, random

class Player:
    def __init__(self, game):
        print("Initializing Player")
        self.game = game
        
        self.name = random.choice(list(game.sprite.character_sheet.keys()))
        self.sprite = game.sprite.get_tiles("farmer_base")
        self.hair = game.sprite.get_tiles("hairstyles")
        self.shirt = game.sprite.get_tiles("shirts")
        self.pants = game.sprite.get_tiles("pants")
        #self.pants = 0 ## TODO - Get first set of pants 192,672 of whole sheet
        self.hair_num = 3#random.randint(0,7)
        self.shirt_num = 8
        self.pants_num = 0
        self.gx = 78  #34
        self.gy = 16  #24
        self.x = self.gx*16 
        self.y = self.gy*16 
        
        self.dir = 0 # 0 = down, 1 = right, 2 = up, 3 = left
        self.frametimer = 0
        self.frame = 0
        self.walking = False
        self.m_up = self.m_down = self.m_right = self.m_left = False
        self.map_width = 0
        self.map_height = 0
        self.moving = False
        
        self.frame_sequence = [18,56,56,23,18,57,57,41]
        self.hair_yoff = [0,-1,-1,-1,0,-1,-1,-1]
        self.shirt_yoff = [0,-1,-1,-1,0,-1,-1,-1]

    def handle_input(self, input):
        if input[pygame.K_s]: self.m_down = True
        if input[pygame.K_d]: self.m_right = True
        if input[pygame.K_w]: self.m_up = True
        if input[pygame.K_a]: self.m_left = True
        if input[pygame.K_x]: self.do_action()
        if input[pygame.K_c]: self.use_item()
        if input[pygame.K_l]: print("Player at (" +str(self.gx)+","+str(self.gy) + ")")
        if input[pygame.K_h]: self.hair_num = random.randint(0,7)
        self.walking = input[pygame.K_LSHIFT]
        
    def tick(self):
        if self.moving:
            self.frametimer += 2 - self.walking
            self.frame = int((self.frametimer/20)%8)
        else:
            self.frame = 0
            self.frametimer = 0
            
        self.gx = int((self.x+8)/16)
        self.gy = int((self.y+8)/16)
        
        if (self.gx, self.gy) in self.game.world.warp_points:
            self.game.world.warp_player(self.game.world.warp_points[(self.gx, self.gy)])
            
        
        if self.m_down: self.move_down()
        if self.m_right: self.move_right()
        if self.m_up: self.move_up()
        if self.m_left: self.move_left()
        
    def set_gx(self, gx):
        self.gx = gx
        self.x = self.gx*16 
        
    def set_gy(self, gy):
        self.gy = gy
        self.y = self.gy*16
        
    def do_action(self):
        target_x = self.gx
        target_y = self.gy
        
        if self.dir == 0: target_y += 1
        if self.dir == 1: target_x += 1
        if self.dir == 2: target_y -= 1
        if self.dir == 3: target_x -= 1
        
        self.game.world.do_action((target_x, target_y))
    
    def use_item(self):
        pass
        
    def render(self, screen):
        top_left_x = self.game.world.top_left_x
        top_left_y = self.game.world.top_left_y
        #body
        screen.blit(self.sprite[self.frame_sequence[self.frame]], (self.x-top_left_x,self.y-16-top_left_y), (0,0,16,32))
        
        #pants
        screen.blit(self.pants[self.frame_sequence[self.frame]], (self.x-top_left_x,self.y-top_left_y), (0,0,16,32))
        
        #shirt
        screen.blit(self.shirt[self.shirt_num], (self.x-top_left_x+4,self.y-top_left_y-1-self.hair_yoff[self.frame]), (0,8,8,8))
        #arms
        screen.blit(self.sprite[self.frame_sequence[self.frame]+6], (self.x-top_left_x,self.y-16-top_left_y), (0,0,16,32))
        
        #hair
        screen.blit(self.hair[self.hair_num+8], (self.x-top_left_x,self.y-15-top_left_y-self.hair_yoff[self.frame]), (0,0,16,32))

    def move_down(self):
        self.moving = True
        self.dir = 0;
        gx = int((self.x+8)/16)
        gy = int((self.y+16)/16)
        if self.game.world.is_movable(gx,gy):
            self.y += 2-self.walking;
        self.m_down = False
        
    def move_right(self):
        self.moving = True
        self.dir = 1;
        gx = int((self.x+17)/16)
        gy = int((self.y+8)/16)
        if self.game.world.is_movable(gx,gy):
            self.x += 2-self.walking;
        self.m_right = False
        
    def move_up(self):
        self.moving = True
        self.dir = 2;
        gx = int((self.x+8)/16)
        gy = int((self.y+4)/16)
        if self.game.world.is_movable(gx,gy):
            self.y -= 2-self.walking;
        self.m_up = False
        
    def move_left(self):
        self.moving = True
        self.dir = 3;
        gx = int((self.x-1)/16)
        gy = int((self.y+8)/16)
        if self.game.world.is_movable(gx,gy):
            self.x -= 2-self.walking;
        self.m_left = False