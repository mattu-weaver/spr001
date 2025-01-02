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

class CreatureSprite(pygame.sprite.Sprite):
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
        self.size = config.critter_size
        self.image = pygame.Surface((self.size, self.size))
        self.image.fill([0, 255, 0])
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.log = config.logger

        self.base_speed = config.critter_base_speed
        self.min_speed = config.critter_min_speed
        self.max_speed = config.critter_max_speed
        self.speed = self.get_speed()

        self.angle = random.uniform(0, 2 * math.pi)
        energy = config.critter_energy
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
        '''
        Returns a colour for the sprite based on its amount of remaining energy.
        Sprites gradually change from blue to red and their energy depletes.
        '''
        energy_percent = max(self.energy / self.initial_energy, 0)

        red = int(255 * (1 - energy_percent))
        blue = int(255 * energy_percent)

        # Ensure RGB values are within the valid range
        red = max(0, min(red, 255))
        blue = max(0, min(blue, 255))

        return (red, 0, blue)

    def deplete_energy(self):
        # Adjust the rate to make smaller critters lose energy at a balanced rate
        rate = self.speed * self.size * config.critter_energy_scale
        size_factor = (config.critter_size / self.size) ** 0.5  # Use square root to reduce the impact
        self.energy -= rate * size_factor

    def check_food_collision(self, food_sprites):
        '''
        Checks for collision with food and increases energy accordingly.
        '''
        collided_food = pygame.sprite.spritecollideany(self, food_sprites)
        if collided_food:
            energy_gain = collided_food.get_energy_value()
            self.energy = min(self.energy + energy_gain, config.critter_max_energy)
            collided_food.kill()

    def update(self, method: UpdateMethod, food_sprites):
        '''
        Updates a sprite before redrawing (overrides base function).
        '''
        match method:
            case UpdateMethod.SIMPLE:
                self.simple_update()

        self.deplete_energy()
        self.handle_edge_collision()
        self.check_food_collision(food_sprites)

        if self.energy < 0.0:
            self.kill()

        c = self.get_colour()
        self.image.fill(c)  # Ensure energy_percent is not negative

    def get_speed(self):
        scaling_factor = 1 / math.log(self.size + 10)  # Adjust the "+ 2" to control the scaling curve

        self.log.debug(f"Speed scaling factor is {scaling_factor}, size is {self.size}")

        # Calculate the scaled speed
        scaled_speed = self.base_speed * scaling_factor

        return max(self.min_speed, min(scaled_speed, self.max_speed))

    def draw(self):
        '''
        Draws a sprite on the screen (overrides base function).
        '''
        self.screen.blit(self.image, self.rect)
