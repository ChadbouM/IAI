import util, copy
from items import *
from random import choice

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
  * Last Edited: 12/13/15
'''

''' heroAgent:
  * A basic decision agent
  * used to traverse the inventory through the map
'''
class heroAgent:

    def __init__(self, start, items, wisdom):
        self.health   = 100     # health points
        self.position = start   # X, Y position as tuple
        self.invtry   = items   # A list of game_items available to the hero
        self.wisdom   = wisdom  # The heroes sense of item-knowledge
    
    ''' use:
      * uses an item, and updates the valuation of that item somewhat
      * returns None, if the action could not be completed
    '''
    def use(self, item, gameState):
        itemVal = self.wisdom.featuredVal # used to update the importance of an item
        itemUse = self.wisdom.relativeUse # used to update the usage of an item

        if item in self.invtry: 
            if type(item) is Weapon:
                for ammo in self.invtry[Ammo]: # see if we have the right ammo type
                    if ammo.getType() == item.getName() or ammo.getType() == 'GENERIC':
                        itemVal.tagAdd(item, 1)
                        itemUse[item] += 1
                        itemVal.tagAdd(ammo, 1)
                        itemUse[ammo] += 1
                        del self.invtry[ammo.name] # delete one use item
                        return True # ammo was found for gun
                return None # ammo wasn't found for gun
            else: # accounts for health items (which are one use items)
                itemVal.tagAdd(item, 1)
                itemUse[item] += 1
                del self.invtry[item.name] # delete one use item
                return True
        else: # item wasn't found
            itemVal.tagAdd(item, 10)
            itemUse[item] += 1
            return None # item wasn't found
    
    ''' move:
      * moves the hero north
      * removing any villians in his path.
    '''
    def move(self, gameState):
        self.position = (self.position[0], self.position[1] + 1)
        # if the hero encounters a villian on the same position,
        # he will melee it to oblivion
        if self.position in gameState.getVilPosn():
            gameState.vilKill(self.position)
    
    def useKit(self, gameState):
        kits = self.wisdom.store[Medkit]
        bestKit  = kits[0]
        bestDiff = -float('inf')
        for i in range(len(kits)):
            for kit in kits:
                thisDiff = kit.healPower - self.health
                if bestDiff < 0 and 0 < thisDiff:
                    bestKit = kit
                    bestDiff = thisDiff
                thisDiff = min(abs(thisDiff), abs(bestDiff))
            self.use(bestKit, gameState)
            if bestKit in self.invtry:
                print "check"
                return bestKit
            else: 
                kits.remove(bestKit)
                print kits
                print self.wisdom.store[Medkit]
        return None
                
            
            
            
    ''' advance:
      * Progresses the hero forward acording
      * to a basic set of rules based upon villian position
      * and moving north
    '''
    def advance(self, gameState):
        weapons = self.wisdom.useable(gameState.hero, gameState.vlns.getPosns())
        if self.health < 40: 
            if self.useKit(gameState) != None: return
        if weapons.decide() == None:
            if health <= 90: 
                if self.useKit(gameState) != None: return
            self.move(gameState)
            return
        for weapon, usage in weapons.items():
            if self.use(weapons.decide(), gameState) != None: return
        self.move(gameState)    
            

''' villiansAgent:
  * A basic decision agent for enemies
  * Acts on a list of positions to attack the Hero
'''
class villiansAgent:
    def __init__(self, positions):
        self.positions = positions
        self.dmg   = 10

    ''' stats:
      * returns a tuple with the stats for the specified villian
      * as (Position, HP)
    '''
    def stats(self, index):
        return (self.positions[i], self.healthi[i])

    ''' positions:
      * returns the list of positions
    '''
    def getPosns(self):
        return self.positions

    
    ''' advance:
      * Progresses each of the locations in 'Positions' forward
      * according to a basic set of rules based upon hero position
      # Attacks hero when in range
    '''
    def advance(self, gameState):
        target = gameState.hero
        
        advanced = []
        temp = copy.copy(self.positions)
        for pos in self.positions:
            # Remove from temp storage
            temp.remove(pos)
            # Damage Calculation
            dist = util.mDist(target.position, pos)
            if dist < 3:
                gameState.hero.health -= self.dmg
            else:
              # Movement
              X, Y = pos
              moves = [(X, Y), (X+1, Y), (X-1,Y), (X, Y+1), (X, Y-1)]
              legalmoves = [move for move in moves 
                              if  move is not target 
                              and move not in advanced
                              and move not in temp
                              and util.mDist(move, target.position) <= dist]

              advanced += [choice(legalmoves)]
        # They essentialy all move towards hero, attacking whenever in range
        # and sometimes randomly staying still.
        self.positions = advanced
            
            
        
            

''' gameState:
  * A representation of the current state of the game
'''
class gameState:
    def __init__(self, map, items, wisdom):
        self.map = map
        self.hero = heroAgent(map.heroSpawn, items, wisdom)
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

    ''' getVilPosn
     * returns the list of villian positions
    '''
    def getVilPosn(self):
        return self.vlns.getPosns()

    ''' vilKill
     * removes a villian position from the list of villian positions
    '''
    def vilKill(self, posn):
        del self.vils[posn]
