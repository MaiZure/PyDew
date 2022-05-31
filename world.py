import random
import pygame

from mapobject import MapObject

class World:

    def __init__(self, game):
        print("Initializing World")
        self.game = game
        self.season = random.choice(["spring","summer","fall","winter"])
        
        self.map_layers = []
        self.tiles = []
        self.tiles_index = {}
        self.current_map = "" #town
        self.current_map_path_objects = []
        self.warp_points = {}
        self.action_points = {}
        self.paths_tile_base = 0
        self.animated_tiles = []
        self.passable_tiles = []
        self.impassable_tiles = []
        self.collision_map = []     # Basic Boolean collisions (Aligned with self.tiles)
        self.spawnable_map = []     
        
        self.bg_tile_update_reel = [[] for a in range(60)]   # Maintan 60 frames
        self.bldg_tile_update_reel = [[] for a in range(60)]
        
        # Map layers
        self.bg_layer = []
        self.bldg_layer = []
        self.path_layer = []
        self.front_layer = []
        self.always_front_layer = []
        
        self.map_width = 0 
        self.map_height = 0 
        
        self.init_map("forest")
        
    def init_map(self, map_name) -> bool:
        
        if not map_name in self.game.map.map:
            print("ERROR - Map doesn't exist yet ("+map_name+")")
            return False
            
        self.current_map = map_name
        self.new_map = True
        
        self.bg_tile_update_reel = [[] for a in range(60)]   # Maintan 60 frames
        self.bldg_tile_update_reel = [[] for a in range(60)]
        
        self.current_map_path_objects.clear()
        
        #TODO - Make these layer arrays
        self.bg_layer = self.game.map.get_layer_data(self.current_map,"Back")
        self.bldg_layer = self.game.map.get_layer_data(self.current_map,"Buildings")
        self.path_layer = self.game.map.get_layer_data(self.current_map,"Paths")
        self.front_layer = self.game.map.get_layer_data(self.current_map,"Front")
        self.always_front_layer = self.game.map.get_layer_data(self.current_map,"AlwaysFront")
        
        self.map_width = self.game.map.get_layer_width(self.current_map,0)
        self.map_height = self.game.map.get_layer_height(self.current_map,0)
        
        # Create background surface to render map
        rect = pygame.Rect(0, 0, self.map_width*16, self.map_height*16) 
        self.bg = pygame.Surface(rect.size).convert()
        self.fg = pygame.Surface(rect.size, pygame.SRCALPHA).convert_alpha()
        
        self.init_second_stage()
        return True
        
        
    def init_second_stage(self):
        self.tiles = self.game.map.get_map_tiles(self.current_map)
        self.tiles_index = self.game.map.get_map_tiles_index(self.current_map)
        self.generate_background_layers()
        self.generate_foreground_layers()
        self.animated_tiles = self.game.map.get_map_animations(self.current_map, self.tiles_index)
        self.passable_tiles, self.impassable_tiles = self.game.map.get_passable_tiles(self.current_map, self.tiles_index)
        self.warp_points = self.game.map.get_map_warps(self.current_map)
        self.action_points = self.game.map.get_map_actions(self.current_map)
        
        self.collision_map = self.generate_collision_map()
        for mapobject in self.current_map_path_objects:
            mapobject.init_second_stage()
        self.embed_map_animations(self.bg_layer, self.bg_tile_update_reel)
        self.embed_map_animations(self.bldg_layer, self.bldg_tile_update_reel)
        
        
        
    def set_random_season(self):
        self.season = random.choice(["spring","summer","fall","winter"])
        self.set_season()
        
    def generate_background_layers(self):
        for j in range(0,self.map_height):
            for i in range(0,self.map_width):
                bg_tile = self.bg_layer[j*self.map_width+i]
                bldg_tile = self.bldg_layer[j*self.map_width+i]
                if bg_tile:
                    if type(bg_tile) == int: # Just a tile number
                        self.bg.blit(self.tiles[bg_tile], (i*16,j*16))
                    if type(bg_tile) == list: # Animated - List of tuple frames (duration, tile number)
                        self.bg.blit(self.tiles[bg_tile[0][1]], (i*16,j*16))
                if bldg_tile:
                    if type(bldg_tile) == int:
                        self.bg.blit(self.tiles[bldg_tile], (i*16,j*16))
                    if type(bldg_tile) == list:
                        self.bg.blit(self.tiles[bg_tile[0][1]], (i*16,j*16))
                    
    def generate_foreground_layers(self):   ## Refactor this fxn somehow
        paths_tile_base = self.tiles_index["paths"]
        for j in range(0,self.map_height):
            for i in range(0,self.map_width):
                path_tile = self.path_layer[j*self.map_width+i]
                front_tile = self.front_layer[j*self.map_width+i]
                if self.always_front_layer:  # Because get_layer_data() returns None if no AlwaysFront layer exists
                    afront_tile = self.always_front_layer[j*self.map_width+i]   #self.always_front_layer could be None
                else:
                    afront_tile = None # to avoid error 7 lines below
                if path_tile: # My god clean this up
                    if path_tile-paths_tile_base < 9: # Delete pathing-related tiles (unused?)
                        self.path_layer[j*self.map_width+i] = 0
                    MapObject(self.game,self,path_tile-paths_tile_base,i,j)
                if front_tile: 
                    self.fg.blit(self.tiles[front_tile], (i*16,j*16))
                if afront_tile:
                    self.fg.blit(self.tiles[afront_tile], (i*16,j*16))
                    
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
        if location in self.action_points:
            #should probably story a type for various behaviors -- for now, warp only
            self.warp_player(self.action_points[location])
        else:
            print ("No action at " + str(location))
        
    def init_active_map(self):
        self.game.player.set_map_width(self.map_width)
        self.game.player.set_map_height(self.map_height)
        self.new_map = False
        
    def tick(self):
        if self.new_map:
            self.init_active_map()
        self.cycle_reel(self.bg_tile_update_reel, self.bg_layer)
        self.cycle_reel(self.bldg_tile_update_reel, self.bldg_layer)
        
        
    def render_back(self, screen):
        top_left_x = min(max(self.game.player.x-screen.get_width()/2,0),self.map_width*16-screen.get_width())
        top_left_y = min(max(self.game.player.y-screen.get_height()/2,0),self.map_height*16-screen.get_height())
        screen.blit(self.bg, (0,0), (top_left_x,top_left_y,screen.get_width(),screen.get_height()))
        
    def render_mid(self, screen):
        screen.fill(pygame.Color(0,0,0,0))
        for mapobject in self.current_map_path_objects:
            mapobject.render_mid(screen)
        self.game.player.render(screen)
        
    def render_front(self, screen):
        screen.fill(pygame.Color(0,0,0,0))
        top_left_x = min(max(self.game.player.x-screen.get_width()/2,0),self.map_width*16-screen.get_width())
        top_left_y = min(max(self.game.player.y-screen.get_height()/2,0),self.map_height*16-screen.get_height())       
        for mapobject in self.current_map_path_objects:
            mapobject.render_front(screen)
        screen.blit(self.fg, (0,0), (top_left_x,top_left_y,screen.get_width(),screen.get_height()))
        
        
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
        if tile_num > len(self.collision_map): return True
        if self.collision_map[tile_num]: return False
        return True
        
    def is_visible(self,x,y):
        if x < self.game.player.gx-self.game.config.base_display_tile_width - 2: return False
        if y < self.game.player.gy-self.game.config.base_display_tile_height - 4: return False
        if x > self.game.player.gx+self.game.config.base_display_tile_width + 2: return False
        if y > self.game.player.gy+self.game.config.base_display_tile_height + 4: return False
        return True
        
    def blit_tile(self, surface, layer, tile_num, x, y):
        new_tile = layer[tile_num]
        if type(new_tile) == int:
            surface.blit(self.tiles[new_tile], (x*16, y*16))
        if type(new_tile) == list:
            surface.blit(self.tiles[new_tile[0][1]], (x*16, y*16))
    
    def update_tile(self, tile_num, layer):
        new_tile = layer[tile_num]
        x = self.get_tile_x(tile_num)
        y = self.get_tile_y(tile_num)
        
        if not self.is_visible(x,y): return
        
        if layer == self.bg_layer:
            self.blit_tile(self.bg, self.bg_layer, tile_num, x, y)
        if layer == self.bldg_layer:
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
        #dest = self.warp_points[warp_point]
        new_map = dest[0]
        new_gx = dest[1]
        new_gy = dest[2]
        if self.init_map(new_map):
            self.game.player.set_gx(new_gx)
            self.game.player.set_gy(new_gy)
        
        
        