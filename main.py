'''
The main application module.
'''
# pylint: disable=E1101
import sys
import random
import pygame
from config import config
from sprite import DefaultSprite
from sprite import UpdateMethod

log = config.logger
critters = pygame.sprite.Group()
SPAWN_BUFFER = 50

clock = pygame.time.Clock()
screen = pygame.display.set_mode((config.screen_width, config.screen_height),
                                  flags=pygame.HWSURFACE | pygame.DOUBLEBUF,
                                  vsync = 1)

def create_sprites(count: int):
    '''
    Create a group of sprites.
    '''
    for _ in range(count):
        x_pos = random.randint((0 + SPAWN_BUFFER), (config.screen_width - SPAWN_BUFFER))
        y_pos = random.randint((0 + SPAWN_BUFFER), (config.screen_height- SPAWN_BUFFER))

        sq1 = DefaultSprite(x_pos, y_pos)
        critters.add(sq1)

RUNNING = True
create_sprites(50000)

while RUNNING:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            RUNNING = False
        elif event.type == pygame.KEYDOWN:
            KEY_PRESSED = True

    # Fill the screen with a color (RGB)
    screen.fill(config.screen_back_colour)

    critters.update(UpdateMethod.SIMPLE)
    critters.draw(screen)

    clock.tick(120)
    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()
