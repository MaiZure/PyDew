import pygame, random
from item import *

class Player:
    def __init__(self, game):
        print("Initializing Player")
        self.game = game
        
        
        self.hair_num = 3
        self.shirt_num = 8
        self.pants_num = 0
        self.skin_num = 23
        self.inventory = [None] * 36
        self.inventory_limit = 24
        self.hair_color = (192,32,32)
        self.pants_color = (0,0,224)
        self.action_locked = False
        self.player_sequence = ()
        self.action_sequence = ()
               
        self.gx = 72 #64  #78
        self.gy = 17 #67  #16
        self.x = self.gx*16 
        self.y = self.gy*16 
        
        self.dir = 0 # 0 = down, 1 = right, 2 = up, 3 = left
        self.frametimer = 0
        self.frame = 0
        self.actiontimer = 0
        self.action_frame = 0
        self.walking = False
        self.m_up = self.m_down = self.m_right = self.m_left = False
        self.map_width = 0
        self.map_height = 0
        self.moving = False
        self.max_hp = self.game.save.player_max_hp
        self.hp = self.max_hp
        self.ep = 270
        self.max_ep = 270
        
        self.run_sequence = ((0,1,54,1,0,2,55,2),        #D
                             (18,56,56,23,18,57,57,41),  #R
                             (36,37,58,37,36,38,59,38),  #U
                             (18,56,56,23,18,57,57,41))  #L
        self.item_sequence = ()
        self.scythe_sequence_D = (72,73,74,75,76,77,78)
        self.scythe_sequence_U = (108,109,110,111,112,113) # swing +12
        self.axe_sequence_D = (198,199,200,201,201,202)
        self.axe_sequence_U = (108,109,110,182,182,183)
        self.frame_sequence = self.run_sequence[self.dir]
        self.hair_yoff_base = ((0,-1,-2,-1,0,-1,-2,-1),
                          (0,-1,-1,-1,0,-1,-1,-1),
                          (0,-1,-2,-1,0,-1,-2,-1),
                          (0,-1,-1,-1,0,-1,-1,-1))
        self.hair_yoff = self.hair_yoff_base[self.dir]
        self.hair_frame_off = 0
        self.scaled_hair = [None]*4
        self.scaled_shirt = [None]*4
        
    def init_second_stage(self):
        self.name = random.choice(list(self.game.sprite.character_sheet.keys()))
        self.sprite = self.game.sprite.get_tiles("farmer_base")
        self.hair = self.game.sprite.get_tiles("hairstyles")
        self.shirt = self.game.sprite.get_tiles("shirts")
        self.pants_sheet = self.game.sprite.get_tiles("pants")
        self.skin = self.game.sprite.sheet["skinColors"][0]
        self.skin_color = self.skin.get_at((2,self.skin_num))[:3]
        self.generate_pants() ## here?
        self.pants = self.game.sprite.colorize_tiles(self.pants, self.pants_color)
        self.hair = self.game.sprite.colorize_tiles(self.hair, self.hair_color)
        self.sprite = self.game.sprite.colorize_tiles(self.sprite, self.skin_color)
        
        # Cache scaled hair/shirt to draw over up facing tools/weapons
        hair_frame = (self.hair_num % 8) + int(self.hair_num/8)*24
        for i in range(4):
            if i == 0: hair_dir_off = 0
            if i == 1: hair_dir_off = 8
            if i == 2: hair_dir_off = 16
            if i == 3: hair_dir_off = 8
            hair_sprite = self.hair[hair_frame+self.hair_frame_off+hair_dir_off]
            self.scaled_hair[i] = self.game.sprite.rescale_sprite(hair_sprite, self.game.config.screen_scaling)
            if i == 3:
                self.scaled_hair[i] = pygame.transform.flip(self.scaled_hair[i],True,False)
            
            shirt_sprite = pygame.Surface((8,8),pygame.SRCALPHA)
            shirt_sprite.blit(self.shirt[self.shirt_num], (0,0),self.get_shirt_dir(i))
            self.scaled_shirt[i] = self.game.sprite.rescale_sprite(shirt_sprite, self.game.config.screen_scaling)
            # TODO - i == 3 needs to be reversed
    
        self.inventory[0] = Tool(self.game, "axe")
        self.inventory[1] = Tool(self.game, "pickaxe")
        self.inventory[2] = Tool(self.game, "hoe")
        self.inventory[3] = Weapon(self.game, "scythe")
        self.inventory[4] = Tool(self.game, "wateringcan")
        self.inventory[5] = Weapon(self.game)
        
        self.inventory[7] = (Item(self.game)).init_item()
        self.inventory[7].count = 3
        self.inventory[8] = (Item(self.game)).init_item()
        self.inventory[8].count = 3
        self.inventory[9] = (Item(self.game)).init_item()
        self.inventory[9].count = 3
        
    def generate_pants(self):
        self.pants = pygame.Surface((288,672),pygame.SRCALPHA) ## TODO - Get first set of pants 192,672 of whole sheet
        self.pants.blit(self.pants_sheet[self.pants_num], (0,0),(0,0,192,672))
        self.game.sprite.player_sheet["player_pants"] = (self.pants, 16,32)
        self.game.sprite.sheet["player_pants"] = self.game.sprite.player_sheet["player_pants"]
        self.game.sprite.tiles["player_pants"] = self.game.sprite.get_spritesheet_tiles("player_pants")
        self.pants = self.game.sprite.get_tiles("player_pants")

    def handle_input(self, input):
        if self.action_locked: return
        if input[pygame.K_s]: self.m_down = True
        if input[pygame.K_d]: self.m_right = True
        if input[pygame.K_w]: self.m_up = True
        if input[pygame.K_a]: self.m_left = True
        if input[pygame.K_x]: self.do_action()
        if input[pygame.K_c]: self.use_item()
        if input[pygame.K_l]: print("Player at (" +str(self.gx)+","+str(self.gy) + ")")
        if input[pygame.K_h]: self.randomize_character()
        if input[pygame.K_1]: self.game.ui.ibar.change_selection(0)
        if input[pygame.K_2]: self.game.ui.ibar.change_selection(1)
        if input[pygame.K_3]: self.game.ui.ibar.change_selection(2)
        if input[pygame.K_4]: self.game.ui.ibar.change_selection(3)
        if input[pygame.K_5]: self.game.ui.ibar.change_selection(4)
        if input[pygame.K_6]: self.game.ui.ibar.change_selection(5)
        if input[pygame.K_7]: self.game.ui.ibar.change_selection(6)
        if input[pygame.K_8]: self.game.ui.ibar.change_selection(7)
        if input[pygame.K_9]: self.game.ui.ibar.change_selection(8)
        if input[pygame.K_0]: self.game.ui.ibar.change_selection(9)
        if input[pygame.K_MINUS]: self.game.ui.ibar.change_selection(10)
        if input[pygame.K_EQUALS]: self.game.ui.ibar.change_selection(11)
        self.walking = input[pygame.K_LSHIFT]
        
    def handle_mouse(self, event):
        if event.button == 1: self.use_item()
        if event.button == 3: self.do_action()
        
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
        self.hitrect = pygame.Rect(self.x-8,self.y-16,16,32)
        
        if (self.gx, self.gy) in self.game.world.edge_warp_points:
            self.game.world.warp_player(self.game.world.edge_warp_points[(self.gx, self.gy)])

        if self.action_locked:
            self.moving = False
            item = self.current_item
            if not self.player_sequence: # Not executing an action
                self.action_locked = False
                self.hair_yoff = self.hair_yoff_base[self.dir]
                self.frame_sequence = self.run_sequence[self.dir]
                self.item_sequence = ()
                self.action_sequence = ()
            else:
                # Tool usage actions
                self.frame_sequence = self.player_sequence
                self.actiontimer += 2
                self.frame = int((self.actiontimer/6)%8) # /6
                
                if self.frame >= len(self.player_sequence): # End of sequence check
                    self.frame = 0
                    self.actiontimer = 0  # Fix for energy drain bug
                    self.action_locked = False
                    self.frame_sequence = self.run_sequence[self.dir]
                    self.hair_yoff = self.hair_yoff_base[self.dir]
                    self.item_sequence = ()
                    self.action_sequence = []
                else:
                    # Still in a sequence, so check for an action
                    if self.action_sequence[self.frame]:  # Check for world interaction (chop,hit,etc)
                        current_map = self.game.world.current_map
                        action_list = self.action_sequence[self.frame]
                        print(action_list)
                        for action in action_list:
                            print(action)
                            action_item = action[0]
                            gx = action[1][0]+self.gx
                            gy = action[1][1]+self.gy
                            action_mxy = (current_map,(gx,gy))
                            #print("Use " + str(action[0]) + " at " + str(action_mxy))
                            if action_mxy in self.game.world.objects:
                                object = self.game.world.objects[action_mxy]
                                if action_item in object.action_list:
                                    object.hp -= (item.quality+1)*30
                                    if object.hp < 1: # Should consider queueing an item event
                                        object.destroy()
                            if action_item == "hoe":
                                map = self.game.world.current_map
                                tile = self.game.world.map_tiles[map][(gx,gy)]
                                tile.dig_tile()
                            if action_item == "watering":
                                map = self.game.world.current_map
                                tile = self.game.world.map_tiles[map][(gx,gy)]
                                if tile.water:
                                    self.current_item.water_level = 40
                                elif self.current_item.water_level > 0:
                                    tile.water_tile()
                                    self.current_item.water_level -= 1
                            self.action_sequence[self.frame] = None # Overwrite after first check
        else:
            self.actiontimer = 0
            self.action_frame = 0
            
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
        
    def get_front_tile(self):
        target_x = self.gx
        target_y = self.gy
        
        if self.dir == 0: target_y += 1
        if self.dir == 1: target_x += 1
        if self.dir == 2: target_y -= 1
        if self.dir == 3: target_x -= 1
        
        return (target_x, target_y)
        
    def do_action(self):
        target = self.get_front_tile()     
        self.game.world.do_action(target)
    
    def use_item(self):
        item = self.current_item
        if not item: return

        if item.category_str == "Sword" or item.category_str == "Tool":        
            self.action_locked = True
            self.player_sequence = item.player_sequence[self.dir]
            self.item_sequence = item.item_sequence
            self.action_sequence = list(item.action_sequence[self.dir])
            self.hair_yoff = item.hair_yoff[self.dir]
            self.ep -= item.ecost
            
        if item.category_str == "Seed":
            seed_index = item.inv_frame
            target = self.get_front_tile()
            tile = self.game.world.map_tiles[self.game.world.current_map][target]
            if tile.dug and not tile.crop and not tile.object:
                tile.plant_crop(seed_index)
                item.count -= 1
                if item.count < 1:
                    self.inventory[self.game.ui.ibar.selection] = None
                self.game.ui.ibar.force_redraw()
        
    @property
    def current_item(self):
        return self.inventory[self.game.ui.ibar.selection]
        
    def has_inventory_space(self):
        return None in self.inventory[:self.inventory_limit]
        
    def find_free_inventory_slot(self):
        inv_row = self.game.ui.ibar.ibar_row
        # check from active row 
        for slot in range(inv_row*12, self.inventory_limit):
            if self.inventory[slot] == None:
                return slot
        # Check for rows behind active row
        if inv_row > 0:
            for slot in range(0, inv_row*12):
                if self.inventory[slot] == None:
                    return slot
        
        # Some empty row should have been return (else has_inventory_space() wasn't used)
        return None
    
    def find_inventory_item_slot(self, item):
        for slot in range(0, self.inventory_limit):
            if not self.inventory[slot]: continue
            if self.inventory[slot].name == item.name:
                if self.inventory[slot].count < 999:
                    return slot
        return None
    
    def pickup_item(self, item): 
        if not item.stackable:
            if not self.has_inventory_space():
                return
            slot = self.find_free_inventory_slot()
            item.remove_from_world()
            self.inventory[slot] = item
        else: # Item is stackable
            slot = self.find_inventory_item_slot(item)
            if type(slot) is int:
                self.inventory[slot].count += item.count
            else:
                if not self.has_inventory_space():
                    return
                slot = self.find_free_inventory_slot()
                self.inventory[slot] = item
            item.remove_from_world()
        self.game.ui.ibar.redraw_inventory = True
        
    def can_pickup(self, item) -> bool:
        if not item.stackable:
            if not self.has_inventory_space():
                return False
            else:
                return True
        else: # Item is stackable
            slot = self.find_inventory_item_slot(item)
            if type(slot) is int:
                return True
            else:
                if not self.has_inventory_space():
                    return False
                return True
    

    def get_shirt_dir(self, dir):
        if dir == 0: return (0,0,8,8)
        if dir == 1: return (0,8,8,8)
        if dir == 2: return (0,24,8,8)
        if dir == 3: return (0,16,8,8)
        
    def cycle_inventory(self):
        if self.inventory_limit == 12: return
        if self.game.ui.player_menu_enabled: return
        for i in range(12):
            Item = self.inventory.pop(0)
            self.inventory.insert(self.inventory_limit-1, Item)
        self.game.ui.ibar.generate_ibar()
        
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
        shirt_sprite = self.shirt[self.shirt_num]
        pants_sprite = self.pants[frame]
        hair_frame = (self.hair_num % 8) + int(self.hair_num/8)*24
        hair_sprite = self.hair[hair_frame+self.hair_frame_off]
        arms_sprite = self.sprite[frame+6] 
        if self.action_locked:
            if self.current_item.category_str == "Sword":
                arms_sprite = self.sprite[frame+12]
            if self.current_item.category_str == "Tool" and self.current_item.arm_frame_off:
                arms_sprite = self.sprite[frame+self.current_item.arm_frame_off[self.dir][self.frame]]
        
        if self.dir == 3:
            body_sprite = pygame.transform.flip(body_sprite,True,False)
            hair_sprite = pygame.transform.flip(hair_sprite,True,False)
            arms_sprite = pygame.transform.flip(arms_sprite,True,False)

        screen.blit(body_sprite, body_pos, (0,0,16,32))
        screen.blit(pants_sprite, pants_pos, (0,0,16,32))
        screen.blit(shirt_sprite, shirt_pos, self.get_shirt_dir(self.dir))        
        screen.blit(hair_sprite, hair_pos, (0,0,16,32))
        screen.blit(arms_sprite, arms_pos, (0,0,16,32))
                
    def render_scaled(self, screen):
        if not self.item_sequence: return
        item = self.current_item
        if not item: return
        
        top_left_x = self.game.world.top_left_x
        top_left_y = self.game.world.top_left_y
        x = self.x
        y = self.y
        scale = self.game.config.screen_scaling
        frame = self.frame
        
        item_x = (x - top_left_x + self.current_item.item_xoff[self.dir][frame]) * scale
        item_y = (y - top_left_y + self.current_item.item_yoff[self.dir][frame] - 32) * scale            
        item_sprite = self.current_item.sprite_sequence[self.dir][frame]         
        
        screen.blit(item_sprite, (item_x, item_y))
        
        # Draw hair over sprite
        if self.dir == 2 or ((self.dir == 1 or self.dir == 3) and self.current_item.category_str == "Sword"):
            shirt_pos = ((self.x-top_left_x+4)*scale,(self.y-top_left_y-1-self.hair_yoff[self.frame])*scale)
            hair_pos = ((self.x-top_left_x)*scale,(self.y-15-top_left_y-self.hair_yoff[self.frame])*scale)
            
            screen.blit(self.scaled_hair[self.dir], hair_pos)
            if self.dir == 2:
                screen.blit(self.scaled_shirt[self.dir], shirt_pos)

    def move_down(self):
        self.moving = True
        self.dir = 0; 
        self.frame_sequence = self.run_sequence[self.dir];
        self.hair_yoff = self.hair_yoff_base[self.dir]
        self.hair_frame_off = 0; 
        gx = int((self.x+6)/16)
        gy = int((self.y+16)/16)
        if self.game.world.is_movable(gx,gy):
            self.y += 2-self.walking;
        self.m_down = False
        
    def move_right(self):
        self.moving = True
        self.dir = 1; 
        self.frame_sequence = self.run_sequence[self.dir];
        self.hair_yoff = self.hair_yoff_base[self.dir]        
        self.hair_frame_off = 8; 
        gy1 = int((self.y+8)/16)
        gy2 = int((self.y+15)/16)
        gx = int((self.x+15)/16)
        if self.game.world.is_movable(gx,gy1) and self.game.world.is_movable(gx,gy2) :
            self.x += 2-self.walking;
        self.m_right = False
        
    def move_up(self):
        self.moving = True
        self.dir = 2; 
        self.frame_sequence = self.run_sequence[self.dir];
        self.hair_yoff = self.hair_yoff_base[self.dir]
        self.hair_frame_off = 16; 
        gx = int((self.x+6)/16)
        gy = int((self.y+6)/16)
        if self.game.world.is_movable(gx,gy):
            self.y -= 2-self.walking;
        self.m_up = False
        
    def move_left(self):
        self.moving = True
        self.dir = 3; 
        self.frame_sequence = self.run_sequence[self.dir];
        self.hair_yoff = self.hair_yoff_base[self.dir]
        self.hair_frame_off = 8; 
        gy1 = int((self.y+8)/16)
        gy2 = int((self.y+15)/16)
        gx = int((self.x)/16)
        if self.game.world.is_movable(gx,gy1) and self.game.world.is_movable(gx,gy2) :
            self.x -= 2-self.walking;
        self.m_left = False