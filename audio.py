import pygame
import random

class Audio:
    def __init__(self, game):
        print("Initializing Audio")
        
    pygame.mixer.init()
    
    pygame.mixer.Sound((".\\Music\\animalstore.wav")).play()