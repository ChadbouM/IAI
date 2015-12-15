import sys
from items import Weapon, Ammo, Medkit
from wiseClass import wisdom
from operator import itemgetter
from util import classyList
from random import randint, choice

''' shopping.py: IAI Project
  * 
  * 
  * *
  * Author(s):
  * Michael Chadbourne
  * Mateo Freyre
& * Tim Webber
  * *
  * Last Edited: 12/12/15
'''

''' shopping class:
  * Determines what items to include
  * in the hero's inventory the next time
  * he goes hunting
'''
class shopping:
    ''' shopping:
     * Buy items from the store and place them in the inventory
     * based on the determined importance of each item
    '''
    def shopping(self, invSize, theWisdom):
        initial = []
        output = classyList(initial)
        temp = theWisdom
        while output.getWeight() <= invSize:
            if randint(0,25) == 1: output += [choice(temp.store)]
            bestItem = self.calculate(output, temp)[0]
            if type(temp.store[bestItem]) is Weapon: 
                counter = 0
                for item in output:
                    if type(temp.store[item]) is Weapon:
                        counter += 1
                if counter < 2:
                    output += [bestItem]
                    temp.store.remove(temp.store[bestItem]) # here is a remove
                else:
                    for i in temp.store:
                        if type(temp.store[i]) is Weapon:
                            temp.store.remove(temp.store[i]) # here is a remove
            elif type(temp.store[bestItem]) is Ammo: # BIGGEST PROBLEM
                if temp.store[bestItem].getType() in output:
                    temp.featuredVal.tagSub(bestItem, 2)
                    output += [bestItem]
                else:
                    temp.featuredVal.tagSub(bestItem, 2)
            else:
                output += [bestItem]

        return output
        
    ''' calculate:
     * Returns a list of tuples sorted by the values in the
     * temp dictionary
     * Also calculates the importance of an item based on its
     * usage and featured value
    '''
    def calculate(self, current, theWisdom):
        temp = []
        for item in theWisdom.store:
            name = item.getName()
            ex = 0
            if type(item) is Ammo and item.type in [item.name for item in theWisdom.store[Weapon]]: ex = 10000
            value = ex + ((theWisdom.featuredVal[name] * theWisdom.relativeUse[name] + 1)/
                            (len([item for item in  current if item.name == name]) + 1)) / item.weight
            temp += [(item, value)]
        return [ key for key, value in sorted(temp, key=itemgetter(1), reverse=True) ]