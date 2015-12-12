from util import knowledge, counter, pmCounter, mDist
import items

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
  * Last Edited: 12/11/15
'''

''' wisdom:
  * Represents the knowledge the hero has gathered 
  * regarding a given item set.
''' 
class wisdom:
    def __init__(self, store):
        ''' Used for access to availble items'''
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
    def useable(self, hero, vilList):
        # Helper, tallies overlap between AOE and Villians
        def kCount(self, tar, wep, tars):
            return len([0 for h in wep.AOE(tar) if in tars])
        rtrn = pmCounter()
        # Find the Best Shot for each
        bestShot = None
        maxHits = 0
        for weap in [item for item in store if type(item) == Weapon]:
            for villian in vilList:
                if mDist(hero, villian) <= weap.range:
                    # Take advantage of Max-Set, a feature of the pmCounter
                    rtrn[weap.name] = (villian, kCount(villian, weap, vilList))
            # Set the relative usefullness to be higher.
            self.relativeUse[weap.name] += rtrn[weap.name][1] 
        return rtrn