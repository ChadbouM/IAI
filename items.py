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

    def __init__(self, name=None, weight=0):
        # Item name as string, used for ID
        self.name   = name
        # Representation of space taken by the item
        self.weight = weight

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

''' ======================== SEMI-ABSTRACT CLASSES ======================== '''
''' Medkit:
  * The semi-stract class for medkits
'''
class Medkit(SuperItem):
    def __init__(self, name='gen_medkit', hp=10, weight=5):
        SuperItem.__init__(self, name, weight) 
        self.healPower = hp
 
''' Weapon:
  * The semi-stract class for weapons
''' 
class Weapon(SuperItem):
    ''' genAOE:
      * The generic AOE function
      * Hits the given target
    '''
    def genAOE(pos):
        return [pos]
    
    def __init__(self, name='pistol', weight=10, range=5, AOE=genAOE):
        SuperItem.__init__(self, name, weight)
        self.range = range
        self.AOE   = AOE

'''Ammo:
  * The semi-stract class for ammo
'''
class Ammo(SuperItem):
    def __init__(self, name="ammo", weight=1, type='GENERIC'):
        SuperItem.__init__(self, name, weight)
        '''The .name of the item this ammo reloads
          *  'GENERIC' can reload anything'''
        self.type   = type 

'''Candy:
  * The semi-stract class for candy
'''
class Candy(SuperItem):
    def __init__(self, name='gen_candy', weight=5, points=50):
        sSuperItem.__init__(self, name, weight)
        self.points = points

''' ========================= WEAPONS & AMMO ========================= '''
''' ::Generic Ammo::
  * Ammo which is heavy, but can reload any weapon
'''
GenericAmmo = Ammo('Lando\'s one-size-fits-all ballistic', 5)

'''Pistol:
  * The Pistol Weapon '''
Pistol = Weapon()
PistolAmmo = Ammo('pistol ammo', 1, 'pistol')

'''Shotgun:
  * The Shotgun Weapon'''
def AOE_Shotgun(pos):
    ''' [       X      ]
      * [ X X X X X X X]
      * [       X      ]
    '''
    horizontal  = [(pos[0]+i, pos[1]) for i in range(-3, 4)]
    verticle    = [(pos[0], pos[1]+i) for i in range(-1, 2)]       
    return set(horizontal + verticle)
    
name_Shotgun = 'shotgun'
Shotgun = Weapon(name_Shotgun, 10, 3, AOE_Shotgun)  
ShotgunAmmo = Ammo('shell', 1, name_Shotgun)

'''Rifle:
  * The Rifle Weapon
'''
def AOE_Rifle(pos):
    ''' [ X  X  X ]
      * [ X  X  X ]
      * [ X  X  X ]
    '''
    lineNorth = [(pos[0]+i, pos[1]+1) for i in range (-1,2)]
    lineMain  = [(pos[0]+i, pos[1])   for i in range (-1,2)]
    lineSouth = [(pos[0]+i, pos[1]-1) for i in range (-1,2)]  
    return list(set(lineNorth + lineMain + lineSouth))

name_Rifle = 'rifle'
Rifle     = Weapon(name_Rifle, 10, 10, AOE_Rifle)
RifleAmmo = Ammo('rifle ammo', 1, name_Rifle)
    
''' ::GrenadeLauncher::
  * The Grenade Launcher Weapon and Ammo
'''
def AOE_Grenade(pos):
    ''' [ X  X  X  X  X ]
      * [ X  X  X  X  X ]
      * [ X  X  X  X  X ]
      * [ X  X  X  X  X ]
      * [ X  X  X  X  X ]
    '''
    rtrn = []
    for j in range(-2, 3):
        rtrn += [(pos[0]+i, pos[1]+j) for i in range(-2,3)]
    return rtrn
        
name_Grenade    = 'grenade launcher'       
GrenadeLauncher = Weapon(name_Grenade, 10, 7, AOE_Grenade)
GrenadeAmmo     = Ammo('grenade', 2, name_Grenade) 

    

#Testing
if __name__ == '__main__' and __debug__:
    def printHits(hitList):
        boundX = [0,0]
        boundY = [0,0]
        for x, y in hitList:
            if x < boundX[0]: boundX[0]=x
            if x > boundX[1]: boundX[1]=x
            if y < boundY[0]: boundY[0]=y
            if y > boundY[1]: boundY[1]=y
        for i in range(boundY[0], boundY[1]+1):
            pline = ""
            for j in range(boundX[0], boundX[1]+1):
                if (j, i) in hitList: pline+="[X]"
                else:                 pline+="   "
            print "\t" + pline
        print " "
            
    print " * RUNNING TESTS: items.py *"

    target = (0,0)

    hitenemiesPistol          = Pistol.AOE(target)
    hitenemiesShotgun         = Shotgun.AOE(target)
    hitenemiesRifle           = Rifle.AOE(target)
    hitenemiesGrenadeLauncher = GrenadeLauncher.AOE(target)
    
    print "\nPistol Hits:"
    printHits(hitenemiesPistol)
    print "Shotgun Hits:"
    printHits(hitenemiesShotgun)
    print "Rifle Hits:"
    printHits(hitenemiesRifle)
    print "Grenade Launcher Hits:"
    printHits(hitenemiesGrenadeLauncher)
