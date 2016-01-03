from util import knowledge, counter, pmCounter, mDist
from items import *

''' wiseClass.py: IAI Project
  * The class(es) used in the creation and manipulation
  * of a feature-based learning agent
  * Uses the list of all possible items, and experience
  * in the hunting simulator to evaluate item and feature
  * values.
  * Used in the simulator to create 'Desire' (Learn)
  * Used in the store to make pourchasing decisions
  * *
  * Author(s):
  * Michael Chadbourne
  * Mateo Freyre
& * Tim Webber
  * *
  * Last Edited: 1/2/16
'''

''' wisdom:
  * Represents the knowledge the hero has gathered 
  * regarding a given item set.
''' 
class wisdom:
    def __init__(self, store):
        ''' Used for access to available items'''
        self.store = store
        ''' Used to store evaluations on items,
          * Which can be evaluated and modified in terms of 
          * features '''
        self.featuredVal = knowledge()
        ''' Used to store the damage potential relative to
          * Other 
          * Defaults to 0. '''
        self.relativeUse = counter()
        
    ''' useable:
      * Returns a counter mapping item-names to the
      * position, and the number of enemies which would be
      * hit by firing on that position
    '''
    def useable(self, hero, vilPosnList):
        # Helper, tallies overlap between AOE and Villians
        def kCount(tar, wep, tars):
            return len([0 for h in wep.AOE(tar) if h in tars])
        rtrn = pmCounter()
        # Find the Best Shot for each
        bestShot = None
        maxHits = 0
        for weap in [item for item in self.store if type(item) == Weapon]:
            for villian in vilPosnList:
                #print villian
                if mDist(hero.position, villian) <= weap.range:
                    # Take advantage of Max-Set, a feature of the pmCounter
                    rtrn[weap.name] = (villian, kCount(villian, weap, vilPosnList))
            # Set the relative usefullness to be higher.
            self.relativeUse[weap.name] += rtrn[weap.name][1] 

        for ammo in [item for item in self.store if type(item) == Ammo]:
            self.relativeUse[ammo.name] += self.relativeUse[ammo.getType()]

        for medkit in [item for item in self.store if type(item) == Medkit]:
            self.relativeUse[medkit.name] += medkit.healPower

        for candy in [item for item in self.store if type(item) == Candy]:
            self.relativeUse[candy.name] += candy.points

        self.relativeUse.normalize()
        return rtrn

    ''' theSage:
     * return an updated wisdom based on the score, the hero's remaining inventory,
     * and whether or not the hero won
    '''
    def theSage(self, score, remainingInv):
        for item in remainingInv:
            if score[0]: # if hero wins
                if self.relativeUse[item] > 0: # if item was used increase its importance
                    self.featuredVal.tagAdd(item, 1 * score[1])
                else: # if item wasn't used decrease importance
                    self.featuredVal.tagSub(item, 10)
            else: # if hero loses
                self.featuredVal.tagSub(item, 100 * score[1])

        return self