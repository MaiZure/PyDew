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
        
    def get_layer_map(self, name, num) -> list:
        encoded_data = self.map[name]["layers"][num*2]["data"]
        decoded_data = base64.b64decode(encoded_data)
        raw_data = zlib.decompress(decoded_data)
        return self.parse_raw_map(raw_data)
        
    def parse_raw_map(self, raw_data) -> list:
        layer = []
        c = 0
        for byte in raw_data:
            if c == 0: num = byte
            if c == 1: num += byte*256
            if c is 3:
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
        
    def get_map_animations(self, name): #Only works for first/main tileset for now
        animated_tiles = []
        for tile in self.game.map.map[name]["tilesets"][0]["tiles"]:
            if "animation" in tile.keys():
                alist = []
                for atile in tile["animation"]:
                    alist.append((atile["duration"],atile["tileid"]+1))
                animated_tiles.append(alist)
        return animated_tiles
        
    def get_passable_tiles(self, name): # Only works for first/main tilset for now
        passable_tiles = []
        impassable_tiles = []
        #return
        for tile in self.game.map.map[name]["tilesets"][0]["tiles"]:
            tile_id = tile["id"]
            if "properties" in tile.keys():
                for property in tile["properties"]:
                    if property["name"] == "Passable":
                        if property["value"] == "T" or property["value"] == "t":
                            passable_tiles.append(tile_id+1)
                        if property["value"] == "F" or property["value"] == "f":
                            impassable_tiles.append(tile_id+1) 
        return passable_tiles, impassable_tiles
        
   