import random
import pygame

class Item:
    def __init__(self, game):
        self.game = game
        self.x = None
        self.y = None
        
        
    def render(self, screen):
        pass
    
    def render_inv_slot(self, screen, slot_num):
        slot_pos = self.game.ui.ibar.slot_pos[slot_num]
        sprite = self.sprite[self.inv_frame]
        scaled_item = pygame.transform.scale(sprite,(60,60))
        screen.blit(scaled_item, (slot_pos[0],slot_pos[1]))
        
class Tool(Item):
    def __init__(self, game, type):
        super().__init__(game)
        tool = game.item.tool[type]
        self.quality = random.choice([0,1,2,3,4])
        self.sprite = self.game.sprite.get_tiles("tools")
        self.inv_frame = tool["inv_frame"][self.quality]
        
class Food(Item):
    def __init__(self, game):
        super().__init__(game)
        

class Seeds(Item):
    def __init__(self, game):
        super().__init__(game)
        
class Weapon(Item):
    def __init__(self, game):
        super().__init__(game)
        
class ItemLoader:
    def __init__(self,game):
        print ("Initializing Items")
        self.tool = {}
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