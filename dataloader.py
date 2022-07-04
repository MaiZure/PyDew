import pygame, json, zlib, base64, os
import random

class DataLoader:
    def __init__(self, game):
        print("Initializing Data")
        
        # Load all maps in to a library (dictionary)
        self.file = {}        
        self.game = game
        
    def init_second_stage(self):
        self.load_data()
        
    def load_data(self) -> None:
        path = ".\\Data\\"
        files = os.listdir(path)
        for file in files:
            name = ((file.split("."))[0]).lower()
            self.file[name] = json.load(open(path+file))
            
    def get_object_by_num(self,num):
        dict = self.file["objectinformation"]["content"]
        result = dict[str(num)]
        result = str(num)+"/"+result
        return result
        
    def get_random_object(self):
        dict = self.file["objectinformation"]["content"]
        choice = random.choice(list(dict))
        result = dict[choice]
        result = choice+"/"+result
        return result
        
    def get_random_weapon(self):
        dict = self.file["weapons"]["content"]
        choice = random.choice(list(dict))
        result = dict[choice]
        result = choice+"/"+result
        return result
    