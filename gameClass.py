import util

''' gameClass.py: IAI Project
  * The classes used in creating and running the
  * hunting simulation.
  * Used as the test site for the inventory
  * *
  * Author(s):
  * Michael Chadbourne
  * Mateo Freyre
& * Tim Webber
  * *
  * Last Edited: 12/10/15
'''

''' heroAgent:
  * A basic decision agent
  * used to traverse the inventory through the map
'''
class heroAgent:
    # init-helper: processes the given item-data into a list
    def refine(rawItems):
        #TODO return as a list of game_items
        return []

    def __init__(self, start, rawItems, wisdom):
        self.health   = 100              # health points
        self.position = start            # X, Y position as tuple
        self.invtry   = refine(rawItems) # A list of game_items available to the hero
        self.wisdom   = wisdom           # The heroes sense of item-knowledge
    
    ''' use:
      * uses an item, and updates the valuation of that item somewhat
      * returns None, if the action could not be completed
    '''
    def use(self, context):
        if context == 'HEAL':
            return None
    
    ''' move:
      * moves the hero north
      * removing any villians in his path. TODO
    '''
    def move(self):
        self.position = (self.position[0] + 1, self.position[1] + 1)
    
    
    ''' advance:
      * Progresses the hero forward acording
      * to a basic set of rules based upon villian position
      * and moving north
    '''
    def advance(self, gameState):
        weapons = self.wisdom.useable()
        if health < 40: 
            if self.use("HEAL") != None: return
        if weapons.decide() == None:
            if health <= 90: 
                if self.use("HEAL") != None: return
            self.move()
            return
        for weapon, usage in weapons.items():
            if self.use(weapons.decide()) != None: return
        self.move()    
            

''' villiansAgent:
  * A basic decision agent for enemies
  * Acts on a list of positions to attack the Hero
'''
class villiansAgent:
    def __init__(self, positions):
        self.positions = positions
        self.healthi   = [20] * len(positions)

    ''' stats:
      * returns a tuple with the stats for the specified villian
      * as (Position, HP)
    '''
    def stats(self, index):
        return (self.positions[i], self.healthi[i])

    ''' advance:
      * Progresses each of the locations in 'Positions' forward
      * acording to a basic set of rules based upon hero position
    '''
    def advance(self, gameState):
        #TODO another 'basic set of rules'

''' gameMap:
  * A representation of a game-level
'''
class gameMap:
    def __init__(self, width, height, start, end, spawns):
        self.levelSize = (width, height) #Level Bounds
        self.heroSpawn = start  # Starting location
        self.levelExit = end    # Win-Condition
        self.vilSpawns = spawns # Enemy start locations


''' gameState:
  * A representation of the current state of the game
'''
class gameState:
    def __init__(self, map, rawItems, wisdom):
        self.map = map
        self.hero = heroAgent(map.heroSpawn, rawItems, wisdom)
        self.vlns = villiansAgent(map.vilSpawns)
        self.maxVil = len(map.vilSpawns)
        self.time = 0

    ''' gameOver:
      * returns true if the game has reached an end-conditions
      * false otherwise
    '''
    def gameOver(self):
        return (self.hero.position == self.map.levelExit or self.hero.health <= 0)

    ''' score:
      * returns a score tuple, consisting of a boolean and an integer score-value
      * the boolean will be true if the win-condition is the only end-condition
      * currently met and false otherwise
    '''
    def score(self):
        victory = self.hero.position == self.map.levelExit and not self.hero.health <= 0
        value   = 100 * (self.maxVil - len(self.vlns.positions)) - (5 * self.time) #TODO less arbitrary
        return (victory, value)

    ''' advance:
      * Progresses the game state forward by one unit of time.
    '''
    def advance(self):
        if (self.gameOver()): return
        self.hero.advance(self)
        self.vlns.advance(self)