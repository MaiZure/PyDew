import pygame, json, zlib, base64

class MapLoader:
    def __init__(self, game):
        print("Initializing Maps")
        
        # Load all maps in to a library (dictionary)
        self.map = {}        
        self.load_maps()
        self.game = game
        
    def load_maps(self) -> None:
        self.map["forest"] = json.load(open("forest.tmj"))
        self.map["farm"] = json.load(open("farm.tmj"))
        self.map["town"] = json.load(open("town.tmj"))
        self.map["busstop"] = json.load(open("busstop.tmj"))
        self.map["mountain"] = json.load(open("mountain.tmj"))
        self.map["backwoods"] = json.load(open("backwoods.tmj"))
        self.map["beach"] = json.load(open("beach.tmj"))
        self.map["railroad"] = json.load(open("railroad.tmj"))
        
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
            names.append(tileset["image"])
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
        
    def get_map_tiles_index(self, name) -> list:
        index = {}
        tilesets = self.get_tileset_names(name)
        tiles = [None]
        for tileset in tilesets:
            index[tileset] = len(tiles)
            tiles += self.game.sprite.get_tiles(tileset)
        return index
        
    def get_map_animations(self, name, tiles_index) -> list: 
        animated_tiles = []
        for tileset in self.map[name]["tilesets"]:
            tileset_name = tileset["image"]
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
            tileset_name = tileset["image"]
            tile_offset = tiles_index[tileset_name]
            if "tiles" in tileset:
                for tile in tileset["tiles"]:
                    tile_id = tile["id"]
                    if "properties" in tile:
                        for property in tile["properties"]:
                            if property["name"] == "Passable":
                                if property["value"] == "T" or property["value"] == "t":
                                    passable_tiles.append(tile_id+tile_offset)
                                if property["value"] == "F" or property["value"] == "f":
                                    impassable_tiles.append(tile_id+tile_offset) 
        return passable_tiles, impassable_tiles
        
   