from util import knowledge, counter

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
  * Last Edited: 12/10/15
'''

''' wisdom:
  * Represents the knowledge the hero has gathered 
  * regarding a given item set.
''' 
class wisdom:
    def __init__(self, store):
        ''' Used for access to availble items'''
        self.store = store
        ''' Used to store valuations on items,
          * Which can be evaluated and modified in terms of 
          * features '''
        self.featuredVal = knowledge()
        ''' Used to store the likleyhood any given item is
          * useful, can be normalized and cloned.
          * Defaults to 0. '''
        self.relativeUse = counter()

    ''' useable:
      * Returns a counter mapping item-names to the
      * number of enemies that item would hit
    '''
    def useable(self, heroPos, vilList):
        rtrn = counter()
        # TODO
        return rtrn