#!/usr/bin/end python
""" itemClassp.py
  * part of the IAI project. Contains the class representations of items.
  * *
  * Last Edited: 01/28/16
"""
# IMPORTS:
import util
from Tkinter import PhotoImage

#### CLASSES ####

""" MapItem: The class representation of an item on the game map.
  * Includes conventional items which can be picked up off the ground, as well 
  * as Enemies.
"""
class MapItem(object):
    """ __init__:
    """
    def __init__(self, map, name, type, args):
        self.name  = name
        self.image = PhotoImage(file=util.local_path("%s\\%s" % (map, name)))
        util.type_check(dict, args)
        # Instantiate type with args.
        self.type = type
        for key, value in args.items():
            self.__setattr__(key, value)

    """ __repr__: Returns the printed representation of the class, used for save
      * Prints the type and name of the class followed by the field values.
    """
    def __repr__(self):
        fields = [ 'health', 'attack', 'speed', 'range', 'count' ]
        repr = "%s: %s {\n" % (self.type.upper(), self.name)
        for field in fields:
            try:
                addition = str(self.__getattribute__(field))
                repr += "\t%s: %s\n" % (field.upper(), addition)
            except: pass
        return repr + "}\n"
        
    
""" GameItem: The class representation of a generic item in the Hero's inventory
"""
class GameItem(object):
    ''' __init__: The generic initializer for items
      * Sets the name weight and cost of an item, the basic stats shared by all
      * item types
    '''
    def __init__(self, name, weight, cost):
        self.name   = name
        self.weight = weight
        self.cost   = cost
        
    # Items should all have a 'use' function    
    def use(self): pass
    
#   ######################   #
# #### ITEM SUB-CLASSES #### #
#   ######################   #
  
# The Item Subclass for Weapons        
class Weapon(GameItem): pass

# The Item Subclass for Healing Items
class Salve(GameItem):  pass

# The Item Subclass for Ammunition
class Ammo(GameItem):   pass 

# The Item Subclass for Candy
class Candy(GameItem):  pass   


#### FUNCTIONS ####

#### LOCAL TESTING ####

### SCRIPT ####
 

