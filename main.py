'''
The main application module.
'''
# pylint: disable=E1101
import sys
import random
import time
import pygame
from config import config
from creature_sprite import CritterSprite
from creature_sprite import UpdateMethod
from food_sprite import FoodSprite

pygame.init()
pygame.font.init()


log = config.logger
SPAWN_BUFFER = config.spawn_buffer_size

critters = pygame.sprite.Group()
foods = pygame.sprite.Group()

clock = pygame.time.Clock()
screen = pygame.display.set_mode((config.screen_width, config.screen_height),
                                  flags=pygame.HWSURFACE | pygame.DOUBLEBUF,
                                  vsync = 1)

def create_initial_food(count: int):
    '''
    Create initial food for the environment.
    '''
    for _ in range(count):
        x_pos = random.randint(0, config.screen_width)
        y_pos = random.randint(0, config.screen_height)
        food = FoodSprite(x_pos, y_pos)
        foods.add(food)

def get_initial_critter_values():
    '''
    Generates initial random values for critter attributes. This is only done
    once when the application starts. After this point, genes are used to 
    update critter attributes.
    '''
    energy = random.uniform(config.critter_min_energy, config.critter_max_energy)
    size = random.randint(config.critter_min_size, config.critter_max_size)
    speed = random.uniform(config.critter_min_speed, config.critter_max_speed)
    config.logger.debug(f"Energy: {energy} Size: {size} Speed: {speed}")
    return energy, size, speed
    
def create_initial_critters(count: int):
    '''
    Create initial critters for the environment.
    '''
    for _ in range(count):
        x_pos = random.randint((0 + SPAWN_BUFFER), (config.screen_width - SPAWN_BUFFER))
        y_pos = random.randint((0 + SPAWN_BUFFER), (config.screen_height- SPAWN_BUFFER))

        energy, size, speed = get_initial_critter_values()
        
        # Create genes based on these random attributes
        genes = {
            "size": (size - config.critter_min_size) / (config.critter_max_size - config.critter_min_size) * 2 - 1,
            "speed": (speed - config.critter_min_speed) / (config.critter_max_speed - config.critter_min_speed) * 2 - 1,
            "energy": (energy - config.critter_min_energy) / (config.critter_max_energy - config.critter_min_energy) * 2 - 1,
            # ... add other genes as required
        }

        config.logger.debug(f"Genes are: {genes}")

        critter = CritterSprite(x_pos, y_pos, genes)
        critters.add(critter)

def render_sidebar(scr):
    '''
    Creates an informational sidebar on the left hand side of the application screen.
    param scr: A reference to the main application screen.
    '''
    font = pygame.font.Font(None, 24)
    # Create a surface for the sidebar with the specified opacity
    sidebar_surface = pygame.Surface((config.sidebar_width, config.screen_height))
    sidebar_surface.set_alpha(config.sidebar_opacity)
    sidebar_surface.fill(config.sidebar_colour)

    # Draw the sidebar
    scr.blit(sidebar_surface, (0, 0))

    # Display the current number of critters
    critter_count_text = font.render(f"Critters: {len(critters)}", True, (255, 255, 255))
    scr.blit(critter_count_text, (10, 10))

def spawn_food(next_spawn, rate, count):
    '''
    Periodically spawns new food in the environment.
    '''
    # Check if it's time to spawn new food
    current_time = time.time()
    if current_time >= next_spawn:
        # Create new food items.
        create_initial_food(count)
        next_spawn = current_time + rate
    return next_spawn

RUNNING = True
create_initial_food(config.food_initial_count)
create_initial_critters(config.critter_initial_count)

next_food_spawn_time = time.time() + config.food_respawn_rate

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

    render_sidebar(screen)

    next_food_spawn_time = spawn_food(next_food_spawn_time,
                                      config.food_respawn_rate,
                                      config.food_respawn_count)

    clock.tick(120)
    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()
