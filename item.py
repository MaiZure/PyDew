import random
import pygame

class Item:
    def __init__(self, game):
        self.game = game
        self.gx = None
        self.gy = None
        self.x = None
        self.y = None
        self.name = ""
        self.count = 1
        self.stackable = False
        
        
    def render(self, screen):
        if not self.x or not self.y:
            return
        if not self.game.world.is_visible(self.gx, self.gy):
            return
            
        top_left_x = self.game.world.top_left_x
        top_left_y = self.game.world.top_left_y
        screen.blit(self.sprite[self.spr_frame], (self.x-top_left_x,self.y-top_left_y), (0,0,16,16))
    
    def render_inv_slot(self, screen, slot_num):
        slot_pos = self.game.ui.ibar.slot_pos[slot_num]
        sprite = self.sprite[self.inv_frame]
        scaled_item = pygame.transform.scale(sprite,(60,60))
        screen.blit(scaled_item, (slot_pos[0],slot_pos[1]))
        if self.count > 1:
            ui = self.game.ui
            num = min(self.count,9) # prevent crash when more than 10 items for now
            screen.blit(ui.tiny_numbers, (slot_pos[0]+55,slot_pos[1]+53),ui.tiny_numbers_rect[num]) 
        
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
        
        if self.game.player.hitrect.collidepoint(self.x,self.y):
            self.game.player.pickup_item(self)

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