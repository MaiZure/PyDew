import random
import pygame

class Item:
    def __init__(self, game):
        self.game = game
        self.gx = None
        self.gy = None
        self.x = None
        self.y = None
        
        self.count = 1
        self.stackable = False
        self.player = self.game.player
        self.sprite = None
        
        self.name = ""
        self.category_str = ""
        self.desc = ""
        self.life_timer = 30
        self.quality = 0
      
        self.spritesheet = self.game.sprite.get_tiles("MenuTiles")

    def render(self, screen):
        if not self.x or not self.y:
            return
        if not self.game.world.is_visible(self.gx, self.gy):
            return
            
        top_left_x = self.game.world.top_left_x
        top_left_y = self.game.world.top_left_y
        screen.blit(self.sprite[self.spr_frame], (self.x-top_left_x,self.y-top_left_y), (0,0,16,16))
        
    def render_inv(self, screen, slot_num):
        if not self.sprite: return
        
        # Only tab_selected 0 and 4 should enter this function
        if self.game.ui.player_menu_enabled:
            menu = 0 if self.game.ui.player_menu.tab_selected == 0 else 1 
            slot_pos = self.game.ui.player_menu.slot_pos[menu][slot_num]
        else:
            top = self.game.ui.ibar.ibar_top # Bool - True if bar is at top. Used below
            slot_pos = self.game.ui.ibar.slot_pos[top][slot_num]
        sprite = self.sprite[self.inv_frame]
        scaled_item = pygame.transform.scale(sprite,(60,60))  # Get rid of this -- precompute scaled
        screen.blit(scaled_item, (slot_pos[0],slot_pos[1]))
        if self.count > 1:
            ui = self.game.ui
            digits = [int(x) for x in str(self.count)]
            digits.reverse()
            for i, d in enumerate(digits):
                screen.blit(ui.tiny_numbers, (slot_pos[0]+55-15*i,slot_pos[1]+53),ui.tiny_numbers_rect[d])
                
                
    def generate_hover(self, width=0, height=0):
        tl_corner = (0,0,16,16)
        tr_corner = (47,0,16,16)
        bl_corner = (0,47,16,16)
        br_corner = (47,47,16,16)
        left_bar = (0,16,12,32)
        right_bar = (47,16,12,32)
        top_bar = (16,0,32,16)
        bottom_bar = (12,44,32,16)
        
        cross_bar_y = 105
        if len(self.category_str) < 2:
            cross_bar_y = 72
        
        # Minimum hover size is 256x256
        self.game.font.set_font("spritefont1")
        w = self.game.font.get_line_width(self.name)
        width = max(256,w+36)
        
        width += 24*int((len(self.desc)/25))
        
        self.game.font.set_font("smallfont")
        lines = self.get_description_lines(self.desc,width-48)
        
        h = 0
        for line in lines:
            h += 24
            
        height = max(192, h+160)
        
        hover = pygame.Surface((width,height),pygame.SRCALPHA)
        
        hover.blit(pygame.transform.scale(self.spritesheet[9],(width-16,height-16)), (8,8))
        
        
        for i in range(16,width-16,32):
            hover.blit(self.spritesheet[16], (i,0), top_bar)
            hover.blit(self.spritesheet[16], (i,cross_bar_y), bottom_bar)
            hover.blit(self.spritesheet[16], (i,height-19), bottom_bar)
            
        for i in range(16,height-16,32):
            hover.blit(self.spritesheet[16], (0,i), left_bar)
            hover.blit(self.spritesheet[16], (width-16,i), right_bar)
            
        hover.blit(self.spritesheet[16], (0,0), tl_corner)
        hover.blit(self.spritesheet[16], (0,cross_bar_y+3), bl_corner)
        hover.blit(self.spritesheet[16], (0,height-16), bl_corner)
        
        hover.blit(self.spritesheet[16], (width-16,0), tr_corner)
        hover.blit(self.spritesheet[16], (width-16,cross_bar_y+3), br_corner)
        hover.blit(self.spritesheet[16], (width-16,height-16), br_corner)
        
        
            
        self.game.font.set_font("spritefont1")
        self.game.font.draw_text(self.name, hover, (18, 20), scaling_cut = 1, justify="left")
        
        self.game.font.set_font("smallfont")
        self.game.font.draw_text(self.category_str, hover, (18, 68), scaling_cut = 1, justify="left")
        
        for i in range(len(lines)):
            self.game.font.draw_text(lines[i], hover, (18, cross_bar_y+23+i*24), scaling_cut = 1, justify="left")
        
        
        return hover
                
    def render_mouse(self, screen):
        sprite = self.sprite[self.inv_frame]
        pos = pygame.mouse.get_pos()
        scaled_item = pygame.transform.scale(sprite,(60,60)) # Get rid of this -- precompute scaled
        screen.blit(scaled_item, pos)
                
    def create_at(self, x, y, count=1):
        self.x = x
        self.y = y
        self.gx = self.x/16
        self.gy = self.y/16
        self.game.world.items[self.game.world.current_map].append(self)
        
    def remove_from_world(self):
        current_map = self.game.world.current_map
        self.game.world.items[current_map].remove(self)
        self.x, self.y, self.gx, self.gy = None, None, None, None   
        
    def tick(self):
        if not self.game.world.is_visible(self.gx,self.gy):
            return
            
        if self.life_timer:
            self.life_timer -= 1
            return
        
        if self.distance_to_player() < 10:
            if self.player.can_pickup(self):
                self.move_towards_player()
                
        if self.game.player.hitrect.collidepoint(self.x,self.y):
            self.game.player.pickup_item(self)
                
    def distance_to_player(self) -> int:
        return ((self.gx-self.player.gx)**2 + (self.gy-self.player.gy)**2)

    def move_towards_player(self) -> None:
        if self.x < self.player.x:
            self.x += 3
        if self.x > self.player.x:
            self.x -= 3
        if self.y < self.player.y:
            self.y += 3
        if self.y > self.player.y:
            self.y -= 3
            
    def init_item(self, data=None):
        if not data:
            data = self.game.data.get_random_object()
            self.parse_item_data(data)
            self.sprite = self.game.sprite.get_tiles("springobjects")
            self.hover = self.generate_hover(256,192)
            return self

        self.inv_frame = int(data[0])
        self.spr_frame = self.inv_frame
        self.name = data[1]
        self.category_str = self.get_category_label(data[4])
        self.desc = data[6]
        self.sprite = self.game.sprite.get_tiles("springobjects")
        self.hover = self.generate_hover(256,192)
        return self
        
    def parse_item_data(self, data) -> None:
        datalist = data.split('/')
        self.inv_frame = int(datalist[0])
        self.name = datalist[1]
        self.category_str = self.get_category_label(datalist[4])
        self.desc = datalist[6]
        return datalist
        
    def get_category_label(self, data) -> str:
        split = data.split(" ")
        if len(split) < 2:
            if split[0] == "Arch": return "Artifact"
            if split[0] == "Ring": return "Ring"
            return ""
        
        cat_num = int(split[1])
        
        if cat_num == -2: return "Mineral"
        if cat_num == -4: return "Fish"
        if cat_num == -5: return "Animal Product"
        if cat_num == -6: return "Animal Product"
        if cat_num == -7: return "Cooking"
        if cat_num == -8: return "Crafting"
        if cat_num == -12: return "Mineral"
        if cat_num == -14: return "Animal Product"
        if cat_num == -15: return "Resource"
        if cat_num == -16: return "Resource"
        if cat_num == -18: return "Animal Product"
        if cat_num == -19: return "Fertilizer"
        if cat_num == -20: return "Trash"
        if cat_num == -21: return "Bait"
        if cat_num == -22: return "Fishing Tackle"
        if cat_num == -24: return "Decor"
        if cat_num == -25: return "Cooking"
        if cat_num == -26: return "Artisan Goods"
        if cat_num == -27: return "Artisan Goods"
        if cat_num == -28: return "Monster Loot"
        if cat_num == -74: return "Seed"
        if cat_num == -75: return "Vegetable"
        if cat_num == -79: return "Fruit"
        if cat_num == -80: return "Flower"
        if cat_num == -81: return "Forage"
        return ""
        
    def quality_name(self, quality):
        if quality == 0: return ""
        if quality == 1: return "Copper"
        if quality == 2: return "Steel"
        if quality == 3: return "Gold"
        if quality == 4: return "Iridium"
        
    def get_description_lines(self, desc, width_limit):
        lines = []
        start = 0
        current = 0
        last_space = 0
        current_line = ""
        while current < len(desc):
            if desc[current] == " ":
                last_space = current
            current_line += desc[current]
            if self.game.font.get_line_width(current_line) > width_limit or current >= len(desc)-1:              
                if current < len(desc)-1:
                    lines.append(desc[start:last_space])
                    current = last_space
                    start = last_space+1
                else:
                    lines.append(desc[start:])
                current_line = ""
            current += 1
        return lines

