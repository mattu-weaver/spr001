'''
Sprite classes
'''
import random
import math
import enum
import pygame
from config import config


class FoodSprite(pygame.sprite.Sprite):
    '''
    The FoodSprite class 
    '''
    def __init__(self, x, y):
        '''
        Constructor for the FoodSprite class.
        '''
        super().__init__()
        self.size = config.sprite_size
        self.image = pygame.Surface((self.size, self.size))
        self.image.fill([0, 255, 0])
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.log = config.logger
        self.next_update_time = 0
        
    def draw(self):
        '''
        Draws a sprite on the screen (overrides base function).
        '''
        self.screen.blit(self.image, self.rect)

    def get_energy_value(self):
        '''
        Returns the energy value of the food based on its size.
        '''
        return math.pow(self.size, 2) * config.food_energy_scale



    def update(self):
        '''
        Updates the food group, including respawning food.
        '''
        self.image.fill((0, 255, 0))

