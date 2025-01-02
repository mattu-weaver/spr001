'''
The main application module.
'''
# pylint: disable=E1101
import sys
import random
import time
import pygame
from config import config
from creature_sprite import CreatureSprite
from creature_sprite import UpdateMethod
from food_sprite import FoodSprite

log = config.logger
critters = pygame.sprite.Group()
foods = pygame.sprite.Group()
SPAWN_BUFFER = 50

clock = pygame.time.Clock()
screen = pygame.display.set_mode((config.screen_width, config.screen_height),
                                  flags=pygame.HWSURFACE | pygame.DOUBLEBUF,
                                  vsync = 1)


def create_food(count: int):
    '''
    Create a group of food sprites.
    '''
    for _ in range(count):
        x_pos = random.randint(0, config.screen_width)
        y_pos = random.randint(0, config.screen_height)
        food = FoodSprite(x_pos, y_pos)
        foods.add(food)

def create_critters(count: int):
    '''
    Create a group of sprites.
    '''
    for _ in range(count):
        x_pos = random.randint((0 + SPAWN_BUFFER), (config.screen_width - SPAWN_BUFFER))
        y_pos = random.randint((0 + SPAWN_BUFFER), (config.screen_height- SPAWN_BUFFER))

        critter = CreatureSprite(x_pos, y_pos)
        critters.add(critter)

RUNNING = True
create_food(10)
create_critters(10)

food_spawn_counter = 0
next_food_spawn_time = time.time() + 1

while RUNNING:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            RUNNING = False
        elif event.type == pygame.KEYDOWN:
            KEY_PRESSED = True

    # Fill the screen with a color (RGB)
    screen.fill(config.screen_back_colour)

    foods.update()
    foods.draw(screen)

    critters.update(UpdateMethod.SIMPLE, foods)
    critters.draw(screen)

    # Check if it's time to spawn new food
    current_time = time.time()
    if current_time >= next_food_spawn_time:
        config.logger.debug(f"Food created!")
        create_food(3)
        next_food_spawn_time = current_time + 1  # Reset the timer


    clock.tick(120)
    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()
