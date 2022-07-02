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
        self.type_str = ""
        self.desc = ""
      
        self.spritesheet = self.game.sprite.get_tiles("MenuTiles")
        self.hover = self.generate_hover(256,256)
        
        
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
                
                
    def generate_hover(self, width, height):
        tl_corner = (0,0,16,16)
        tr_corner = (47,0,16,16)
        bl_corner = (0,47,16,16)
        br_corner = (47,47,16,16)
        left_bar = (0,16,12,32)
        right_bar = (47,16,12,32)
        top_bar = (16,0,32,16)
        bottom_bar = (12,44,32,16)
        
        hover = pygame.Surface((width,height),pygame.SRCALPHA)
        
        hover.blit(pygame.transform.scale(self.spritesheet[9],(width-16,height-16)), (8,8))
        
        
        for i in range(16,width-16,32):
            hover.blit(self.spritesheet[16], (i,0), top_bar)
            hover.blit(self.spritesheet[16], (i,105), bottom_bar)
            hover.blit(self.spritesheet[16], (i,height-19), bottom_bar)
            
        for i in range(16,height-16,32):
            hover.blit(self.spritesheet[16], (0,i), left_bar)
            hover.blit(self.spritesheet[16], (width-16,i), right_bar)
            
        hover.blit(self.spritesheet[16], (0,0), tl_corner)
        hover.blit(self.spritesheet[16], (0,108), bl_corner)
        hover.blit(self.spritesheet[16], (0,height-16), bl_corner)
        
        hover.blit(self.spritesheet[16], (width-16,0), tr_corner)
        hover.blit(self.spritesheet[16], (width-16,108), br_corner)
        hover.blit(self.spritesheet[16], (width-16,height-16), br_corner)
        
        
            
        self.game.font.set_font("spritefont1")
        self.game.font.draw_text(self.name, hover, (18, 20), scaling_cut = 1, justify="left")
        
        self.game.font.set_font("smallfont")
        self.game.font.draw_text("Tool", hover, (18, 68), scaling_cut = 1, justify="left")
        
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
            
        if self.distance_to_player() < 10:
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
        return self
        
    def parse_item_data(self, data) -> None:
        datalist = data.split('/')
        self.inv_frame = int(datalist[0])
        self.name = datalist[1]
        self.type_str = datalist[4]
        self.desc = datalist[6]
        
        self.hover = self.generate_hover(256,256)
        return datalist

class Resource(Item):
    def __init__(self, game, type):
        super().__init__(game)
        resource = game.item.resource[type]
        self.name = resource["name"]
        self.sprite = self.game.sprite.get_tiles("springobjects")
        self.inv_frame = resource["inv_frame"][0]
        self.spr_frame = self.inv_frame
        self.stackable = True
        
class Tool(Item):
    def __init__(self, game, type):
        super().__init__(game)
        tool = game.item.tool[type]
        self.name = tool["name"]
        self.quality = random.choice([0,1,2,3,4])
        self.sprite = self.game.sprite.get_tiles("tools")
        self.inv_frame = tool["inv_frame"][self.quality]
        self.stackable = True
        
class Food(Item):
    def __init__(self, game, type):
        super().__init__(game)
        

class Seeds(Item):
    def __init__(self, game, type):
        super().__init__(game)
        
class Weapon(Item):
    def __init__(self, game, type):
        super().__init__(game)
        weapon = game.item.weapon[type]
        self.name = weapon["name"]
        self.sprite = self.game.sprite.get_tiles("weapons")
        self.inv_frame = weapon["inv_frame"][0]
        self.stackable = False
        
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
            "inv_frame": [47, 54, 61, 89, 96]  # Each quality level
        }
        self.tool["pickaxe"] = {
            "name": "Pickaxe",
            "inv_frame": [131, 138, 145, 173, 180]  # Each quality level
        }
        self.tool["axe"] = {
            "name": "Axe",
            "inv_frame": [215, 222, 229, 257, 264]  # Each quality level
        }
        self.tool["wateringcan"] = {
            "name": "Watering Can",
            "inv_frame": [296, 303, 310, 338, 345]  # Each quality level
        }       
        self.weapon["galaxysword"] = {
            "name": "Galaxy Sword",
            "inv_frame": [4]  # Each quality level
        }
        self.resource["wood"] = {
            "name": "Wood",
            "inv_frame": [388]  # Each quality level
        }
        self.resource["stone"] = {
            "name": "Stone",
            "inv_frame": [390]  # Each quality level
        }