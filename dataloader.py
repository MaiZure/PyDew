import pygame, json, zlib, base64, os
import random

class DataLoader:
    def __init__(self, game):
        print("Initializing Data")
        
        # Load all maps in to a library (dictionary)
        self.file = {}        
        self.game = game
        self.items = {}
        self.weapons = {}
        self.crops = {}
        
    def init_second_stage(self):
        self.load_data()
        self.parse_object_data()
        
    def load_data(self) -> None:
        path = ".\\Data\\"
        files = os.listdir(path)
        for file in files:
            name = ((file.split("."))[0]).lower()
            self.file[name] = json.load(open(path+file))
            
    def get_object_by_num(self,num):
        return self.items[num]
        
    def get_object_by_name(self,name):
        return self.items[name]
        
    def get_weapon_by_num(self,num):
        return self.weapons[num]
        
    def get_weapon_by_name(self,name):
        return self.weapons[name]
        
    def get_random_object(self):
        dict = self.file["objectinformation"]["content"]
        choice = random.choice(list(dict))
        result = dict[choice]
        result = choice+"/"+result
        return result
        
    def get_random_seed(self):
        dict = self.file["objectinformation"]["content"]
        choice = random.choice(list(self.crops.values()))[0]
        result = dict[choice]
        result = choice+"/"+result
        return result
        
    def get_random_weapon(self):
        dict = self.file["weapons"]["content"]
        choice = random.choice(list(dict))
        result = dict[choice]
        result = choice+"/"+result
        return result
        
    def parse_object_data(self):
        self.items = self.build_lookup_dict(self.file["objectinformation"]["content"])
        self.weapons = self.build_lookup_dict(self.file["weapons"]["content"])
        self.crops = self.build_lookup_dict(self.file["crops"]["content"])
            
    def build_lookup_dict(self, dict):
        output = {}
        for key in dict:
            data = dict[key]
            result = key+"/"+data
            datalist = result.split('/')
            output[int(key)] = datalist
            output[key] = datalist
            output[datalist[1].lower()] = datalist
            output[datalist[1]] = datalist
        return output