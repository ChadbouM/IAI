#!/usr/bin/end python
""" gameClass.py: contains the files used in representing and playing the game
  * part of the IAI project.
  * Contains the GameState class which represents and controls the game.
  * *
  * Last Edited: 01/16/16
"""
# IMPORTS:
from   mapClass import Map
import util

#### CLASSES ####

""" GameState: the class representation of the entire game world
"""
class GameState(object):
    __slots__ = ['hero', 'shop', 'level' ]
    """ __init__: The initialization function for GameState
    """
    def __init__(self):
        self.hero  = Hero()
        self.shop  = Shop()
        self.level = Level()
        
    """ tick: Advances the gameState forward by one frame
    """
    def tick(self, cmd):
        self.hero.tick(cmd)
        self.current_level.tick(cmd)
        
    """ run: Runs the game through, in the case of invisible mode
    """
    def run(self): pass
        
""" Hero: the class representation of the game's Hero agent
"""
class Hero(object):
    __slots__ = [ 'health', 'inventory', 'position' ]
    """ __init__: The initialization function for Hero
    """
    def __init__(self):
        self.health    = 100
        self.inventory = None
        self.position  = (0, 0)
        
    """ tick: Advances the Hero forward by one frame using the given command
    """
    def tick(self, cmd): pass
    
""" Level: the class representation of a game level
"""
class Level(object):
    __slots__ =  [ 'map', 'objects' ]
    """ __init__: The initialization function for Level
    """
    def __init__(self):
        self.map     = Map()
        self.objects = []
        
    """ tick: Advances the level and its contents forward by one frame
    """
    def tick(self, cmd): pass
    
""" Shop: the class representation of the game's shop
"""    
class Shop(object):
    __slots__ = [ 'inventory', 'prices' ]
    """ __init__: The initialization function for Shop
    """
    def __init__(self):
        self.inventory = None
        self.prices    = None
    

#### FUNCTIONS ####

#### LOCAL TESTING ####

### SCRIPT ####
 

