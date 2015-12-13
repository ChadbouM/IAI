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

''' SuperItem:
  * An abstract superclass for all items
'''
class SuperItem(object):

    def __init__(self):
        self.name = ""
        self.weight = 0

    ''' getName:
      * Returns the name of the object
    '''
    def getName(self):
        return self.name

    ''' getWeight:
      * Returns the name of the object
    '''
    def getWeight(self):
        return self.weight

''' ========================= NON-ABSTRACT CLASSES ========================= '''

''' Medkit:
  * An abstract class for medkits
'''
class Medkit(SuperItem):
    def __init__(self):
        self.name = "medkit"
        self.healPower = 10
        self.weight = 5

'''Ammo:
  * An abstract class for ammo
'''
class Ammo(SuperItem):
    def __init__(self):
        self.name = "ammo"
        self.weight = 1
        # If we need an "ammo type", it must be here as 

'''Grenade Ammo:
  * An abstract class for Grenade Ammo
'''
class GrenadeAmmo(SuperItem):
    def __init__(self):
        self.name = "grenade ammo"
        self.weight = 1

'''Candy:
  * An abstract class for candy
'''
class Candy(SuperItem):
    def __init__(self):
        self.name = "candy"
        self.weight = 5
        self.points = 50

''' ========================= WEAPONS ========================= '''
'''Pistol:
  * The Pistol Weapon Class
'''
class Pistol(SuperItem):
    def __init__(self):
      	self.name = "pistol"
      	self.range = 5
        self.weight = 10

	def AOE(self):
		raise NotImplementedError('MAKE ME BITCH')

'''Shotgun:
  * The Shotgun Weapon Class
'''
class Shotgun(SuperItem):
    def __init__(self):
        self.name = "shotgun"
        self.range = 2
        self.weight = 10

    def AOE(self):
        raise NotImplementedError('MAKE ME BITCH')

'''Rifle:
  * The Rifle Weapon Class
'''
class Rifle(SuperItem):
    def __init__(self):
        self.name = "rifle"
        self.range = 10
        self.weight = 10

    def AOE(self):
        raise NotImplementedError('MAKE ME BITCH')

'''GrenadeLauncher:
  * The Grenade Launcher Weapon Class
'''
class GrenadeLauncher(SuperItem):
    def __init__(self):
        self.name = "Grenade Launcher"
        self.range = 5
        self.weight = 10

    def AOE(self):
        raise NotImplementedError('MAKE ME BITCH')