import pygame, json, zlib, base64

class MapLoader:
    def __init__(self):
        print("Initializing Maps")
        
        # Load all maps in to a library (dictionary)
        self.map = {}        
        self.load_maps()
        
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