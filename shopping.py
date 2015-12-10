import sys

''' shopping class:
  * This class stores a diary of moves
  * and actions taken during the game
  * and determines what items to include
  * in the hero's inventory the next time
  * he goes hunting son
'''
class shopping

	'''
	 * A diary item is:
	 * - (string, int, int, int or list of strings)
	 * - (item used or move or damage, turn number, hit points, kills or list of tags)
	'''
	def __init__(self, diary):
        self.diary = diary

    '''
    If the first item in the tuple is a "hit", then the last item will be a list of tags
    '''
    def whatToBuy():
    	