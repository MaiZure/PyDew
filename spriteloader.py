import pygame
import random

class SpriteLoader:
    def __init__(self, game):
        print("Initializing Sprites")
        
        self.game = game
        
        # Load all images in to a library (dictionary)
        self.sheet = {}
        self.load_spritesheets()
        
        self.tiles = {}
        self.build_tiles()
        
        # Metadata
        self.large_sprites = {}
        self.build_large_sprites()
        
    # Procedure to load all spritesheets from disk in to this object
    def load_spritesheets(self) -> None:
        # Each sheet contains a 3-tuple: (image, tile_width, tile_height)
        self.sheet["spring_outdoorsTileSheet"] = (pygame.image.load(".\\Tiles\\spring_outdoorsTileSheet.png").convert_alpha(), 16, 16)
        self.sheet["spring_outdoorsTileSheet2"] = (pygame.image.load(".\\Tiles\\spring_outdoorsTileSheet2.png").convert_alpha(), 16, 16)
        self.sheet["summer_outdoorsTileSheet"] = (pygame.image.load(".\\Tiles\\summer_outdoorsTileSheet.png").convert_alpha(), 16, 16)
        self.sheet["summer_outdoorsTileSheet2"] = (pygame.image.load(".\\Tiles\\summer_outdoorsTileSheet2.png").convert_alpha(), 16, 16)
        self.sheet["fall_outdoorsTileSheet"] = (pygame.image.load(".\\Tiles\\fall_outdoorsTileSheet.png").convert_alpha(), 16, 16)
        self.sheet["fall_outdoorsTileSheet2"] = (pygame.image.load(".\\Tiles\\fall_outdoorsTileSheet2.png").convert_alpha(), 16, 16)
        self.sheet["winter_outdoorsTileSheet"] = (pygame.image.load(".\\Tiles\\winter_outdoorsTileSheet.png").convert_alpha(), 16, 16)
        self.sheet["winter_outdoorsTileSheet2"] = (pygame.image.load(".\\Tiles\\winter_outdoorsTileSheet2.png").convert_alpha(), 16, 16)
        self.sheet["bushes"] = (pygame.image.load(".\\Tiles\\bushes.png").convert_alpha(), 16, 16)
        self.sheet["paths"] = (pygame.image.load(".\\Tiles\\paths.png").convert_alpha(), 16, 16)
        self.sheet["emily"] = (pygame.image.load(".\\Tiles\\Emily.png").convert_alpha(), 16, 32)
        self.sheet["cursors"] = (pygame.image.load(".\\Tiles\\Cursors.png").convert_alpha(), 16, 16)
        self.sheet["springobjects"] = (pygame.image.load(".\\Tiles\\springobjects.png").convert_alpha(), 16, 16)
    
    def build_tiles(self) -> None:
        for sheet in self.sheet: 
            self.tiles[sheet] = self.get_spritesheet_tiles(sheet)
    
    def get_tiles(self, name) -> list:
        return self.tiles[name]
        
    # Get the spritesheet from the library
    def get_spritesheet(self, name) -> pygame.image:
        return self.sheet[name][0]
    
    # Get the spritesheet's expected tile width
    def get_spritesheet_tile_width(self, name) -> int:
        return self.sheet[name][1]
    
    # Get the spritesheet's expected tile height
    def get_spritesheet_tile_height(self, name) -> int:
        return self.sheet[name][2]
        
    # Decompose the spritesheet in to a list of tiles
    def get_spritesheet_tiles(self,name) -> list:
        tiles = []
        spritesheet = self.get_spritesheet(name)
        sheet_width = spritesheet.get_width()
        sheet_height = spritesheet.get_height()
        tile_width = self.get_spritesheet_tile_width(name)
        tile_height = self.get_spritesheet_tile_height(name)
        
        # Loop through the sprite sheet and tilize
        for column in range(int(sheet_height/tile_height)):
            for row in range(int(sheet_width/tile_width)):
                rect = pygame.Rect(row*tile_width, column*tile_height, tile_width, tile_height)
                new_tile = pygame.Surface(rect.size, pygame.SRCALPHA).convert_alpha()
                new_tile.blit(spritesheet, (0,0), rect)
                tiles.append(new_tile)
                
        return tiles
        
    def build_large_sprites(self) -> None:
        self.large_sprites["spr_oak"] = {
            "sheet": "spring_outdoorsTileSheet",
            "tiles": [(0,3), (1,3), (2,3), (25, 3), (26, 3), (27,3), (50, 3), (51, 3), (52, 3), (75, 3), (76, 3), (77, 3), None, (101,2), None, None, (126,1), None],
            "sprite_height": 6,
            "sprite_width": 3,
            "sprite_origin": (1,5),
            "collision_width": 1,
            "collision_height": 1
        }
        self.large_sprites["spr_maple"] = {
            "sheet": "spring_outdoorsTileSheet",
            "tiles": [(3,3), (4,3), (5,3), (28, 3), (29, 3), (30,3), (53, 3), (54, 3), (55, 3), (78, 3), (79, 3), (80, 3), None, (104,2), None, None, (129,1), None],
            "sprite_height": 6,
            "sprite_width": 3,
            "sprite_origin": (1,5),
            "collision_width": 1,
            "collision_height": 1
        }
        self.large_sprites["spr_pine"] = {
            "sheet": "spring_outdoorsTileSheet",
            "tiles": [(10,3), (11,3), (12,3), (35, 3), (36, 3), (37,3), (60, 3), (61, 3), (62, 3), (85, 3), (86, 3), (87, 3), None, (111,2), None, None, (136,1), None],
            "sprite_height": 6,
            "sprite_width": 3,
            "sprite_origin": (1,5),
            "collision_width": 1,
            "collision_height": 1
        }
        self.large_sprites["spr_bush_large"] = {
            "sheet": "bushes",
            "tiles": [(64,3), (65,3), (66,3), (72,1), (73, 1), (74, 1), (80,1), (81, 1), (82, 1)],
            "sprite_height": 3,
            "sprite_width": 3,
            "sprite_origin": (0,2),
            "collision_width": 3,
            "collision_height": 2
        }
        self.large_sprites["spr_bush_medium"] = {
            "sheet": "bushes",
            "tiles": [(0,3), (1,3), (8,2), (9, 2), (16, 1), (17,1)],
            "sprite_height": 3,
            "sprite_width": 2,
            "sprite_origin": (0,2),
            "collision_width": 2,
            "collision_height": 1
        }
        self.large_sprites["spr_bush_small"] = {
            "sheet": "bushes",
            "tiles": [[(112,2), (120,1)],[(113,2), (121,1)]],
            "sprite_height": 2,
            "sprite_width": 1,
            "sprite_origin": (0,1),
            "collision_width": 1,
            "collision_height": 1
        }
        
        
        
    def get_large_sprite_origin(self,name) -> tuple:
        return self.large_sprites[name]["sprite_origin"]
        
    def get_collision_width(self,name) -> int:
        return self.large_sprites[name]["collision_width"]
        
    def get_collision_height(self,name) -> int:
        return self.large_sprites[name]["collision_height"]
        
    def get_large_sprite(self, name):
        sheet = self.large_sprites[name]["sheet"]
        sheet_tiles = self.get_tiles(sheet)
        sprite_height = self.large_sprites[name]["sprite_height"]
        sprite_width = self.large_sprites[name]["sprite_width"]
        tiles = self.large_sprites[name]["tiles"].copy()
        if type(tiles[0]) == list: # Choose from two possible sprites
            tiles = random.choice(tiles).copy()
        rect = pygame.Rect(0, 0, sprite_width*16, sprite_height*16)
        new_sprite = pygame.Surface(rect.size, pygame.SRCALPHA).convert_alpha()
        
        for column in range(sprite_height):
            for row in range(sprite_width):
                src_tile = tiles.pop(0)
                if src_tile:
                    rect = pygame.Rect(row*16, column*16, 16, 16)
                    new_sprite.blit(sheet_tiles[src_tile[0]], rect)
        return new_sprite
     
    def get_large_sprite_reverse(self, name) -> pygame.Surface:
        base_sprite = self.get_large_sprite(name)
        rect = pygame.Rect(0, 0, base_sprite.get_width(), base_sprite.get_height())
        new_sprite = pygame.Surface(rect.size, pygame.SRCALPHA).convert_alpha()
        new_sprite.blit(pygame.transform.flip(base_sprite, True, False), rect)
        return new_sprite