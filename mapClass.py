from random import randint

''' mapClass.py: IAI Project
  * The classes used in representing the map
  * as well as instantiations of those classes
  * *
  * Author(s):
  * Michael Chadbourne
  * Mateo Freyre
& * Tim Webber
  * *
  * Last Edited: 12/13/15
'''
__MINRANDSIZE__ = 5
__MAXRANDSIZE__ = 30



''' gameMap:
  * A representation of a game-level
  * Self randomizes anything left undeclared
'''
class gameMap:
    __slots__ = ['levelSize', 'heroSpawn', 'levelExit', 'vilSpawns']
                    
    def __init__(self, size=None, startX=None, spawns=None):
        if size is None: size = (randint(__MINRANDSIZE__, __MAXRANDSIZE__),
                                 randint(__MINRANDSIZE__, __MAXRANDSIZE__))
        self.levelSize = size               # Level Bounds
        if startX is None: startX = randint(0, size[1])
        self.heroSpawn = (startX, 0)        # Starting location (X, 0)
        self.levelExit = (startX, size[1])  # Win-Condition
        if spawns is None: spawns = randint(5, size[0]*size[1]/3)
        if type(spawns) == list:
            self.vilSpawns = spawns         # Set enemy start locations
        elif type(spawns) == int:
            self.randomizeVil(spawns)
        else: raise TypeError(str(spawns) + " is not a valid spawn type")
        
    ''' randomizeVil:
      * Sets the villians to random locations
    '''
    def randomizeVil(self, n=None):
        # Default n to the current number of Villians
        if n is None: n = len(self.vilSpawns)
        self.vilSpawns = []
        for i in range(n):
            while True:
                tempVil = (randint(0, self.levelSize[0]), randint(0, self.levelSize[1]))
                if tempVil not in self.vilSpawns and tempVil is not self.heroSpawn:
                    self.vilSpawns += [tempVil]
                    break
        
def generateSwarm(size, botLeft):
    swarm = []
    X, Y = size
    lX, bY = botLeft
    for x in range(X):
        swarm += [(lX + x, bY + y) for y in range(Y)]
    return swarm
        
'''============================= PRESET MAPS ================================'''

SwarmSize = (4, 6)
SwarmLocations = [(0, 0), (0, 10), (0, 17), (20, 5), (20, 12)]
SpawnLocations = []
for Swarm in SwarmLocations: SpawnLocations += generateSwarm(SwarmSize, Swarm)
MapSize       = (30, 30)
LargeSwarmMap = gameMap(MapSize, 10, SpawnLocations)

if __name__ == '__main__' and __debug__:
    def printMap(map):
        X, Y = map.levelSize
        for y in range(Y, -1, -1):
            pline = ""
            for x in range(X):
                point = (x, y)
                if point in map.vilSpawns:   pline+="[X]"
                elif point == map.heroSpawn: pline+="|0|"
                elif point == map.levelExit: pline+="{E}"
                else:                        pline+="   "
            print "\t" + pline
        print " "
        
    print "PRINTING LARGE SWARM MAP:"
    printMap(LargeSwarmMap)
        
    