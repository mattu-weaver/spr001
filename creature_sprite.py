"""
Sprite classes
"""

import random
import math
import enum
import pygame
from config import config


class UpdateMethod(enum.Enum):
    """
    An enum that defines the update method of a sprite.
    """

    SIMPLE = 1
    RANDOM = 2
    TOWARDS = 3


class CritterSprite(pygame.sprite.Sprite):
    """
    The CritterSprite class
    """

    died_of_old_age = 0
    died_of_no_energy = 0

    def __init__(self, x, y, genes):
        """
        Constructor for the DefaultSprite class.
        """
        super().__init__()
        self.age = 0
        self.dx = 0
        self.dy = 0
        self.genes = genes
        self.died_from_old_age = False
        self.died_no_energy = False
        self.last_mating_time = 0

        self.size = config.critter_min_size + (genes["size"] + 1) / 2 * (
            config.critter_max_size - config.critter_min_size
        )
        self.speed = config.critter_min_speed + (genes["speed"] + 1) / 2 * (
            config.critter_max_speed - config.critter_min_speed
        )
        self.energy = config.critter_min_energy + (genes["energy"] + 1) / 2 * (
            config.critter_max_energy - config.critter_min_energy
        )

        self.image = pygame.Surface((self.size, self.size))
        self.image.fill([0, 255, 0])
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.log = config.logger
        self.max_age = config.critter_max_age + random.randint(0, 1000)

        self.angle = random.uniform(0, 2 * math.pi)
        self.initial_energy = self.energy

    def handle_edge_collision(self):
        """
        Determines if a critter is at the edge of its environment. If it is, the critter's 
        direction is changed. When a critter reaches a wall, it is reflected at the same 
        angle as its angle of incidence.
        """
        if self.rect.y <= (0 - self.size // 2) or self.rect.y >= (
            config.screen_height - self.size // 2
        ):
            self.angle = -self.angle
        if self.rect.x <= (0 - self.size // 2) or self.rect.x >= (
            config.screen_width - self.size // 2
        ):
            self.angle = math.pi - self.angle

    def simple_update(self):
        """
        Simple motion, the critter is given a fixed speed and a random angle.
        """
        self.dx = self.speed * math.cos(self.angle)
        self.dy = self.speed * math.sin(self.angle)
        self.rect.x += self.dx
        self.rect.y += self.dy

    def get_colour(self):
        """
        Returns a colour for the sprite based on its amount of remaining energy.
        Sprites gradually change from blue to red as their energy depletes.
        """
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
        size_factor = (
            config.critter_size / self.size
        ) ** 0.5  # Use square root to reduce the impact
        self.energy -= rate * size_factor

    def check_food_collision(self, food_sprites):
        """
        Checks for collision with food and increases energy accordingly.
        @param self A reference to this class.
        @param food_sprites The group of all existing food sprites.
        """
        collided_food = pygame.sprite.spritecollideany(self, food_sprites)
        if collided_food:
            energy_gain = collided_food.get_energy_value()
            self.energy = min(self.energy + energy_gain, config.critter_max_energy)
            collided_food.kill()

    def identify_mates(self, critters, current_update):
        if (current_update - self.last_mating_time) >= config.critter_mating_cooldown:
            if self.energy > config.critter_min_mating_energy:
                for other_critter in critters:
                    if other_critter != self:
                        if other_critter.energy > config.critter_min_mating_energy:
                            distance = math.dist((self.rect.x, self.rect.y), (other_critter.rect.x, other_critter.rect.y))
                            if distance <= config.critter_mating_distance:
                                # Mating can occur!
                                self.log.debug("Mating is taking place!")
                                self.last_mating_time = current_update
                                other_critter.last_mating_time = current_update
                                break


    def update(self, method: UpdateMethod, food_sprites, critters, update_count):
        """
        Updates a sprite before redrawing (overrides base function).
        """
        match method:
            case UpdateMethod.SIMPLE:
                self.simple_update()

        self.deplete_energy()
        self.handle_edge_collision()
        self.check_food_collision(food_sprites)

        self.identify_mates(critters, update_count)

        self.age += 1

        if config.critter_can_die_of_old_age:
            if self.age >= self.max_age:
                self.died_from_old_age = True
                CritterSprite.died_of_old_age += 1
                self.kill()

        if self.energy < 0.0:
            self.died_no_energy = True
            CritterSprite.died_of_no_energy += 1
            self.kill()

        c = self.get_colour()
        self.image.fill(c)  # Ensure energy_percent is not negative

    def draw(self):
        """
        Draws a sprite on the screen (overrides base function).
        """
        self.screen.blit(self.image, self.rect)
