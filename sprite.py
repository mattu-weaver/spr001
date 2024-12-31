'''
Sprite classes
'''
import random
import math
import enum
import pygame
from config import config

class UpdateMethod(enum.Enum):
    '''
    An enum that defines the update method of a sprite.
    '''
    SIMPLE = 1
    RANDOM = 2
    TOWARDS = 3

class DefaultSprite(pygame.sprite.Sprite):
    '''
    The DefaultSprite class 
    '''
    def __init__(self, x, y):
        '''
        Constructor for the DefaultSprite class.
        '''
        super().__init__()
        self.dx = 0
        self.dy = 0
        self.size = config.sprite_size
        self.image = pygame.Surface((self.size, self.size))
        self.image.fill([0, 255, 0])
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.log = config.logger

        self.base_speed = config.sprite_base_speed
        self.min_speed = config.sprite_min_speed
        self.max_speed = config.sprite_max_speed
        self.speed = self.get_speed()

        self.angle = random.uniform(0, 2 * math.pi)
        energy = config.sprite_energy
        self.energy = energy

        self.initial_energy = energy


    def handle_edge_collision(self):
        if self.rect.y <= (0 - self.size // 2) or self.rect.y >= (config.screen_height - self.size // 2):
            self.angle = -self.angle
        if self.rect.x <= (0  - self.size // 2) or self.rect.x >= (config.screen_width - self.size // 2):
            self.angle = math.pi - self.angle

    def simple_update(self):
        '''
        Simple motion, sprite is given a fixed speed and a random angle.
        '''
        self.dx = self.speed * math.cos(self.angle)
        self.dy = self.speed * math.sin(self.angle)
        self.rect.x += self.dx
        self.rect.y += self.dy

    def get_colour(self):
        energy_percent = self.energy / self.initial_energy

        if energy_percent < 0:
            energy_percent = 0

        red = int(255 * (1 - energy_percent))
        blue = int (255 - 255 * (1 - energy_percent))

        return (red, 0, blue)

    def deplete_energy(self):
        rate = self.speed * self.size * config.sprite_energy_scale      
        #rate = self.speed * pow(self.size, 2) * config.sprite_energy_scale
        self.energy -= rate
        pass

    def update(self, method: UpdateMethod):
        '''
        Updates a sprite before redrawing (overrides base function).
        '''
        match method:
            case UpdateMethod.SIMPLE:
                self.simple_update()

        self.deplete_energy()
        self.handle_edge_collision()

        if self.energy < 0.0:
            self.kill()

        c = self.get_colour()
        self.image.fill(c)  # Ensure energy_percent is not negative

    def get_speed(self):
        scaling_factor = 1 / math.log(self.size + 2)  # Adjust the "+ 2" to control the scaling curve

        # Calculate the scaled speed
        scaled_speed = self.base_speed * scaling_factor

        return max(self.min_speed, min(scaled_speed, self.max_speed))

    def draw(self):
        '''
        Draws a sprite on the screen (overrides base function).
        '''
        self.screen.blit(self.image, self.rect)
