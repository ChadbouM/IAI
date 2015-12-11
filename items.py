#IMPORTS

''' items.py: IAI Project
  * Provides outlines of what each item-class
  * is required to have, followed by several instantiated
  * item classes
  * *
  * Author(s):
  * Michael Chadbourne
  * Mateo Freyre
& * Tim Webber
  * *
  * Last Edited: 12/10/15
'''

''' Weapon:
  * An abstract class for weapons
'''
class Weapon(object):
    def __init__(self):
        self.name = ""
        self.range = 0
        self.weight = 0
        self.damage = 0
        # Do we need an "ammo type"?
        
    ''' AOE:
      * Given 'pos' a (int, int) tuple representing the position of
      * impact, Returns a list of all (int, int) tuples,
      * representing the set of positions hit by the weapon
    '''
    def AOE(self, pos):
        raise NotImplementedError('subclasses must be overidden, yo')

''' Medkit:
  * An abstract class for medkits
'''
class Medkit(object):
    def __init__(self):
        self.name = ""
        self.healPower = 0
        self.weight = 0


'''Ammo:
  * An abstract class for ammo
'''
class Ammo(object):
    def __init__(self):
        self.name = ""
        self.weight = 0
        # If we need an "ammo type", it must be here as well

'''Candy:
  * An abstract class for candy
'''
class Candy(object):
    def __init__(self):
        self.name = ""
        self.weight = 0
        self.points = 0