import pygame, random

class Player:
    def __init__(self, game):
        print("Initializing Player")
        self.game = game
        
        self.name = random.choice(list(game.sprite.character_sheet.keys()))
        self.sprite = game.sprite.get_tiles("farmer_base")
        self.hair = game.sprite.get_tiles("hairstyles")
        self.shirt = game.sprite.get_tiles("shirts")
        self.pants_sheet = game.sprite.get_tiles("pants")
        self.hair_num = 3
        self.shirt_num = 8
        self.pants_num = 0
        self.skin_num = 23
        
        self.generate_pants()
        self.hair_color = (192,32,32)
        self.pants_color = (0,0,224)
        self.skin = self.game.sprite.sheet["skinColors"][0]
        self.skin_color = self.skin.get_at((2,self.skin_num))[:3]
        
        self.pants = game.sprite.colorize_tiles(self.pants,self.pants_color)
        self.hair = game.sprite.colorize_tiles(self.hair, self.hair_color)
        self.sprite = game.sprite.colorize_tiles(self.sprite, self.skin_color)
        
        
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
        
        self.run_sequence_RL = (18,56,56,23,18,57,57,41)
        self.run_sequence_D = (0,1,54,1,0,2,55,2)
        self.run_sequence_U = (36,37,58,37,36,38,59,38)
        self.frame_sequence = self.run_sequence_RL
        self.hair_yoff_rl = (0,-1,-1,-1,0,-1,-1,-1)
        self.hair_yoff_ud = (0,-1,-2,-1,0,-1,-2,-1)
        self.shirt_yoff = (0,-1,-1,-1,0,-1,-1,-1)
        
        self.hair_yoff = self.hair_yoff_rl
        self.hair_frame_off = 0
    
    # Because pants are weird....
    def generate_pants(self):
        self.pants = pygame.Surface((288,672),pygame.SRCALPHA) ## TODO - Get first set of pants 192,672 of whole sheet
        self.pants.blit(self.pants_sheet[self.pants_num], (0,0),(0,0,192,672))
        self.game.sprite.player_sheet["player_pants"] = (self.pants, 16,32)
        self.game.sprite.sheet["player_pants"] = self.game.sprite.player_sheet["player_pants"]
        self.game.sprite.tiles["player_pants"] = self.game.sprite.get_spritesheet_tiles("player_pants")
        self.pants = self.game.sprite.get_tiles("player_pants")

    def handle_input(self, input):
        if input[pygame.K_s]: self.m_down = True
        if input[pygame.K_d]: self.m_right = True
        if input[pygame.K_w]: self.m_up = True
        if input[pygame.K_a]: self.m_left = True
        if input[pygame.K_x]: self.do_action()
        if input[pygame.K_c]: self.use_item()
        if input[pygame.K_l]: print("Player at (" +str(self.gx)+","+str(self.gy) + ")")
        if input[pygame.K_h]: self.randomize_character()
        self.walking = input[pygame.K_LSHIFT]
        
    def randomize_character(self):
        self.hair_num = random.randint(0,55)
        self.shirt_num = random.randint(0,15)
        self.pants_num = random.randint(0,15)
        self.skin_num = random.randint(0,23)
        self.generate_pants()
        self.game.sprite.change_skin(self.skin_num)
        self.sprite = self.game.sprite.get_tiles("farmer_base")
        self.hair_color = random.choice(((192,32,32),(232,232,32),(32,32,32)))
        self.hair = self.game.sprite.get_tiles("hairstyles")
        self.hair = self.game.sprite.colorize_tiles(self.hair, self.hair_color)
        
        
    def tick(self):
        if self.moving:
            self.frametimer += 2 - self.walking
            self.frame = int((self.frametimer/10)%8)
            self.moving = False
        else:
            self.frame = 0
            self.frametimer = 0
            
        self.gx = int((self.x+8)/16)
        self.gy = int((self.y+8)/16)
        
        if (self.gx, self.gy) in self.game.world.edge_warp_points:
            self.game.world.warp_player(self.game.world.edge_warp_points[(self.gx, self.gy)])
            
        
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
        
    def get_shirt_dir(self, dir):
        if dir == 0: return (0,0,8,8)
        if dir == 1: return (0,8,8,8)
        if dir == 2: return (0,24,8,8)
        if dir == 3: return (0,16,8,8)
        
    def render(self, screen):
        top_left_x = self.game.world.top_left_x
        top_left_y = self.game.world.top_left_y
        x = self.x
        y = self.y
        
        frame = self.frame_sequence[self.frame]
        
        body_pos = (self.x-top_left_x,self.y-16-top_left_y)
        shirt_pos = (self.x-top_left_x+4,self.y-top_left_y-1-self.hair_yoff[self.frame])
        hair_pos = (self.x-top_left_x,self.y-15-top_left_y-self.hair_yoff[self.frame])
        arms_pos = (self.x-top_left_x,self.y-16-top_left_y)
        pants_pos = (self.x-top_left_x,self.y-16-top_left_y)
        
        body_sprite = self.sprite[frame]
        arms_sprite = self.sprite[frame+6]
        shirt_sprite = self.shirt[self.shirt_num]
        pants_sprite = self.pants[frame]
        hair_frame = (self.hair_num % 8) + int(self.hair_num/8)*24
        hair_sprite = self.hair[hair_frame+self.hair_frame_off]
        
        if self.dir == 3:
            body_sprite = pygame.transform.flip(body_sprite,True,False)
            hair_sprite = pygame.transform.flip(hair_sprite,True,False)
            arms_sprite = pygame.transform.flip(arms_sprite,True,False)

        screen.blit(body_sprite, body_pos, (0,0,16,32))
        screen.blit(pants_sprite, pants_pos, (0,0,16,32))
        screen.blit(shirt_sprite, shirt_pos, self.get_shirt_dir(self.dir))
        screen.blit(arms_sprite, arms_pos, (0,0,16,32))
        screen.blit(hair_sprite, hair_pos, (0,0,16,32))

    def move_down(self):
        self.moving = True
        self.dir = 0; self.frame_sequence = self.run_sequence_D; self.hair_frame_off = 0; self.hair_yoff = self.hair_yoff_ud
        gx = int((self.x+8)/16)
        gy = int((self.y+16)/16)
        if self.game.world.is_movable(gx,gy):
            self.y += 2-self.walking;
        self.m_down = False
        
    def move_right(self):
        self.moving = True
        self.dir = 1; self.frame_sequence = self.run_sequence_RL; self.hair_frame_off = 8; self.hair_yoff = self.hair_yoff_rl
        gx = int((self.x+17)/16)
        gy = int((self.y+8)/16)
        if self.game.world.is_movable(gx,gy):
            self.x += 2-self.walking;
        self.m_right = False
        
    def move_up(self):
        self.moving = True
        self.dir = 2; self.frame_sequence = self.run_sequence_U; self.hair_frame_off = 16; self.hair_yoff = self.hair_yoff_ud
        gx = int((self.x+8)/16)
        gy = int((self.y+4)/16)
        if self.game.world.is_movable(gx,gy):
            self.y -= 2-self.walking;
        self.m_up = False
        
    def move_left(self):
        self.moving = True
        self.dir = 3; self.frame_sequence = self.run_sequence_RL; self.hair_frame_off = 8; self.hair_yoff = self.hair_yoff_rl
        gx = int((self.x-1)/16)
        gy = int((self.y+8)/16)
        if self.game.world.is_movable(gx,gy):
            self.x -= 2-self.walking;
        self.m_left = False