class Resource(Item):
    def __init__(self, game, type):
    
        #if not type in game.item.resource: return
    
        super().__init__(game)
        
        # Check for objects with duplicate names
        if type == "stone": objdata = self.game.data.get_object_by_num(390)
        else: objdata = self.game.data.get_object_by_name(type)
        
        self.init_item(objdata)
        self.sprite = game.sprite.get_tiles("springobjects")
        self.spr_frame = self.inv_frame
        self.stackable = True
        
class Tool(Item):
    def __init__(self, game, type):
        super().__init__(game)
        tool = game.item.tool[type]
        self.name = ""
        self.desc = tool["desc"]
        self.sprite = self.game.sprite.get_tiles(tool["sprite"])
        self.category_str = "Tool"
        self.quality = random.randint(0,len(tool["inv_frame"])-1)
        if self.quality > 0:
            self.name += self.quality_name(self.quality) + " " 
        self.name += tool["name"]
        self.inv_frame = tool["inv_frame"][self.quality]
        self.player_sequence = tool["player_sequence"]
        
        self.item_sequence = tool["item_sequence"]
        self.item_sequence = self.quality_item_sequence(self.item_sequence, self.quality)
        
        self.sprite_sequence = self.generate_sprite_sequence(self.item_sequence, tool["item_rot"])
        
        
        self.hair_yoff = tool["hair_yoff"]
        self.item_xoff = tool["item_xoff"]
        self.item_yoff = tool["item_yoff"]
        self.ecost = tool["ecost"]
        self.action_sequence = tool["action_sequence"]
        self.stackable = True
        self.hover = self.generate_hover()
        
    def quality_item_sequence(self, base_tuple, quality):
        outer = []
        if quality == 0: offset = 0
        if quality == 1: offset = 7
        if quality == 2: offset = 14
        if quality == 3: offset = 42
        if quality == 4: offset = 49
        for i in range(len(base_tuple)):
            inner = []
            for j in range(len(base_tuple[i])):
                inner.append(base_tuple[i][j]+offset)
            outer.append(tuple(inner))
        return tuple(outer)
        
    def generate_sprite_sequence(self, frames, rotations):
        out = []
        scale = self.game.config.screen_scaling
        size = (self.sprite[0].get_width(), self.sprite[0].get_height()*2)
        for outer in range(len(frames)):
            dir_sequence = []
            reverse = True if outer == 3 else False
            for inner in range(len(frames[outer])):
                # Get basic sprite
                surf = pygame.Surface(size, pygame.SRCALPHA).convert_alpha()
                if reverse:
                    base_surf = pygame.Surface(size, pygame.SRCALPHA).convert_alpha()
                    base_surf.blit(self.sprite[frames[outer][inner]-21],(0,0))
                    base_surf.blit(self.sprite[frames[outer][inner]],(0,16))
                    surf.blit(pygame.transform.flip(base_surf,True,False),surf.get_rect())
                else:
                    surf.blit(self.sprite[frames[outer][inner]-21],(0,0))
                    surf.blit(self.sprite[frames[outer][inner]],(0,16))
                
                #Rescale sprite
                scaled_surf = pygame.transform.scale(surf,(size[0]*scale,size[1]*scale))
                
                #Rotate sprite
                scaled_surf = self.rotate_tool(scaled_surf,rotations[outer][inner])
                
                #Finalize
                dir_sequence.append(scaled_surf)
            out.append(tuple(dir_sequence))
        return tuple(out)

        
    def rotate_tool(self,image,angle):
        scale = self.game.config.screen_scaling
        pos = (0,0)
        originPos = (image.get_width() // 2, image.get_height() // 2)
        
        image_rect = image.get_rect(topleft = (pos[0] - originPos[0], pos[1]-originPos[1]))
        offset_center_to_pivot = pygame.math.Vector2(pos) - image_rect.center
        rotated_offset = offset_center_to_pivot.rotate(-angle)
        rotated_image_center = (pos[0] - rotated_offset.x, pos[1] - rotated_offset.y)
        rotated_image = pygame.transform.rotate(image, angle)
        rotated_image_rect = rotated_image.get_rect(center = rotated_image_center)
        return rotated_image
        
        # Probably need to return a rect too? See below
        #self.rotated_arrow_rect = rotated_image_rect
       
class Food(Item):
    def __init__(self, game, type):
        super().__init__(game)
        

class Seeds(Item):
    def __init__(self, game, type):
        super().__init__(game)
        
class Weapon(Item):
    def __init__(self, game, type=None):
        super().__init__(game)
        
        # Overrides specific weapon for now
        self.init_item()
        self.sprite = self.game.sprite.get_tiles("weapons")
        self.stackable = False
        
        self.player_sequence = ((),
                                (),
                                (),
                                ())
        self.action_sequence = ((None,None,None,None,None,None),
                                (),
                                (),
                                ())
        self.item_sequence = ()
        self.item_xoff = ()
        self.item_yoff = ()
        self.hair_yoff = (-1,0,1,2,2,1)
        self.ecost = 2
        
    def init_item(self, data=None):
        if not data:
            data = self.game.data.get_random_weapon()
        self.parse_item_data(data)
        self.hover = self.generate_hover(256,192)
        return self
    
    def parse_item_data(self, data) -> None:
        datalist = data.split('/')
        self.inv_frame = int(datalist[0])
        self.name = datalist[1]
        self.category_str = self.get_category_label(datalist[9])
        self.desc = datalist[2]
        return datalist
        
    def get_category_label(self, data) -> None:        
        if int(data) == 0: return "Sword"
        if int(data) == 1: return "Dagger"
        if int(data) == 2: return "Hammer"
        if int(data) == 3: return "Sword"
        if int(data) == 4: return ""
        return ""
        
        
class ItemLoader:
    def __init__(self,game):
        print ("Initializing Items")
        self.resource = {}
        self.tool = {}
        self.weapon = {}
        self.food = {}
        self.seed = {}
        
    def init_second_stage(self):
        self.tool["hoe"] = {
            "name": "Hoe",
            "desc": "Used to dig and till soil",
            "ecost": 2,
            "sprite": "tools",
            "inv_frame": [47, 54, 61, 89, 96],  # Each quality level
            "player_sequence": ((198,199,200,201,201,202),
                                (144,145,146,147,147,148),
                                (108,109,110,111,111,112),
                                (144,145,146,147,147,148)),
            "action_sequence": ((None,None,None,("hoe",(0,1)),None,None),
                                (None,None,None,("hoe",(1,0)),None,None),
                                (None,None,None,("hoe",(0,-1)),None,None),
                                (None,None,None,("hoe",(-1,0)),None,None)),
            "item_sequence": ((42,42,43,43,43,265), # base frame
                             (44,44,44,44,44,265),  # tool 'level'
                             (45,45,46,46,46,265),  # computed in 
                             (44,44,44,44,44,265)), # tool constructor
            "item_xoff": ((-6,-3,-1,0,0,0),
                         (-10,0,6,12,12,0),
                         (0,0,0,0,0,0),
                         (5,0,-25,-28,-28,0)),
            "item_yoff": ((-1,4,10,16,16,16),
                         (-2,-3,1,25,25,0),
                         (-10,-5,2,2,2,0),
                         (-2,-3,1,25,25,0)),
            "item_rot": ((5,3,0,0,0,0),
                         (10,0,-45,-100,-100,0),
                         (0,0,0,0,0,0),
                         (-10,0,45,100,100,0)),
            "hair_yoff": (-1,0,1,2,2,1)
        }
        self.tool["pickaxe"] = {
            "name": "Pickaxe",
            "desc": "Used to break stones",
            "ecost": 2,
            "sprite": "tools",
            "inv_frame": [131, 138, 145, 173, 180],  # Each quality level
            "player_sequence": ((198,199,200,201,201,202),
                                (144,145,146,147,147,148),
                                (108,109,110,111,111,112),
                                (144,145,146,147,147,148)),
            "action_sequence": ((None,None,None,("pickaxe",(0,1)),None,None),
                                (None,None,None,("pickaxe",(1,0)),None,None),
                                (None,None,None,("pickaxe",(0,-1)),None,None),
                                (None,None,None,("pickaxe",(-1,0)),None,None)),
            "item_sequence": ((126,126,127,127,127,265), # base frame
                             (128,128,128,128,128,265),  # tool 'level'
                             (129,129,130,130,130,265),  # computed in 
                             (128,128,128,128,128,265)), # tool constructor
            "item_xoff": ((-6,-3,-1,0,0,0),
                         (-10,0,6,12,12,0),
                         (0,0,0,0,0,0),
                         (5,0,-25,-28,-28,0)),
            "item_yoff": ((-1,4,10,16,16,16),
                         (-2,-3,1,25,25,0),
                         (-10,-5,2,2,2,0),
                         (-2,-3,1,25,25,0)),
            "item_rot": ((5,3,0,0,0,0),
                         (10,0,-45,-100,-100,0),
                         (0,0,0,0,0,0),
                         (-10,0,45,100,100,0)),
            "hair_yoff": (-1,0,1,2,2,1)
        }
        self.tool["axe"] = {
            "name": "Axe",
            "desc": "Used to chop wood",
            "ecost": 2,
            "sprite": "tools",
            "inv_frame": [215, 222, 229, 257, 264],  # Each quality level
            "player_sequence": ((198,199,200,201,201,202),
                                (144,145,146,147,147,148),
                                (108,109,110,111,111,112),
                                (144,145,146,147,147,148)),
            "action_sequence": ((None,None,None,("axe",(0,1)),None,None),
                                ((None,None,None,("axe",(1,0)),None,None)),
                                ((None,None,None,("axe",(0,-1)),None,None)),
                                ((None,None,None,("axe",(-1,0)),None,None))),
            "item_sequence": ((210,210,211,211,211,265), # base frame
                             (212,212,212,212,212,265),  # tool 'level'
                             (213,213,214,214,214,265),  # computed in 
                             (212,212,212,212,212,265)), # tool constructor
            "item_xoff": ((-6,-3,-1,0,0,0),
                         (-10,0,6,12,12,0),
                         (0,0,0,0,0,0),
                         (5,0,-25,-28,-28,0)),
            "item_yoff": ((-1,4,10,16,16,16),
                         (-2,-3,1,25,25,0),
                         (-10,-5,2,2,2,0),
                         (-2,-3,1,25,25,0)),
            "item_rot": ((5,3,0,0,0,0),
                         (10,0,-45,-100,-100,0),
                         (0,0,0,0,0,0),
                         (-10,0,45,100,100,0)),
            "hair_yoff": (-1,0,2,3,3,2)
        }
        self.weapon["scythe"] = {
            "name": "Scythe",
            "desc": "It can cut grass in to hay, if you've built a silo",
            "ecost": 2,
            "sprite": "weapons",
            "inv_frame": [47],
            "player_sequence": ((72,73,74,75,76,77),
                                (90,91,92,93,94,95),
                                (108,109,110,111,112,113),
                                (90,91,92,93,94,95)),
            "action_sequence": ((None,None,None,None,None,None),
                                (None,None,None,None,None,None),
                                (None,None,None,None,None,None),
                                (None,None,None,None,None,None)),
            "item_sequence": ((47,47,47,47,47,265), # base frame
                             (47,47,47,47,47,265),  # tool 'level'
                             (47,47,47,47,47,265),  # computed in 
                             (47,47,47,47,47,265)), # tool constructor
            "item_xoff": ((-6,-3,-1,0,0,0),
                         (-10,0,6,12,12,0),
                         (0,0,0,0,0,0),
                         (5,0,-25,-28,-28,0)),
            "item_yoff": ((-1,4,10,16,16,16),
                         (-2,-3,1,25,25,0),
                         (-10,-5,2,2,2,0),
                         (-2,-3,1,25,25,0)),
            "item_rot": ((0,0,0,0,0,0),
                         (0,0,0,0,0,0),
                         (0,0,0,0,0,0),
                         (0,0,0,0,0,0)),
            "hair_yoff": (-1,0,1,2,2,1)
        }
        self.weapon["gscythe"] = {
            "name": "Golden Scythe",
            "desc": "It's more powerful than a normal scythe",
            "ecost": 2,
            "sprite": "weapons",
            "inv_frame": [53],
            "player_sequence": ((),
                                (),
                                (),
                                ()),
            "action_sequence": ((None,None,None,None,None,None),
                                (),
                                (),
                                ()),
            "item_sequence": (),
            "item_xoff": (),
            "item_yoff": (),
            "item_rot": ((0,0,0,0,0,0),
                         (0,0,0,0,0,0),
                         (0,0,0,0,0,0),
                         (0,0,0,0,0,0)),
            "hair_yoff": (-1,0,1,2,2,1)
        }
        self.tool["wateringcan"] = {
            "name": "Watering Can",
            "desc": "Used to water crops. It can be refilled at any water source",
            "ecost": 2,
            "sprite": "tools",
            "inv_frame": [296, 303, 310, 338, 345],  # Each quality level
            "player_sequence": ((),
                                (),
                                (),
                                ()),
            "action_sequence": ((None,None,None,None,None,None),
                                (),
                                (),
                                ()),
            "item_sequence": (),
            "item_xoff": (),
            "item_yoff": (),
            "item_rot": ((0,0,0,0,0,0),
                         (0,0,0,0,0,0),
                         (0,0,0,0,0,0),
                         (0,0,0,0,0,0)),
            "hair_yoff": (-1,0,1,2,2,1)
        }       
        #self.weapon["galaxysword"] = {
        #    "name": "Galaxy Sword",
        #    "desc": "",
        #    "inv_frame": [4]  # Each quality level
        #}