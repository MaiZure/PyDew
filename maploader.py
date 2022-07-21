import pygame, json, zlib, base64, os

class MapLoader:
    def __init__(self, game):
        print("Initializing Maps")
        
        # Load all maps in to a library (dictionary)
        self.map = {}        
        self.game = game
        
    def init_second_stage(self):
        self.load_maps()
        
    def load_maps(self) -> None:
        path = ".\\Maps\\"
        files = os.listdir(path)
        for file in files:
            name = ((file.split("."))[0]).lower()
            self.map[name] = json.load(open(path+file))
        
    def get_layer_data(self, map_name, layer_name) -> list:
        for layer in self.map[map_name]["layers"]:
            if layer["name"] == layer_name and "data" in layer:
                encoded_data = layer["data"]
                decoded_data = base64.b64decode(encoded_data)
                raw_data = zlib.decompress(decoded_data)
                return self.parse_raw_map(raw_data)
        print ("ERROR! Looing for " + layer_name + " in " + map_name)
            
    def parse_raw_map(self, raw_data) -> list:
        layer = []
        c = 0
        for byte in raw_data:
            if c == 0: num = byte
            if c == 1: num += byte*256
            if c == 3:
                layer.append(num)
                c = 0
            else:
                c += 1           
        return layer
        
    def get_layer_width(self, name, num) -> int:
        assert num >= 0 and num <= 4
        return self.map[name]["layers"][num*2]["width"]
        
    def get_layer_height(self, name, num) -> int:
        assert num >= 0 and num <= 4
        return self.map[name]["layers"][num*2]["height"]
        
    def get_tileset_names(self, name) -> list:
        names = []
        for tileset in self.map[name]["tilesets"]:
            tileset_name = (tileset["image"].split("/")).pop()
            tileset_name = tileset_name.split(".")[0]
            names.append(tileset_name)
        return names
        
    def get_map_tiles(self, name) -> list:
        tiles = [None]
        tilesets = self.get_tileset_names(name)
        for tileset in tilesets:
            tiles += self.game.sprite.get_tiles(tileset)
        return tiles
        
    def get_map_warps(self,name) -> dict:
        warps = {}  # nested tuple ( (gx,gy), (newmap, gx, gy) )
        for map_properties in self.map[name]["properties"]:
            if map_properties["name"] == "Warp":
                warp_data = map_properties["value"].split()
                while warp_data:
                    warp_gx = int(warp_data.pop(0))
                    warp_gy = int(warp_data.pop(0))
                    warp_dest = warp_data.pop(0)
                    warp_dest_gx = int(warp_data.pop(0))
                    warp_dest_gy = int(warp_data.pop(0))
                    warps[(warp_gx, warp_gy)] = (warp_dest.lower(), warp_dest_gx, warp_dest_gy)
        return warps
        
    def get_map_warpactions(self,map_name) -> dict:
        warps = {}  # nested tuple ( (gx,gy), (newmap, gx, gy) )
        for layer in self.map[map_name]["layers"]:
            if layer["name"] == "Buildings" and "objects" in layer:
                for object in layer["objects"]:
                    if "properties" in object:
                        for property in object["properties"]:   #TODO - Generalize this to load ALL actions
                            if property["name"] == "Action":
                                warp_data = property["value"].split()
                                if warp_data[0] == "Warp" or warp_data[0] == "LockedDoorWarp":
                                    warp_gx = int(int(object["x"])/16)
                                    warp_gy = int(int(object["y"])/16)
                                    action_type = (warp_data.pop(0)).lower()
                                    warp_dest_gx = int(warp_data.pop(0))
                                    warp_dest_gy = int(warp_data.pop(0))
                                    map_name = (warp_data.pop(0)).lower()
                                    if action_type == "lockeddoorwarp":
                                        start_time = int(warp_data.pop(0))
                                        end_time = int(warp_data.pop(0))
                                        ## Add relatonship requierments
                                        warps[(warp_gx, warp_gy)] = (map_name, warp_dest_gx, warp_dest_gy)
        return warps
        
    def get_map_actions(self, map_name) -> dict:
        actions = {}  # nested tuple ( (gx,gy), (newmap, gx, gy) )
        for layer in self.map[map_name]["layers"]:
            if layer["name"] == "Buildings" and "objects" in layer:
                for object in layer["objects"]:
                    if "properties" in object:
                        for property in object["properties"]:   #TODO - Generalize this to load ALL actions
                            if property["name"] == "Action":
                                action_data = property["value"].split()
                                action_gx = int(int(object["x"])/16)
                                action_gy = int(int(object["y"])/16)
                                actions[(action_gx,action_gy)] = action_data
        return actions
                                
        
    def get_map_tiles_index(self, name) -> list:
        index = {"paths": -1}
        tilesets = self.get_tileset_names(name)
        tiles = [None]
        for tileset in tilesets:
            index[tileset] = len(tiles)
            tiles += self.game.sprite.get_tiles(tileset)
        return index
        
    def get_map_outdoors(self, name) -> bool:
        outdoors = False  
        for map_properties in self.map[name]["properties"]:
            if map_properties["name"].lower() == "outdoors":
                if map_properties["value"] == True:
                    outdoors = True
                elif map_properties["value"].lower() == "t":
                    # Crash bug still exists here if property is boolean False
                    outdoors = True
        return outdoors
                    
    def get_ambient_light(self, name) -> bool:
        outdoors = False  # nested tuple ( (gx,gy), (newmap, gx, gy) )
        light_cut_factor = 3
        for map_properties in self.map[name]["properties"]:
            if map_properties["name"].lower() == "ambientlight":
                light = map_properties["value"].split()
                r = int(int(light[0])/2)
                g = int(int(light[1])/2)
                b = int(int(light[2])/2)
                return (r,g,b)
        # No given light indoors so return default
        return ((int(95/light_cut_factor),int(95/light_cut_factor),int(95/light_cut_factor)))
        
    def get_map_animations(self, name, tiles_index) -> list: 
        animated_tiles = []
        for tileset in self.map[name]["tilesets"]:
            tileset_name = (tileset["image"].split("/")).pop()
            tileset_name = tileset_name.split(".")[0]
            tile_offset = tiles_index[tileset_name]
            if "tiles" in tileset:
                for tile in tileset["tiles"]:
                    if "animation" in tile.keys():
                        alist = []
                        for atile in tile["animation"]:
                            alist.append((atile["duration"],atile["tileid"]+tile_offset))
                        animated_tiles.append(alist)
        return animated_tiles
        
    def get_passable_tiles(self, name, tiles_index):
        passable_tiles = []
        impassable_tiles = []
        
        for tileset in self.map[name]["tilesets"]:
            tileset_name = (tileset["image"].split("/")).pop()
            tileset_name = tileset_name.split(".")[0]
            tile_offset = tiles_index[tileset_name]
            if "tiles" in tileset:
                for tile in tileset["tiles"]:
                    tile_id = tile["id"]
                    if "properties" in tile:
                        for property in tile["properties"]:
                            if property["name"] == "Passable" or property["name"] == "Shadow":
                                if property["value"] == "T" or property["value"] == "t":
                                    passable_tiles.append(tile_id+tile_offset)
                                if property["value"] == "F" or property["value"] == "f":
                                    impassable_tiles.append(tile_id+tile_offset) 
        return passable_tiles, impassable_tiles
        
   