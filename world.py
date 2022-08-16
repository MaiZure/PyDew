import random
import pygame
from npc import NPC
from item import *

from mapobject import *

class World:

    def __init__(self, game):
        print("Initializing World")
        self.game = game
        self.top_left_x = 0
        self.top_left_y = 0
        self.top_left_x_last = 0
        self.top_left_y_last = 0
        self.optimized_render = False
        self.redraw_front = True
        self.redraw_objects = True
        self.map_width = 0
        self.map_height = 0
        self.hour = 6
        self.minute = 0
        self.tick_time = 0
        self.speed_time = False
        
        self.map_tiles = {}         # Nested dictionary of MapTiles {map_name}{(gx,gy)}
        self.tileset = []
        self.tileset_index = {}
        self.current_map = "" #town
        self.current_map_path_objects = []
        self.special_objects = {}
        self.edge_warp_points = {}  # Map edge warps
        self.warp_points = {}       # (legacy) object warp points (doors)
        self.action_points = {}     # General map action list
        self.paths_tile_base = 0
        self.animated_tiles = []
        self.passable_tiles = []
        self.diggable_tiles = []
        self.impassable_tiles = []
        self.collision_map = []     # Basic Boolean collisions (Aligned with *_layer)
        self.spawnable_map = []
        self.npcs = []
        self.lights = []
        self.outdoor_ambient = (0,0,0)
        self.ambient_light = (0,0,0) #(0,0,0) - day/clear, (180,150, 0) - night, (50,50,0) - day/raining
        self.darkening = False
        
        self.items = {}      # Items in the world
        self.objects = {}    # Objects on the map 
        
        self.bg_tile_update_reel = [[] for a in range(60)]   # Maintan 60 frames
        self.bldg_tile_update_reel = [[] for a in range(60)]
        
        # Map layers
        self.bg_layer = []
        self.bldg_layer = []
        self.path_layer = []
        self.front_layer = []
        self.afront_layer = []
        
        self.map_width = 0 
        self.map_height = 0
        self.outdoors = True
        self.night = False
        
    @property
    def speed_factor(self):
        return 60 if self.speed_time else 1
        
    def init_second_stage(self):
        for key in self.game.map.map:
            self.items[key] = []
            
        self.init_map("farm") #normally forest
        
    def init_map(self, map_name) -> bool:
        
        if not map_name in self.game.map.map:
            print("ERROR - Map doesn't exist yet ("+map_name+")")
            return False
            
        self.current_map = map_name
        self.new_map = True
        
        self.bg_tile_update_reel = [[] for a in range(60)]   # Maintan 60 frames in to the future
        self.bldg_tile_update_reel = [[] for a in range(60)] # Maintan 60 frames in to the future
        
        self.current_map_path_objects.clear()
        
        #TODO - Make these layer arrays
        self.bg_layer = self.game.map.get_layer_data(self.current_map,"Back")
        self.bldg_layer = self.game.map.get_layer_data(self.current_map,"Buildings")
        self.path_layer = self.game.map.get_layer_data(self.current_map,"Paths")
        self.front_layer = self.game.map.get_layer_data(self.current_map,"Front")
        self.afront_layer = self.game.map.get_layer_data(self.current_map,"AlwaysFront")
        
        self.map_width = self.game.map.get_layer_width(self.current_map,0)
        self.map_height = self.game.map.get_layer_height(self.current_map,0)
        
        # Create intermediate surfaces
        rect = pygame.Rect(0, 0, self.map_width*16, self.map_height*16) 
        self.bg = pygame.Surface(rect.size).convert()
        self.mid = pygame.Surface(rect.size, pygame.SRCALPHA).convert_alpha()
        self.mid_object = pygame.Surface(rect.size, pygame.SRCALPHA).convert_alpha()
        self.fg = pygame.Surface(rect.size, pygame.SRCALPHA).convert_alpha()
        self.front_object = pygame.Surface(rect.size, pygame.SRCALPHA).convert_alpha()
        
        # Clear old surfaces
        self.game.bg_surface.fill(pygame.Color(0,0,0,0))
        self.game.mid_surface.fill(pygame.Color(0,0,0,0))
        self.game.fg_surface.fill(pygame.Color(0,0,0,0))
        
        # Create basic map objects (if first visit)
        self.create_map_tiles(self.current_map, (self.map_width, self.map_height))
        
        self.init_map_second_stage()
        return True
        
        
    def init_map_second_stage(self):
        self.lights = []
        self.outdoors = self.game.map.get_map_outdoors(self.current_map)
        
        if self.outdoors: 
            self.ambient_light = (0,0,0)
        else: 
            self.ambient_light = self.game.map.get_ambient_light(self.current_map)
            
        self.init_specials()
        
        self.tileset = self.game.map.get_map_tiles(self.current_map)
        self.tileset_index = self.game.map.get_map_tileset_index(self.current_map)
        self.animated_tiles = self.game.map.get_map_animations(self.current_map, self.tileset_index)
        self.passable_tiles, self.impassable_tiles = self.game.map.get_passable_tiles(self.current_map, self.tileset_index)
        self.diggable_tiles = self.game.map.get_diggable_tiles(self.current_map, self.tileset_index)
        self.edge_warp_points = self.game.map.get_map_warps(self.current_map)
        self.warp_points = self.game.map.get_map_warpactions(self.current_map)
        self.action_points = self.game.map.get_map_actions(self.current_map)
        
        self.collision_map = self.generate_collision_map()
        
        self.embed_map_animations(self.bg_layer, self.bg_tile_update_reel)
        self.embed_map_animations(self.bldg_layer, self.bldg_tile_update_reel)
        
        for tiles in self.map_tiles[self.current_map]:
            tile = self.map_tiles[self.current_map][tiles]
            self.set_tile_neighbors(tile)
            tile.init_second_stage()
   
        self.current_map_path_objects = self.get_all_map_objects(self.current_map)
        
        for mapobject in self.current_map_path_objects:
            mapobject.init_second_stage()     

        for tiles in self.map_tiles[self.current_map]:
            tile = self.map_tiles[self.current_map][tiles]
            tile.update() #tile.render_tile()
         
        self.generate_background_specials()
        
        self.init_npcs()
        
    def create_map_tiles(self, map, location):
        if map in self.map_tiles: return    # No need to create twice
        self.map_tiles[map] = {}
        width = location[0]
        height = location[1]
        for j in range(height):
            for i in range(width):
                key = (i,j)
                tile = MapTile(self.game, map, (i,j))
                self.map_tiles[map][key] = tile 
                tile_num = self.get_tile_num(i,j)
                
                if self.bg_layer: 
                    if type(self.bg_layer[tile_num]) == list:  # This is an animated tile
                        tile.bg_layer = self.bg_layer[tile_num][0][1]
                        tile.animated = True
                    else:
                        tile.bg_layer = self.bg_layer[tile_num]
                if self.bldg_layer:
                    if type(self.bldg_layer[tile_num]) == list:  # This is an animated tile
                        tile.bldg_layer = self.bldg_layer[tile_num][0][1]
                        tile.animated = True
                    else:
                        tile.bldg_layer = self.bldg_layer[tile_num]
                        
                if self.path_layer: tile.path_layer = self.path_layer[tile_num]                   
                if self.front_layer: tile.front_layer = self.front_layer[tile_num]                   
                if self.afront_layer: tile.afront_layer = self.afront_layer[tile_num]
                    
    
    def create_wood(self):
    
        # Practice items
        new_item = Resource(self.game, "wood")
        new_item.create_at(self.game.player.x-24, self.game.player.y-24)
        self.items[self.current_map].append(new_item)
               
    def set_random_season(self):
        self.game.config.season = random.choice(["spring","summer","fall","winter"])
        self.set_season()
        
    def init_npcs(self):
        if self.npcs: return
        if self.current_map != "forest": return
        
        self.npcs.append(NPC(self.game))
        
    def generate_background_specials(self):
        for object in self.special_objects[self.current_map]:
            object.render_back(self.bg)
            
                    
    def generate_collision_map(self) -> list:
        collision_map = []
        
        # Use bldg_layer as a baseline
        for tile in self.bldg_layer:
            if tile:
                if tile in self.passable_tiles: # Handle custom properties
                    collision_map.append(0)
                else:
                    collision_map.append(1)
            else:
                collision_map.append(0)
                
        # Handle custom bg_layer properties
        for tile_index in range(len(self.bg_layer)):
            if self.bg_layer[tile_index] in self.impassable_tiles:
                collision_map[tile_index] = 1
        return collision_map
        
    def embed_map_animations(self, layer, reel):
        matchlist = self.make_animation_matchlist()
        for i in range(len(layer)):
            tile = layer[i]
            if tile in matchlist:
                layer[i] = self.find_animation_reel(tile)
                if layer == self.bg_layer:
                    reel[random.randint(0,59)]+=[i]
                else:
                    reel[0]+=[i]
    def make_animation_matchlist(self):
        match = []
        for i in range(len(self.animated_tiles)):
            match.append(self.animated_tiles[i][0][1])
        return match
        
    def find_animation_reel(self, first_tile):
        for reel in self.animated_tiles:
            if reel[0][1] == first_tile:
                return reel.copy()
        return None
        
    def do_action(self, location):
        if location not in self.action_points:
            return print("No action at " + str(location))
            
        action = self.action_points[location]
        action_type = action[0]
        print(action)
        if action_type == "Message": pass
        if action_type in ("LockedDoorWarp","Warp"):  # [type, tx, ty, dest_map, open time, close time, person, relation]
            target_gx = int(action[1])
            target_gy = int(action[2])
            target_map = action[3].lower()
            self.warp_player((target_map, target_gx, target_gy))
        if action_type == "WarpCommunityCenter":
            self.warp_player(("communitycenter_ruins", 33, 21))
        if action_type == "Billboard": pass
        if action_type == "Garbage": pass
        if action_type == "HMTGF": pass
        if action_type == "DwarfGrave": pass
        if action_type == "TownMainBox": pass
        if action_type == "IceCreamStand": pass
        if action_type == "EnterSewer":
            self.warp_player(("sewer", 16, 12))
        
    def init_active_map(self):
        self.set_map_width(self.map_width)
        self.set_map_height(self.map_height)
        self.redraw_front = True
        self.optimized_render = False
        
    def set_map_width(self,w) -> None:
        assert w >= 0 <= 120
        self.map_width = w
    
    def set_map_height(self,h) -> None:
        assert h >= 0 <= 120
        self.map_height = h
        
    def tick(self):
        self.update_time()
        if self.new_map:
            self.new_map = False
            self.init_active_map()
        self.cycle_reel(self.bg_tile_update_reel, self.bg_layer)
        self.cycle_reel(self.bldg_tile_update_reel, self.bldg_layer)
        self.game.player.tick()
        self.update_ambient()
        for item in self.items[self.current_map]:
            item.tick()
        for npc in self.npcs:
            npc.tick()
            
    def litterbug(self):
        for i in range(1000):
            x = random.randint(0,self.map_width*16)
            y = random.randint(0,self.map_height*16)
            item = Resource(self.game,random.choice(["wood","stone"]))
            item.create_at(x,y)
            
    def update_time(self):
        self.tick_time = self.tick_time + self.speed_factor
        if self.tick_time >= 360:
            self.tick_time = 0
            self.minute += 10
            self.game.ui.clock.trigger_update()            
            if self.minute >= 60:
                self.minute = 0
                self.hour += 1
                if self.hour > 23:
                    self.hour = 0
        self.darkening = True if self.hour >= 18 else False
    
    def update_ambient(self):
        r = self.outdoor_ambient[0]; g=self.outdoor_ambient[1]; b=self.outdoor_ambient[2]
        if self.darkening:
            r = min(180, r+(0.03*self.speed_factor))
            g = min(150, g+(0.03*self.speed_factor))
        self.outdoor_ambient = (r,g,b)
        
        if self.outdoors: self.ambient_light = self.outdoor_ambient
        
    
    def prerender(self, screen):
        self.top_left_x_last = self.top_left_x
        self.top_left_y_last = self.top_left_y
        self.top_left_x = min(max(self.game.player.x-screen.get_width()/2,0),self.map_width*16-screen.get_width())
        self.top_left_y = min(max(self.game.player.y-screen.get_height()/2,0),self.map_height*16-screen.get_height())
        
        self.optimized_render = False
        if self.top_left_x == self.top_left_x_last and self.top_left_y == self.top_left_y_last and not self.redraw_front:
            self.optimized_render = True
            
        # Centers the screen in the case of rooms smaller than the whole screen
        if self.top_left_x < 0: self.top_left_x = int(self.top_left_x/2)
        if self.top_left_y < 0: self.top_left_y = int(self.top_left_y/2)
        
        self.game.ambient_surface.fill((self.ambient_light[0],self.ambient_light[1],self.ambient_light[2],255))
        
    def render_back(self, screen):
        screen.blit(self.bg, (0,0), (self.top_left_x,self.top_left_y,screen.get_width(),screen.get_height()))
        
    def render_mid(self, screen):
        player = self.game.player
        screen.fill(pygame.Color(0,0,0,0))
        
        if self.redraw_objects:
            self.mid_object.fill(pygame.Color(0,0,0,0))
            self.front_object.fill(pygame.Color(0,0,0,0))
            for tiles in self.map_tiles[self.current_map]:
                tile = self.map_tiles[self.current_map][tiles]
                tile.render_object(self.mid_object, self.front_object)
            self.redraw_objects = False
        
        dest = (0,0)
        src = (self.top_left_x, 
               self.top_left_y, 
               screen.get_width(), 
               16*(((player.y - self.top_left_y)//16)+1)-self.top_left_y%16)  # Top 'half'
               
        screen.blit(self.mid_object, dest, src)
        screen.blit(self.mid, dest, src)
        
        for item in self.items[self.current_map]:
            item.render(screen)
        
        for npc in self.npcs:
            npc.render(screen)
        
        player.render(screen) 
        
        dest = (0, 16*(((player.y - self.top_left_y)//16)+1)-self.top_left_y%16)
        src = (self.top_left_x, 
               self.top_left_y+16*(((player.y - self.top_left_y)//16)+1)-self.top_left_y%16, 
               screen.get_width(), 
               screen.get_height()-(player.y - self.top_left_y)+8)   # bottom 'half'
        
        screen.blit(self.mid_object, dest, src)
        screen.blit(self.mid, dest, src)
        
        screen.blit(self.front_object, (0,0), (self.top_left_x,self.top_left_y,screen.get_width(),screen.get_height()))
        
    def render_front(self, screen):
        if self.optimized_render: return
        screen.fill(pygame.Color(0,0,0,0))
        if self.redraw_front:
            self.redraw_front = False
            for object in self.special_objects[self.current_map]:
                object.render_front(self.fg)
        screen.blit(self.fg, (0,0), (self.top_left_x,self.top_left_y,screen.get_width(),screen.get_height()))
        
    def render_scaled(self,screen):
        self.game.player.render_scaled(screen)
        
    def get_tile_x(self, tile_num):
        return tile_num % self.map_width
        
    def get_tile_y(self, tile_num):
        return int(tile_num / self.map_width)
        
    def get_tile_num(self, x, y):
        return y*self.map_width+x
        
    def get_tile_xy(self,tile_num):
        return (self.get_tile_x(tile_num), self.get_tile_y(tile_num))
        
    def is_movable(self,gx,gy):
        tile_num = self.get_tile_num(gx,gy)
        if gx >= self.map_width: return True
        if gy >= self.map_height: return True
        if gx < 1: return True
        if gy < 1: return True
        if tile_num > len(self.collision_map): return True
        tile = self.map_tiles[self.current_map][(gx, gy)]
        if tile.collision: return False
        return True
        
    def is_visible(self,x,y):
        if x < self.game.player.gx-self.game.config.base_display_tile_width - 2: return False
        if y < self.game.player.gy-self.game.config.base_display_tile_height - 4: return False
        if x > self.game.player.gx+self.game.config.base_display_tile_width + 2: return False
        if y > self.game.player.gy+self.game.config.base_display_tile_height + 4: return False
        return True
        
    def blit_tile(self, surface, layer, tile_num, x, y):
        new_tile = layer[tile_num]
        if not new_tile: return   
        if type(new_tile) == int:
            surface.blit(self.tileset[new_tile], (x*16, y*16))
        if type(new_tile) == list:
            surface.blit(self.tileset[new_tile[0][1]], (x*16, y*16))
    
    def update_tile(self, tile_num, layer):
        new_tile = layer[tile_num]
        x = self.get_tile_x(tile_num)
        y = self.get_tile_y(tile_num)
        
        if not self.is_visible(x,y): return
        
        # Render both layers to avoid lower-layer artifacts
        self.blit_tile(self.bg, self.bg_layer, tile_num, x, y)
        self.blit_tile(self.bg, self.bldg_layer, tile_num, x, y)
        
    def cycle_reel(self, reel, layer):
        tiles_to_update = reel.pop(0)
        reel.append([])
        for next_tile in tiles_to_update:
            last_frame = layer[next_tile].pop(0)
            delay = min(int((last_frame[0]*60)/1000),59)
            reel[delay] += [next_tile]  
            layer[next_tile].append(last_frame)
            self.update_tile(next_tile,layer)
            
    def warp_player(self, dest):
        new_map = dest[0]
        new_gx = dest[1]
        new_gy = dest[2]
        if self.init_map(new_map):
            self.game.player.set_gx(new_gx)
            self.game.player.set_gy(new_gy)
            
    def init_specials(self):
        if self.current_map not in self.special_objects:
            self.special_objects[self.current_map] = []
                       
            if self.current_map == "farm":
                self.special_objects[self.current_map].append(Farmhouse(self.game, self))
                
    def set_tile_neighbors(self, tile):
        gx = tile.gx
        gy = tile.gy
        map = self.map_tiles[self.current_map]
        key = (gx,gy+1)
        if key in map: tile.neighbors[0] = map[key]
        key = (gx+1,gy+1)
        if key in map: tile.neighbors[1] = map[key]
        key = (gx+1,gy)
        if key in map: tile.neighbors[2] = map[key]
        key = (gx+1,gy-1)
        if key in map: tile.neighbors[3] = map[key]
        key = (gx,gy-1)
        if key in map: tile.neighbors[4] = map[key]
        key = (gx-1,gy-1)
        if key in map: tile.neighbors[5] = map[key]
        key = (gx-1,gy)
        if key in map: tile.neighbors[6] = map[key]
        key = (gx-1,gy+1)
        if key in map: tile.neighbors[7] = map[key]
        
    def get_all_map_objects(self, map):
        objects = []
        for j in range(self.map_height):
            for i in range(self.map_width):
                key = (i,j)
                if key in self.map_tiles[self.current_map]: 
                    tile = self.map_tiles[self.current_map][key]
                    if tile.object:
                        objects.append(tile.object)
        return objects
        
class MapTile:
    def __init__(self, game, map, location):
        self.game = game
        self.world = self.game.world
        self.gx = location[0]
        self.gy = location[1]
        self.map = map
        self.collision = False
        self.spawnable = False
        self.diggable = False
        self.passable = False
        self.spawnable = False
        self.water = False
        self.dug = False
        self.watered = False
        self.type = 0
        self.init = False
        self.animated = False
        self.redraw = True
        self.crop = None
        self.object = None
        self.neighbors = [None for i in range(8)]
        
        self.bg_layer = None
        self.bldg_layer = None
        self.path_layer = None
        self.front_layer = None
        self.afront_layer = None
        
        self.bg_tile = None
        self.bldg_tile = None
        self.front_tile = None
        self.afront_tile = None
        
        rect = pygame.Rect(0, 0, 16, 16) 
        self.surface = pygame.Surface(rect.size).convert()
        self.surface.fill(pygame.Color(0,0,0,0))
        self.dig_tiles = self.game.sprite.get_tiles("hoeDirt")
        self.dig_tilenum = 0
        
    def init_second_stage(self):
        if self.init: return
        
        if self.bg_layer: self.bg_tile = self.world.tileset[self.bg_layer]
        if self.bldg_layer: self.bldg_tile = self.world.tileset[self.bldg_layer]
        if self.front_layer: self.front_tile = self.world.tileset[self.front_layer]
        if self.afront_layer: self.afront_tile = self.world.tileset[self.afront_layer]      
        
        if self.bg_layer in self.world.passable_tiles or self.bldg_layer in self.world.passable_tiles:
            self.passable = True
        if self.bg_layer in self.world.diggable_tiles or self.bldg_layer in self.world.diggable_tiles:
            self.diggable = True       
        if self.bldg_layer and not self.passable:
            self.collision = True
        
        if self.path_layer:
            if self.path_layer < 9: self.path_layer = 0
            paths_tile_base = self.world.tileset_index["paths"]
            type = self.path_layer-paths_tile_base         
            new_obj = MapObject(self.game,self.world,self,type,self.gx,self.gy)
            self.object = new_obj if type > 8 and type < 27 else None
        
        #Test dig
        if self.diggable:
            self.dug = True
           
        self.init = True
    
    def get_dig_grid(self):
        grid = []
        for neighbor in range(8):
            if self.neighbors[neighbor]:
                grid.append(True if self.neighbors[neighbor].dug else False)
            else:
                grid.append(False)
        return grid
        
    def compute_tilenum(self):
        dig_grid = self.get_dig_grid()
        if True not in dig_grid: return 0
        if dig_grid[0]: return 12
        return 0
    
    def update(self):
        self.dig_tilenum = self.compute_tilenum()
        self.render_tile()
        
    def render_tile(self):
        if self.map != self.world.current_map: return
        
        bg = self.world.bg
        mid_obj = self.world.mid_object
        front_obj = self.world.front_object
        mid = self.world.mid
        fg = self.world.fg
        
        bg.blit(self.surface, (0,0), (0,0,16,16))
        mid.blit(self.surface, (0,0), (0,0,16,16))
        fg.blit(self.surface, (0,0), (0,0,16,16))
        
        self.render_back(bg)
        self.render_object(mid_obj, front_obj)
        self.render_mid(mid)
        self.render_front(fg)
        
    def render_back(self, surface): 
        # This typically only happens once at map init
        if self.bg_tile:
            surface.blit(self.bg_tile, (self.gx*16,self.gy*16))
        if self.bldg_tile:
            surface.blit(self.bldg_tile, (self.gx*16,self.gy*16))      
        if self.dug:
            surface.blit(self.dig_tiles[self.dig_tilenum], (self.gx*16,self.gy*16))
            
    def render_object(self, mid, fg):
        if self.object:
            self.object.render_mid(mid)
            self.object.render_front(fg)
            
    def render_mid(self, mid):
        if self.front_tile:
            mid.blit(self.front_tile, (self.gx*16,self.gy*16))
            
    def render_front(self, surface):
        if self.afront_tile:
            surface.blit(self.afront_tile, (self.gx*16,self.gy*16))
            
    