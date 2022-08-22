import pygame, os
import random

class SpriteLoader:
    def __init__(self, game):
        print("Initializing Sprites")
        
        self.game = game
        
        # Load all images in to a library (dictionary)
        self.sheet = {}
        self.character_sheet = {}
        self.player_sheet = {}
        self.font = {}
        self.tiles = {}
        self.large_sprites = {}
        
        self.load_tile_spritesheets()
        self.load_character_spritesheets()
        
        self.load_player_spritesheets()
        self.pc_index = self.index_sprite(self.player_sheet["farmer_base"][0])
        
        self.load_font_spritesheets()
        
        #Put all character sheets in base sheets
        self.sheet = self.sheet | self.character_sheet | self.player_sheet | self.font
        
        self.build_tiles()  # loads {tiles}
        self.build_large_sprites()  # loads {large_sprites}
    
    def init_second_stage(self):
        pass
        
    # Procedure to load all spritesheets from disk in to this object
    def load_tile_spritesheets(self) -> None:
        # Each sheet contains a 3-tuple: (image, tile_width, tile_height)
        path = ".\\Tiles\\"
        files = os.listdir(path)
        for file in files:
            name = ((file.split("."))[0])
            size = (16, 16)
            if name == "MenuTiles": size = (64,64)
            if name == "daybg": size = (128,192)
            if name == "map": size = (300,180)
            if name == "houses": size = (272,144)
            if name == "grass": size = (15,20)
            if name == "crops": size = (16,32)
            #if name == "walls_and_floors": size = (16,32)
            self.sheet[name] = (pygame.image.load(open(path+file)).convert_alpha(), size[0], size[1])
    
    def load_character_spritesheets(self) -> None:
        # Each sheet contains a 3-tuple: (image, tile_width, tile_height)
        path = ".\\Characters\\"
        files = os.listdir(path)
        for file in files:
            name = ((file.split("."))[0]).lower()
            if name == "farmer": continue #skip subdirs - cheap hack for now
            self.character_sheet[name] = (pygame.image.load(open(path+file)).convert_alpha(), 16, 32)
            
    def load_player_spritesheets(self) -> None:
        # Each sheet contains a 3-tuple: (image, tile_width, tile_height)
        path = ".\\Characters\\Farmer\\"
        self.player_sheet["farmer_base"] = (pygame.image.load(open(path+"farmer_base.png")).convert_alpha(), 16, 32)
        self.player_sheet["hairstyles"] = (pygame.image.load(open(path+"hairstyles.png")).convert_alpha(), 16, 32)
        self.player_sheet["shirts"] = (pygame.image.load(open(path+"shirts.png")).convert_alpha(), 8, 32)
        self.player_sheet["pants"] = (pygame.image.load(open(path+"pants.png")).convert_alpha(), 192, 672)
        self.player_sheet["skinColors"] = (pygame.image.load(open(path+"skinColors.png")).convert_alpha(), 3, 24)
        
    def load_font_spritesheets(self) -> None:
        # Each sheet contains a 3-tuple: (image, tile_width, tile_height)
        # Font sheets are loaded as a single tile since processing requires custom treatment
        path = ".\\Font\\"
        self.font["spritefont1"] = (pygame.image.load(open(path+"SpriteFont1.png")).convert_alpha(), 512, 272)
        self.font["smallfont"] = (pygame.image.load(open(path+"SmallFont.png")).convert_alpha(), 256, 260)
        self.font["tinyfont"] = (pygame.image.load(open(path+"tinyFont.png")).convert_alpha(), 512, 196)
        self.font["tinyfontborder"] = (pygame.image.load(open(path+"tinyFontBorder.png")).convert_alpha(), 512, 200)


    # Build the sprite index for player body. Needs 'farmer_base' and 'skinColors' loaded
    def index_sprite(self, surf):
        # Uses the main spritesheet including all player images (no tiles)
        index = {"A": [], "B": [], "C": []}
        colorA = self.player_sheet["skinColors"][0].get_at((0,0))
        colorB = self.player_sheet["skinColors"][0].get_at((1,0))
        colorC = self.player_sheet["skinColors"][0].get_at((2,0))
        size = surf.get_size()
        for j in range(size[1]):
            for i in range(size[0]):
                col = surf.get_at((i,j))
                if col == colorA: index["A"].append((i,j))
                if col == colorB: index["B"].append((i,j))
                if col == colorC: index["C"].append((i,j))
        return index
        
    def change_skin(self, skin_num):
        colA = self.player_sheet["skinColors"][0].get_at((0,skin_num))
        colB = self.player_sheet["skinColors"][0].get_at((1,skin_num))
        colC = self.player_sheet["skinColors"][0].get_at((2,skin_num))
        base = self.player_sheet["farmer_base"][0]
        for point in self.pc_index["A"]:
            base.set_at((point[0],point[1]),colA)
        for point in self.pc_index["B"]:
            base.set_at((point[0],point[1]),colB)
        for point in self.pc_index["C"]:
            base.set_at((point[0],point[1]),colC)
        
        
        
        self.sheet["farmer_base"] = self.player_sheet["farmer_base"]
        self.build_tiles("farmer_base")
        
    def colorize_tiles(self, old_tiles, color):
        new_tiles = []
        for tile in old_tiles:
            new_tile = tile.copy()
            color_layer = pygame.Surface(tile.get_size()).convert_alpha()
            color_layer.fill(color)
            new_tile.blit(color_layer, (0,0), special_flags = pygame.BLEND_RGBA_MIN)
            new_tiles.append(new_tile)
        return new_tiles
    
    def build_tiles(self, sheet=None) -> None:
        if sheet:
            self.tiles[sheet] = self.get_spritesheet_tiles(sheet)
        else:
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
        
    def rescale_tiles(self, tiles, factor) -> list:
        output_tiles = []
        for tile in tiles:
            base_size = tile.get_size()
            new_tile = pygame.transform.scale(tile, (int(base_size[0]*factor),int(base_size[1]*factor)))
            output_tiles.append(new_tile)
        return output_tiles
        
    def rescale_sprite(self, src, factor) -> pygame.Surface:
        base_size = src.get_size()
        dest = pygame.Surface(base_size, pygame.SRCALPHA)
        dest = pygame.transform.scale(src, (int(base_size[0]*factor),int(base_size[1]*factor)))
        return dest
        
    def get_large_sprite_origin(self,name) -> tuple:
        return self.large_sprites[name]["sprite_origin"]
        
    def get_collision_width(self,name) -> int:
        return self.large_sprites[name]["collision_width"]
        
    def get_collision_height(self,name) -> int:
        return self.large_sprites[name]["collision_height"]
       
    def get_draw_off_x(self,name) -> int:
        return self.large_sprites[name]["draw_off_x"] if "draw_off_x" in self.large_sprites[name] else 0
    
    def get_draw_off_y(self,name) -> int:
        return self.large_sprites[name]["draw_off_y"] if "draw_off_y" in self.large_sprites[name] else 0
    
    def get_large_sprite(self, name):
        sheet = self.large_sprites[name]["sheet"]
        sheet_tiles = self.get_tiles(sheet)
        sprite_height = self.large_sprites[name]["sprite_height"]
        sprite_width = self.large_sprites[name]["sprite_width"]
        tw_px = self.large_sprites[name]["tile_width_px"] if "tile_width_px" in self.large_sprites[name] else 16
        th_px = self.large_sprites[name]["tile_height_px"] if "tile_height_px" in self.large_sprites[name] else 16
        tiles = self.large_sprites[name]["tiles"].copy()
        if type(tiles[0]) == list: # Choose from two possible sprites
            tiles = random.choice(tiles).copy()
        rect = pygame.Rect(0, 0, sprite_width*tw_px, sprite_height*th_px)
        new_sprite_mid = pygame.Surface(rect.size, pygame.SRCALPHA).convert_alpha()
        new_sprite_front = pygame.Surface(rect.size, pygame.SRCALPHA).convert_alpha()
        new_sprite_all = pygame.Surface(rect.size, pygame.SRCALPHA).convert_alpha()
        
        for column in range(sprite_height):
            for row in range(sprite_width):
                src_tile = tiles.pop(0)
                if src_tile:
                    rect = pygame.Rect(row*16, column*16, tw_px, th_px) # Optimize - don't make 2 sprites if not used
                    if src_tile[1] == 1:  #Should be < 3 when mid layer is actually working (rendered by gy order) 
                        new_sprite_mid.blit(sheet_tiles[src_tile[0]], rect)
                    if src_tile[1] > 1 :
                        new_sprite_front.blit(sheet_tiles[src_tile[0]], rect)
        new_sprite_all.blit(new_sprite_mid, (0,0))
        new_sprite_all.blit(new_sprite_front, (0,0))
        return new_sprite_mid, new_sprite_front, new_sprite_all
     
    def get_large_sprite_reverse(self, name) -> pygame.Surface:
        base_sprite = self.get_large_sprite(name) #This is a 3-tuple
        rect = pygame.Rect(0, 0, base_sprite[0].get_width(), base_sprite[0].get_height())
        new_sprite = (pygame.Surface(rect.size, pygame.SRCALPHA).convert_alpha(),
            pygame.Surface(rect.size, pygame.SRCALPHA).convert_alpha(),
            pygame.Surface(rect.size, pygame.SRCALPHA).convert_alpha())
        new_sprite[0].blit(pygame.transform.flip(base_sprite[0], True, False), rect)
        new_sprite[1].blit(pygame.transform.flip(base_sprite[1], True, False), rect)
        new_sprite[2].blit(pygame.transform.flip(base_sprite[2], True, False), rect)
        return new_sprite
        
    def build_large_sprites(self) -> None:
        # 1 and 2 in 'mid' and 3 in front
        season = self.game.save.season
        self.large_sprites["spr_oak"] = {
            "sheet": "spring_outdoorsTileSheet",
            "tiles": [(0,2), (1,2), (2,2), (25, 2), (26, 2), (27,2), (50, 2), (51, 2), (52, 2), (75, 2), (76, 2), (77, 2), None, (101,1), None, None, (126,1), None],
            "sprite_height": 6,
            "sprite_width": 3,
            "sprite_origin": (1,5),
            "collision_width": 1,
            "collision_height": 1
        }
        self.large_sprites["spr_maple"] = {
            "sheet": "spring_outdoorsTileSheet",
            "tiles": [(3,2), (4,2), (5,2), (28, 2), (29, 2), (30,2), (53, 2), (54, 2), (55, 2), (78, 2), (79, 2), (80, 2), None, (104,1), None, None, (129,1), None],
            "sprite_height": 6,
            "sprite_width": 3,
            "sprite_origin": (1,5),
            "collision_width": 1,
            "collision_height": 1
        }
        self.large_sprites["spr_pine"] = {
            "sheet": "spring_outdoorsTileSheet",
            "tiles": [(10,2), (11,2), (12,2), (35, 2), (36, 2), (37,2), (60, 2), (61, 2), (62, 2), (85, 2), (86, 2), (87, 2), None, (111,1), None, None, (136,1), None],
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
            "collision_height": 1
        }
        self.large_sprites["spr_bush_medium"] = {
            "sheet": "bushes",
            "tiles": [(0,2), (1,2), (8,1), (9, 1), (16, 1), (17,1)],
            "sprite_height": 3,
            "sprite_width": 2,
            "sprite_origin": (0,2),
            "collision_width": 2,
            "collision_height": 1
        }
        self.large_sprites["spr_bush_small"] = {
            "sheet": "bushes",
            "tiles": [[(112,1), (120,1)],[(113,1), (121,1)]],
            "sprite_height": 2,
            "sprite_width": 1,
            "sprite_origin": (0,1),
            "collision_width": 1,
            "collision_height": 1
        }
        self.large_sprites["spr_stick"] = {
            "sheet": "springobjects",
            "tiles": [[(294,1)],[(295,1)]],
            "sprite_height": 1,
            "sprite_width": 1,
            "sprite_origin": (0,0),
            "collision_width": 1,
            "collision_height": 1
        }
        self.large_sprites["spr_weed"] = {
            "sheet": "springobjects",
            "tiles": [[(784,1)],[(674,1)],[(675,1)]],
            "sprite_height": 1,
            "sprite_width": 1,
            "sprite_origin": (0,0),
            "collision_width": 1,
            "collision_height": 1
        }
        self.large_sprites["spr_rock_small"] = {
            "sheet": "springobjects",
            "tiles": [[(343,1)],[(450,1)]],
            "sprite_height": 1,
            "sprite_width": 1,
            "sprite_origin": (0,0),
            "collision_width": 1,
            "collision_height": 1
        }
        self.large_sprites["spr_log"] = {
            "sheet": "springobjects",
            "tiles": [[(602,1),(603,1),(626,1),(627,1)]],
            "sprite_height": 2,
            "sprite_width": 2,
            "sprite_origin": (0,0),
            "collision_width": 2,
            "collision_height": 2
        }
        self.large_sprites["spr_grass"] = {
            "sheet": "grass",
            "tiles": [[(0+(season*4),1)],[(1+(season*4),1)],[(2+(season*4),1)]],
            "sprite_height": 1,
            "sprite_width": 1,
            "tile_width_px": 15,
            "tile_height_px": 20,
            "draw_off_x": 1,
            "draw_off_y": -4,
            "sprite_origin": (0,0),
            "collision_width": 0,
            "collision_height": 0
        }
        self.large_sprites["spr_little_tree"] = {
            "sheet": "paths",
            "tiles": [[(23,1)]],
            "sprite_height": 1,
            "sprite_width": 1,
            "sprite_origin": (0,0),
            "collision_width": 1,
            "collision_height": 1
        }
        self.large_sprites["spr_stump_large"] = {
            "sheet": "springobjects",
            "tiles": [[(600,1),(601,1),(624,1),(625,1)]],
            "sprite_height": 2,
            "sprite_width": 2,
            "sprite_origin": (0,0),
            "collision_width": 2,
            "collision_height": 2
        }
        self.large_sprites["spr_rock_large"] = {
            "sheet": "springobjects",
            "tiles": [[(672,1),(673,1),(696,1),(697,1)]],
            "sprite_height": 2,
            "sprite_width": 2,
            "sprite_origin": (0,0),
            "collision_width": 2,
            "collision_height": 2
        }