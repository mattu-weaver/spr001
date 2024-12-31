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
    def sprite_fixed_size(self) -> int:
        '''
        Read-only: Returns the fixed size of a sprite.
        '''
        return int(self._config['sprite']['fixed_size'])

    @property
    def sprite_min_energy(self) -> float:
        '''
        Read-only: Returns the default speed of a sprite.
        '''
        return float(self._config['sprite']['min_energy'])

    @property
    def sprite_max_energy(self) -> float:
        '''
        Read-only: Returns the default speed of a sprite.
        '''
        return float(self._config['sprite']['max_energy'])

    @property
    def sprite_energy(self) -> float:
        '''
        Read-only: Returns an initial energy for a sprite.
        '''
        return random.uniform(self._config['sprite']['min_energy'], self._config['sprite']['max_energy'])

    @property
    def sprite_has_random_size(self) -> bool:
        '''
        Read-only: Returns a flag that determines if sprites are given a random size.
        '''
        return bool(self._config['sprite']['random_size'])


    @property
    def sprite_min_size(self) -> int:
        '''
        Read-only: Returns the minimum initial size of a sprite.
        '''
        return int(self._config['sprite']['min_size'])

    @property
    def sprite_max_size(self) -> int:
        '''
        Read-only: Returns the maximum initial size of a sprite.
        '''
        return int(self._config['sprite']['max_size'])

    @property
    def sprite_size(self) -> int:
        '''
        Read-only: Returns an initial size for a sprite.
        '''
        if self.sprite_has_random_size:
            return int(random.uniform(self._config['sprite']['min_size'], self._config['sprite']['max_size']))
        else:
            return self.sprite_fixed_size

    @property
    def sprite_energy_scale(self) -> float:
        '''
        Read-only: Returns a scalar value for sprite energy calculations.
        '''
        return float(self._config['sprite']['energy_scale'])
    
    @property
    def sprite_base_speed(self) -> int:
        '''
        Read-only: Returns the base speed of a sprite.
        '''
        return int(self._config['sprite']['base_speed'])
    
    @property
    def sprite_min_speed(self) -> int:
        '''
        Read-only: Returns the minimum speed for the largest sprite.
        '''
        return int(self._config['sprite']['min_speed'])
    

    @property
    def sprite_max_speed(self) -> int:
        '''
        Read-only: RReturns the maximum speed for the msallest sprite.
        '''
        return int(self._config['sprite']['max_speed'])
    



config = Config()
