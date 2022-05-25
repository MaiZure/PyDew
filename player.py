import pygame

class Player:
    def __init__(self, game):
        print("Initializaing Player")
        self.game = game
        self.spritesheet = pygame.image.load(".\\Tiles\\Emily.png").convert_alpha()
        self.x = 32*16 #self.game.config.screen_width/2
        self.y = 17*16 #self.game.config.screen_height/2
        self.dir = 0
        self.sprite = []
        self.frametimer = 0
        self.frame = 0
        self.running = False
        self.m_up = self.m_down = self.m_right = self.m_left = False
        
        for j in range(4):
            for i in range(4):
                rect = pygame.Rect(i*16, j*32, 16, 32)
                self.sprite.append(pygame.Surface(rect.size, pygame.SRCALPHA).convert_alpha())
                self.sprite[j*4+i].blit(self.spritesheet, (0, 0), rect)
    

    def handle_input(self, input):
        if input[pygame.K_s]: self.m_down = True
        if input[pygame.K_d]: self.m_right = True
        if input[pygame.K_w]: self.m_up = True
        if input[pygame.K_a]: self.m_left = True
        self.running = input[pygame.K_LSHIFT]
        
    def tick(self):
        self.frametimer += 1 + self.running
        self.frame = int((self.frametimer/20)%4)
        
        if self.m_down: self.move_down()
        if self.m_right: self.move_right()
        if self.m_up: self.move_up()
        if self.m_left: self.move_left()
        
    def render(self, screen):
        top_left_x = min(max(self.game.player.x-screen.get_width()/2,0),75*16-screen.get_width())
        top_left_y = min(max(self.game.player.y-screen.get_height()/2,0),50*16-screen.get_height())
        screen.blit(self.sprite[self.dir*4+self.frame], (self.x-top_left_x,self.y-16-top_left_y), (0,0,16,32))
        
    def move_down(self):
        self.dir = 0;
        self.y += 1+self.running;
        self.m_down = False
        
    def move_right(self):
        self.dir = 1;
        self.x += 1+self.running;
        self.m_right = False
        
    def move_up(self):
        self.dir = 2;
        self.y -= 1+self.running;
        self.m_up = False
        
    def move_left(self):
        self.dir = 3;
        self.x -= 1+self.running;
        self.m_left = False