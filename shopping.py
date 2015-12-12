import sys
from wiseClass import wisdom

''' shopping.py: IAI Project
  * 
  * 
  * *
  * Author(s):
  * Michael Chadbourne
  * Mateo Freyre
& * Tim Webber
  * *
  * Last Edited: 12/10/15
'''

''' shopping class:
  * Determines what items to include
  * in the hero's inventory the next time
  * he goes hunting
'''
class shopping:

	'''
	 * initializes a weight for the inventory
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
   		while counter < maxWeight:
   			self.inventory.update({"itemName": wisdom.store["itemName"]})
   		return self.inventory
    	