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

''' ======================== NON-ABSTRACT CLASSES ======================== '''
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
        self.hitcount = 1
        self.weight = 10

    ''' AOE:
      * Given 'pos' a (int, int) tuple representing the position of
      * impact, Returns a list of all (int, int) tuples,
      * representing the set of positions hit by the weapon
      * [ X ]
    '''
    def AOE(self, pos):
        return [pos]

'''Shotgun:
  * The Shotgun Weapon Class

class Shotgun(SuperItem):
    def __init__(self):
        self.name = "shotgun"
        self.range = 3
        self.hitcount = 3
        self.weight = 10

    '' AOE:
      * Given 'pos' a (int, int) tuple representing the position of
      * impact, Returns a list of all (int, int) tuples,
      * representing the set of positions hit by the weapon
    ''
    def AOE(self, posPlayer, listofTargets):
        hitList = []
        counter = 0
        # hit up to number of possible hitcounts
        for target in listofTargets:
            # hit the first three targets within range in the list
            if self.manhattanDistance(posPlayer, target) <= self.range and counter < self.hitcount:
                hitList.append(target)
                counter += 1
        return hitList
'''

'''Rifle:
  * The Rifle Weapon Class
'''
class Rifle(SuperItem):
    def __init__(self):
        self.name = "rifle"
        self.range = 10
        self.hitcount = 1
        self.weight = 10

    ''' AOE:
      * Given 'posPlayer' a (int, int) tuple representing the position of
      * the player and 'listofTargets' a list of posn tuples representing
      * the positions of the point of enemies, Returns a list of all enemy
      * positions (int, int) hit by the weapon. Position of first impact 
      * is always in the middle of the returned list.
      * [ X  X  X ]
      * [ X  X  X ]
      * [ X  X  X ]
    '''
    def AOE(self, pos):
        return [pos, 
        (pos[0] - 1, pos[1] + 0),
        (pos[0] - 1, pos[1] - 1),
        (pos[0] + 0, pos[1] + 1),
        (pos[0] + 1, pos[1] + 1),
        (pos[0] + 1, pos[1] + 0),
        (pos[0] + 1, pos[1] - 1),
        (pos[0] + 0, pos[1] - 1),
        (pos[0] - 1, pos[1] - 1)]

'''GrenadeLauncher:
  * The Grenade Launcher Weapon Class
'''
class GrenadeLauncher(SuperItem):
    def __init__(self):
        self.name = "grenade launcher"
        self.range = 7
        self.hitcount = 5
        self.weight = 10

    ''' AOE:
      * Given 'posPlayer' a (int, int) tuple representing the position of
      * the player and 'listofTargets' a list of posn tuples representing
      * the positions of the point of enemies, Returns a list of all enemy
      * positions (int, int) hit by the weapon. Position of first impact 
      * is always in the middle of the returned list.
      * [ X  X  X  X  X ]
      * [ X  X  X  X  X ]
      * [ X  X  X  X  X ]
      * [ X  X  X  X  X ]
      * [ X  X  X  X  X ]
    '''
    def AOE(self, pos):
        return [pos, 
        (pos[0] - 1, pos[1] + 0),
        (pos[0] - 1, pos[1] - 1),
        (pos[0] + 0, pos[1] + 1),
        (pos[0] + 1, pos[1] + 1),
        (pos[0] + 1, pos[1] + 0),
        (pos[0] + 1, pos[1] - 1),
        (pos[0] + 0, pos[1] - 1),
        (pos[0] - 1, pos[1] - 1),  # Here and above same as rifle
        (pos[0] - 2, pos[1] + 0),
        (pos[0] - 2, pos[1] + 1),
        (pos[0] - 2, pos[1] + 2),
        (pos[0] - 1, pos[1] + 2),
        (pos[0] - 0, pos[1] + 2),
        (pos[0] + 1, pos[1] + 2),
        (pos[0] + 2, pos[1] + 2),
        (pos[0] + 2, pos[1] + 1),
        (pos[0] + 2, pos[1] + 0),
        (pos[0] + 2, pos[1] - 1),
        (pos[0] + 2, pos[1] - 2),
        (pos[0] + 1, pos[1] - 2),
        (pos[0] + 0, pos[1] - 2),
        (pos[0] - 1, pos[1] - 2),
        (pos[0] - 2, pos[1] - 2),
        (pos[0] - 2, pos[1] - 1)]

#Testing
target = (0,0)

a = Pistol()
b = Rifle()
c = GrenadeLauncher()
hitenemiesPistol = a.AOE(target)
hitenemiesRifle = b.AOE(target)
hitenemiesGrenadeLauncher = c.AOE(target)

print "\n", "Pistol hit: ", hitenemiesPistol, "\n"
print "Rifle hit: ", hitenemiesRifle, "\n"
print "Grenade Launcher hit: ", hitenemiesGrenadeLauncher, "\n"
print "DataType of elements: ", type(hitenemiesGrenadeLauncher[0])
