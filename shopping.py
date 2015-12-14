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
     * Buy items from the store and place them in the inventory
     * based on the determined importance of each item
    '''
   	def shopping(invSize, theWisdom):
   		counter = 0
   		output = {}
   		itemRatings = self.calculate(theWisdom)
   		for key, value in itemRatings:
   			currentItem = theWisdom.store[key]
   			if counter + currentItem.getWeight() <= invSize:
   				output.update({key: currentItem})
   				counter += currentItem.getWeight()
   			
   		return output
    	
    '''
     * Returns a list of tuples sorted by the values in the
     * temp dictionary
     * Also calculates the importance of an item based on its
     * usage and featured value
    '''
    def calculate(theWisdom):
    	temp = {}
    	for item in wisdom.store:
    		name = item.getName()
    		temp.update({name: theWisdom.featuredVal[name] * theWisdom.relativeUse[name]})

    	return sortDictByVal(temp)

    '''
     * Sorts a dictionary by values and returns it as a list of tuples
     * Values sorted greatest to smallest
    '''
   	def sortDictByVal(dictionary):
   		return sorted(dictionary.iteritems(), key=itemgetter(1), reverse=True)