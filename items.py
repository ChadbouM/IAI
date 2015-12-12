#IMPORTS
from abc import ABCMeta, abstractmethod

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

''' Medkit:
  * An abstract class for medkits
'''
class Medkit(object):
    def __init__(self):
        self.name = ""
        self.healPower = 10
        self.weight = 5

'''Ammo:
  * An abstract class for ammo
'''
class Ammo(object):
    def __init__(self):
        self.name = ""
        self.weight = 1
        # If we need an "ammo type", it must be here as well

'''Candy:
  * An abstract class for candy
'''
class Candy(object):
    def __init__(self):
        self.name = ""
        self.weight = 5
        self.points = 50

''' Weapon:
  * An abstract superclass for all weapons
'''
class Weapon(object):

    def __init__(self):
        self.name = ""
        self.range = 0
        self.weight = 0
        self.damage = 0
        # Do we need an "ammo type"?
        # I think we should leave out for now
        # and add in if we have time.
        # It will add complexity
        
    ''' AOE:
      * Given 'pos' a (int, int) tuple representing the position of
      * impact, Returns a list of all (int, int) tuples,
      * representing the set of positions hit by the weapon
    '''
    def AOE(self, pos):
        raise NotImplementedError('subclasses must be overidden, yo')

    ''' getName:
      * Returns the name of the object
    '''
    def getName(self):
        return self.name

''' ========================= WEAPONS ========================= '''
'''Pistol:
  * The Pistol Weapon Class
'''
class Pistol(Weapon):
    def __init__(self):
      	self.name = "pistol"
      	self.range = 5
        self.weight = 10

	def AOE(self):
		raise NotImplementedError('MAKE ME BITCH')

'''Shotgun:
  * The Shotgun Weapon Class
'''
class Shotgun(Weapon):
    def __init__(self):
        self.name = "shotgun"
        self.range = 2
        self.weight = 10

    def AOE(self):
        raise NotImplementedError('MAKE ME BITCH')

'''Rifle:
  * The Rifle Weapon Class
'''
class Rifle(Weapon):
    def __init__(self):
        self.name = "rifle"
        self.range = 10
        self.weight = 10

    def AOE(self):
        raise NotImplementedError('MAKE ME BITCH')

a = Pistol()
print a.getName()

