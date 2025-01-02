"""
The main application module.
"""

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

critters_group = pygame.sprite.Group()
food_group = pygame.sprite.Group()

clock = pygame.time.Clock()
screen = pygame.display.set_mode(
    (config.screen_width, config.screen_height),
    flags=pygame.HWSURFACE | pygame.DOUBLEBUF,
    vsync=1,
)


def create_initial_food(count: int):
    """
    Create initial food for the environment. Count number of food items are created
    at random positions and with a constrained random size. All food items exist in
    the food_group.
    This is only done once when the application starts. New food is created with
    the spawn food function.
    """
    for _ in range(count):
        x_pos = random.randint(0, config.screen_width)
        y_pos = random.randint(0, config.screen_height)
        food = FoodSprite(x_pos, y_pos)
        food_group.add(food)


def get_initial_critter_values():
    """
    Generates initial random values for critter attributes. This is only done
    once when the application starts. After this point, genes are used to
    update critter attributes.
    """
    energy = random.uniform(config.critter_min_energy, config.critter_max_energy)
    size = random.randint(config.critter_min_size, config.critter_max_size)
    speed = random.uniform(config.critter_min_speed, config.critter_max_speed)
    config.logger.debug(f"Energy: {energy} Size: {size} Speed: {speed}")
    return energy, size, speed


def create_initial_critters(count: int):
    """
    Create initial critters for the environment. This is only done once when the
    application starts. After this, critters can die from zero energy or old age.
    New critters are created through mating.
    """
    for _ in range(count):
        x_pos = random.randint((0 + SPAWN_BUFFER), (config.screen_width - SPAWN_BUFFER))
        y_pos = random.randint(
            (0 + SPAWN_BUFFER), (config.screen_height - SPAWN_BUFFER)
        )

        energy, size, speed = get_initial_critter_values()

        # Create genes based on the initial critter values that are generated above.
        genes = {
            "size": (size - config.critter_min_size)
            / (config.critter_max_size - config.critter_min_size)
            * 2
            - 1,
            "speed": (speed - config.critter_min_speed)
            / (config.critter_max_speed - config.critter_min_speed)
            * 2
            - 1,
            "energy": (energy - config.critter_min_energy)
            / (config.critter_max_energy - config.critter_min_energy)
            * 2
            - 1,
            # ... add other genes as required
        }

        config.logger.debug(f"Genes are: {genes}")

        critter = CritterSprite(x_pos, y_pos, genes)
        critters_group.add(critter)


def render_text(scr, text, values, text_line):
    """
    Displays text in the application sidebar.
    @param scr A reference to the main application screen.
    @param text The text to be displayed (including placeholders).
    @param values The values to populate placeholders in the text.
    @param text_line The line on which to display the text.
    """
    font = pygame.font.Font(None, 24)
    line_pos = text_line * 30 + 70
    formatted_text = text.format(**values)
    rendered_text = font.render(formatted_text, True, (255, 255, 255))
    scr.blit(rendered_text, (10, line_pos))


def render_sidebar(scr):
    """
    Creates an informational sidebar on the left hand side of the application screen.
    @param scr A reference to the main application screen.
    """
    # Draw the sidebar
    sidebar_surface = pygame.Surface((config.sidebar_width, config.screen_height))
    sidebar_surface.set_alpha(config.sidebar_opacity)
    sidebar_surface.fill(config.sidebar_colour)
    scr.blit(sidebar_surface, (0, 0))

    render_text(
        scr, "Current critter count: {count}", {"count": len(critters_group)}, 1
    )

    total_age = sum(critter.age for critter in critters_group)
    average_age = total_age / len(critters_group) #if critters_group else 0
    render_text(
        scr, "Average critter's age: {average_age}", {"average_age": average_age}, 2
    )

    oldest_critter = max(critters_group, key=lambda critter: critter.age, default=None)
    oldest_age = oldest_critter.age #if oldest_critter else 0
    render_text(scr, "Oldest critter's age: {oldest}", {"oldest": oldest_age}, 3)

    render_text(
        scr,
        "Critters died from no energy: {died_energy}",
        {"died_energy": CritterSprite.died_of_no_energy},
        4,
    )

    render_text(
        scr,
        "Critters died from old age: {died_old}",
        {"died_old": CritterSprite.died_of_old_age},
        5,
    )


def spawn_food(next_spawn, rate, count):
    """
    Periodically spawns new food in the environment - this simulates the growth of new plants
    that critters can then consume.
    @param next_spawn The time until food is next spawned.
    @param rate The interval between spawning food.
    @param count The number of food items to spawn.
    """
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

    food_group.update()
    food_group.draw(screen)

    critters_group.update(UpdateMethod.SIMPLE, food_group)
    critters_group.draw(screen)

    render_sidebar(screen)

    next_food_spawn_time = spawn_food(
        next_food_spawn_time, config.food_respawn_rate, config.food_respawn_count
    )

    clock.tick(120)
    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()
