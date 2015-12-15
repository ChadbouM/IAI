import sys
from items import Weapon, Ammo, Medkit
from wiseClass import wisdom
from operator import itemgetter
from util import classyList

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
        # for key in self.calculate(theWisdom):
        # 	currentItem = theWisdom.store[key]
        # 	if output.getWeight(currentItem.getWeight()) <= invSize:
        # 		if type(currentItem) == Weapon: 
        # 			counter = 0
        # 			for item in output:
        # 				if type(item) == Weapon:
        # 					counter += 1
        # 			if counter < 2:
        # 				output += [currentItem]
        # 		else:
        # 			output += [currentItem]
        # print output
        # return output

        temp = theWisdom
        while output.getWeight() <= invSize:
        	bestItem = self.calculate(temp)[0]
        	# print "weapon?:", temp.store[bestItem]
        	# print "bestItem:", output
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
        # print output
        return output
    	
    ''' calculate:
     * Returns a list of tuples sorted by the values in the
     * temp dictionary
     * Also calculates the importance of an item based on its
     * usage and featured value
    '''
    def calculate(self, theWisdom):
    	temp = []
        for item in theWisdom.store:
            name = item.getName()
            value = theWisdom.featuredVal[name] * theWisdom.relativeUse[name] + 1
            temp += [(name, value)]
        # print temp
        return [ key for key, value in sorted(temp, key=itemgetter(1), reverse=True) ]