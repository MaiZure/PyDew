import pygame

class SpriteLoader:
    def __init__(self):
        print("Initializing Sprites")
        
        # Load all images in to a library (dictionary)
        self.sheet = {}       
        self.load_spritesheets()
    
    # Procedure to load all spritesheets from disk in to this object
    def load_spritesheets(self) -> None:
        # Each sheet contains a 3-tuple: (image, tile_width, tile_height)
        self.sheet["spring_outdoors"] = (pygame.image.load(".\\Tiles\\Tiles_spring.png").convert_alpha(), 16, 16)
        self.sheet["summer_outdoors"] = (pygame.image.load(".\\Tiles\\Tiles_summer.png").convert_alpha(), 16, 16)
        self.sheet["fall_outdoors"] = (pygame.image.load(".\\Tiles\\Tiles_fall.png").convert_alpha(), 16, 16)
        self.sheet["winter_outdoors"] = (pygame.image.load(".\\Tiles\\Tiles_winter.png").convert_alpha(), 16, 16)
        self.sheet["emily"] = (pygame.image.load(".\\Tiles\\Emily.png").convert_alpha(), 16, 32)
    
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
    
    # Gets all tiles for a map
    def get_spritesheet_map_tiles(self, name) -> list:
        tiles = self.get_spritesheet_tiles(name)
        tiles.insert(0,None)  # All map tiles start with an empty (no-draw index)
        return tiles
        