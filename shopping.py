import sys
from wiseClass import wisdom
from operator import itemgetter

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

	'''
	 * initializes a weight for the inventory
	 * initializes an inventory as a dictionary {itemName: itemObject}
	'''
	def __init__(self, maxWeight=100):
        self.maxWeight = maxWeight # maximum inventory space for each hunt
        self.inventory = {} #items to be used on the next hunt

    '''
     * Buy items from the store and place them in the inventory
     * based on the determined importance of each item
    '''
   	def buy():
   		counter = 0
   		itemRatings = self.calculate()
   		for key, value in itemRatings:
   			currentItem = wisdom.store[key]
   			if counter + currentItem.getWeight() <= self.maxWeight:
   				self.inventory.update({key: currentItem})
   				counter += currentItem.getWeight()
   			
   		return self.inventory
    	
    '''
     * Returns a list of tuples sorted by the values in the
     * temp dictionary
     * Also calculates the importance of an item based on its
     * usage and featured value
    '''
    def calculate():
    	temp = {}
    	for item in wisdom.store:
    		name = item.getName()
    		temp.update({name: wisdom.featuredVal[name] * wisdom.relativeUse[name]})

    	return sortDictByVal(temp)

    '''
     * Sorts a dictionary by values and returns it as a list of tuples
     * Values sorted greatest to smallest
    '''
   	def sortDictByVal(dictionary):
   		return sorted(dictionary.iteritems(), key=itemgetter(1), reverse=True)