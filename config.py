'''
Global Configuration module for use by various application files. 
'''
import toml
import random
from loguru import logger

class Config:
    '''
    The Config class can be used globally to expose configuration parameters.
    All parameters are read only and may be changed in the config.toml file prior to execution.
    '''
    def __init__(self):
        '''
        Constructor for the Config class.
        Assumes there is a config.toml file in the same directory as this file.
        '''
        self._config = toml.load("config.toml")
        logger.add("debug.log",
                   format="{time:DD/MM/YYYY HH:mm:ss} {level} {function} {line} {message}",
                   rotation="50 MB",
                   level=self.logging_level)
        self._logger = logger


    @property
    def sidebar_width(self) -> int:
        '''
        Read-only: Returns the width of the sidebar from the application config file.
        '''
        return int(self._config['screen']['sidebar_width'])

    @property
    def sidebar_opacity(self) -> int:
        '''
        Read-only: Returns the width of the sidebar from the application config file.
        '''
        return int(self._config['screen']['sidebar_opacity'])

    @property
    def sidebar_colour(self) -> tuple:
        '''
        Read-only: Returns the opacity for the sidebar.
        '''
        return tuple(self._config['screen']['sidebar_colour'])


    @property
    def logger(self):
        '''
        Read-only: Returns a logger object.
        '''
        return self._logger

    @property
    def screen_width(self) -> int:
        '''
        Read-only: Returns the screen width from the application config file.
        '''
        return int(self._config['screen']['width'])

    @property
    def spawn_buffer_size(self) -> int:
        '''
        Read-only: Returns the spawn buffer size.
        '''
        return int(self._config['screen']['spawn_buffer'])

    @property
    def screen_height(self) -> int:
        '''
        Read-only: Returns the screen height from the application config file.
        '''
        return int(self._config['screen']['height'])

    @property
    def screen_title(self) -> str:
        '''
        Read-only: Returns the screen title from the application config file.
        '''
        return str(self._config['screen']['title'])

    @property
    def screen_back_colour(self) -> tuple:
        '''
        Read-only: Returns the default background colour for the screen.
        '''
        return tuple(self._config['screen']['back_colour'])

    @property
    def logging_level(self) -> str:
        '''
        Read-only: Returns the logging level that loguru will use.
        '''
        return str(self._config['loguru']['level'])

    @property
    def critter_fixed_size(self) -> int:
        '''
        Read-only: Returns the fixed size of a critter.
        '''
        return int(self._config['critter']['fixed_size'])

    @property
    def critter_initial_count(self) -> int:
        '''
        Read-only: Returns the initial number of critters.
        '''
        return int(self._config['critter']['initial_count'])

    @property
    def critter_min_energy(self) -> float:
        '''
        Read-only: Returns the default speed of a critter.
        '''
        return float(self._config['critter']['min_energy'])

    @property
    def critter_max_energy(self) -> float:
        '''
        Read-only: Returns the default speed of a critter.
        '''
        return float(self._config['critter']['max_energy'])

    @property
    def critter_energy(self) -> float:
        '''
        Read-only: Returns an initial energy for a critter.
        '''
        return random.uniform(self._config['critter']['min_energy'], self._config['critter']['max_energy'])

    @property
    def critter_has_random_size(self) -> bool:
        '''
        Read-only: Returns a flag that determines if critters are given a random size.
        '''
        return bool(self._config['critter']['random_size'])


    @property
    def critter_min_size(self) -> int:
        '''
        Read-only: Returns the minimum initial size of a critter.
        '''
        return int(self._config['critter']['min_size'])

    @property
    def critter_max_size(self) -> int:
        '''
        Read-only: Returns the maximum initial size of a critter.
        '''
        return int(self._config['critter']['max_size'])

    @property
    def critter_size(self) -> int:
        '''
        Read-only: Returns an initial size for a critter.
        '''
        if self.critter_has_random_size:
            return int(random.uniform(self._config['critter']['min_size'], 
                                      self._config['critter']['max_size']))
        else:
            return self.critter_fixed_size

    @property
    def critter_energy_scale(self) -> float:
        '''
        Read-only: Returns a scalar value for critter energy calculations.
        '''
        return float(self._config['critter']['energy_scale'])

    @property
    def critter_min_speed(self) -> int:
        '''
        Read-only: Returns the minimum speed for the largest critter.
        '''
        return int(self._config['critter']['min_speed'])

    @property
    def critter_max_speed(self) -> int:
        '''
        Read-only: Returns the maximum speed for the msallest critter.
        '''
        return int(self._config['critter']['max_speed'])

    @property
    def food_min_size(self) -> int:
        '''
        Read-only: Returns the minimum size of food.
        '''
        return int(self._config['food']['min_size'])

    @property
    def food_initial_count(self) -> int:
        '''
        Read-only: Returns the initial amount of food.
        '''
        return int(self._config['food']['initial_count'])

    @property
    def food_max_size(self) -> int:
        '''
        Read-only: Returns the maximum size of food.
        '''
        return int(self._config['food']['max_size'])

    @property
    def food_energy_scale(self) -> float:
        '''
        Read-only: Returns an initial energy for a sprite.
        '''
        return float(self._config['food']['energy_scale'])

    @property
    def food_respawn_rate(self) -> int:
        '''
        Read-only: Returns the maximum speed for the msallest sprite.
        '''
        return int(self._config['food']['respawn_rate'])
    
    @property
    def food_respawn_count(self) -> int:
        '''
        Read-only: Returns the maximum speed for the msallest sprite.
        '''
        return int(self._config['food']['respawn_count'])

config = Config()
