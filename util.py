from random import choice

''' util.py: IAI Project
  * A small collection of custom mapping agents 
  * and other utilities used for various tasks
  * *
  * Author(s):
  * Michael Chadbourne
  * Mateo Freyre
& * Tim Webber
  * *
  * Last Edited: 12/13/15
'''

''' tagon:
  * Special sub-class used to track the various
  * feature tags used in the knowledge class
'''
class tagon(dict):
    ''' copy:
      * Returns a clone of this object
    '''
    def copy(self):
        return tagon(dict.copy(self))

    ''' __missing__:
      * Defines the behavior when retrieving a key which is
      * not in self.keys(), returns an empty list
    '''
    def __missing__(self, key):
        return []
        
    ''' __add__:
      * Defines behavior around the '+' operand
      * concatenates lists for each key.
    '''
    def __add__(self, n):
        clone = self.copy()
        if type(n) == tagon:
            for key, val in n.items():
                for item in val:
                    if item not in clone[key]:
                        clone[key] += [item]
        else: raise TypeError("Cannot add " + type(n).__name__ + " to tagon")
        return clone

''' knowledge:
  * A special class used to track the value of items
  * Supports addition, copy, feature-based tagging and
  * defaults to 1
'''
class knowledge(dict):
    tags = tagon()
    
    ''' copy:
      * Returns a clone of this object
    '''
    def copy(self):
        clone = knowledge(dict.copy(self))
        clone.tags = self.tags
        return clone
    
    ''' __missing__:
      * Defines the behavior of retrieving a key, when the key does not exist.
      * Defaults to 1, with Feature-based-retrieval.
    '''
    def __missing__(self, key):
        if key in self.tags.keys():
            return [self[newkey] for newkey in self.tags[key]]
        return 1
    
    ''' __add__:
      * Defines behavior around '+' opperator
      * Handles ints and other knowledge classes
    '''    
    def __add__(self, n):
        clone = self.copy()
        if type(n) == int:
            for key in clone.keys(): clone[key] += n        
        elif type(n) == knowledge:
            clone.tags += n.tags
            for key, value in n.items():
                if key in clone.keys():
                    clone[key] += value
                else: clone[key] = value
        else: raise TypeError("Cannot add " + type(n).__name__ + " to knowledge")
        return clone
        
    ''' __radd__:
      * Defines behavior around '+' operator from the right
      * Handles ints, as they have no knowledge addition method
    '''
    def __radd__(self, n):
        try:
            return self.__add__(n)
        except TypeError:
            return NotImplemented 
    
    ''' tagAs:
      * Labels the given key with the given tag
    '''
    def tagAs(self, key, tag):
        self.tags[tag] += [key]
        
    ''' tagAdd:
      * Performs addition on each key belonging to the given tag
    '''
    def tagAdd(self, tag, n):
        for key in self.tags[tag]:
            self[key] += n
    
    ''' tagSub:
      * Performs subtraction on each key belonging to the given tag
    '''
    def tagSub(self, tag, n):
        self.tagAdd(tag, -n)
        
    ''' tagMul:
      * Performs multiplication on each key belonging to the given tag
    '''    
    def tagMul(self, tag, n):
        for key in self.tags[tag]:
            self[key] *= n
            
    ''' tagDiv:
      * Performs division on each key belonging to the given tag
    '''
    def tagDiv(self, tag, n):
        for key in self.tags[tag]:
            self[key] /= n
            
''' counter:
  * A special class used to track probabilities
  * supports copy, and normalization
  * defaults to 0
'''    
class counter(dict):
    ''' __missing__:
      * Defines the behavior when retrieving a key which is
      * not in self.keys(), returns 0
    '''
    def __missing__(self, key):
        return 0
        
    ''' normalize:
      * redistributes the values contained within so that they
      * will sum to 1.
    '''
    def normalize(self):
        """
        Edits the counter such that the total count of all
        keys sums to 1.  The ratio of counts for all keys
        will remain the same. Note that normalizing an empty
        Counter will result in an error.
        """
        total = float(sum(self.values()))
        if total == 0: return
        for key in self.keys():
            self[key] = self[key] / total
           
    ''' copy:
      * Returns a clone of this object
    '''
    def copy(self):
        return counter(dict.copy(self))

''' posMaxCounter:
  * A highly specialized mapping object
  * Defaults to (None, 0), and records the position
  * and value pair for each key, where the value element 
  * is the highest ever recieved for the key
'''
class pmCounter(dict):
    ''' __missing__:
      * Defines the behavior when retrieving a key which is
      * not in self.keys(), returns (None, 0)
    '''
    def __missing__(self, key):
        return (None, 0)
        
    ''' __setitem__:
      * Defines the behavior when setting a Key-Value pair
      * Sets as normal if and only if value[1]
    '''
    def __setitem__(self, key, value):
        # Type Check
        if (    type(value)    == tuple 
            and len(value)     == 2
            and type(value[0]) == tuple 
            and len(value[0])  == 2 
            and type(value[1]) == int):
            # Maintain the Max Value for value[1]
            if self[key][1] < value[1]:
                dict.__setitem__(self, key, value)
        else: raise TypeError("posMaxCounter only accepts values of the type (int, int)")
        
    ''' copy:
      * Returns a clone of this object
    '''
    def copy(self):
        return posCounter(dict.copy(self))
        
    ''' decide:
      * Randomly returns one of the most highly rated
      * key-position pairs.
    '''
    def decide(self):
        rtrn = []
        best = 0
        for key, value in self.items():
            pos, score = value
            if best < score:
                rtrn = [(key, pos)]
            elif best == score:
                rtrn += [(key, pos)]
        if len(rtrn) == 0: return None
        return choice(rtrn)
        
''' classyList:
  * A list with type based functions.
'''
class classyList(list):
    __slots__ = []       
    def __getitem__(self, key):
        if type(key) is str:
            return [item for item in self if self.isItem(item) and item.name == key][0]
        elif type(key) == int:
            return list.__getitem__(self, key)
        elif type(key) == type:
            return [value for value in self if  type(value) == key]
            
    def getClasses(self):
        return list(set([type(value) for value in self]))
        
    ''' isItem:
      * Returns true iff the SuperClass for the given item is Super Item
    '''
    def isItem(self, item):
        return type(item).__base__ is SuperItem
        
    
    ''' getWeight:
      * Returns the sum of the weight of all sub-SuperItems
    '''
    def getWeight(self, adding=0):
        return sum([item.getWeight() for item in self 
                    if self.isItem(item)]) + adding
        
''' manDistance:
  * Returns the manhattan distance between two points
  * Given two (int, int) tuples, returns an int
'''
def mDist(posA, posB):
    return abs(posA[0] - posB[0]) + abs(posA[1] - posB[1])

        
if __name__ == "__main__" and __debug__:
    ''' 
    * TESTING *
    '''
    print "\t* RUNNING TESTS: Util.py *"
    
    # Tests for the Tagon Class
    print "Tagon Tests:_______________________"
    var = tagon()
    assert var['test'] == [], "Tagon default failure"
    temp = var.copy()
    temp['james'] += ['cow']
    assert var['james'] == [], "Copy mutates source"
    var['james'] += ['duck']
    var['school'] += ['bus']
    temp['flava'] += ['flav']
    var += temp
    assert var['james'] == ["duck", "cow"], "Addition failure"
    assert var['school'] == ['bus'], "Addition failure"
    assert var['flava'] == ['flav'], "Addition failure"
    var += var
    assert var['james'] == ['duck', 'cow'], "Addition duplication"
    print "\t         Tagon Tests Passed!"
    
    # Tests for the Knowledge Class
    print "Knowledge Tests:___________________"
    var = knowledge()
    var["one"] = 0
    var["two"] = 1
    temp = var.copy()
    temp["three"] = 3
    var['one'] += 1
    var += temp
    assert var['four'] == 1,  "knowledge default failure"
    assert var['one'] == 1,   "knowledge failure 100 (+)"
    assert var['two'] == 2,   "knowledge failure 102 (+)"
    assert var['three'] == 3, "knowledge failure 103 (+)"
    var.tagAs('one', 'odd')
    var.tagAs('three', 'odd')
    var.tagAdd('odd', 2)
    assert var['odd'] == [3, 5], "knowledge failure 200 (Tag+)"
    temp = var.copy()
    temp.tagAs('two', 'even')
    var += temp
    assert var.tags.keys() == ['even', 'odd'], "knowledge failure 300 (+Tag)"
    assert var.tags['odd'] == ['one', 'three'], "knowledge failure 301 (+Tag)"
    # TODO Test additional Tag-Math Methods TODO    
    print "\t     Knowledge Tests Passed!"
    
    # Tests for the counter Class
    print "Counter Tests:_____________________"
    var = counter()
    var['simple'] += 1
    var['example'] += 2
    assert var['simple'] == 1, "counter assignment error"
    var.normalize()
    assert var['simple'] == float(1)/3, "counter normalization error"
    assert var['example'] == float(2)/3, "counter normaliztion error"
    assert var[3] == 0, "counter default error"
    print "\t       Counter Tests Passed!"
    
    # Tests for the pmCounter Class
    print "pmCounter Tests:___________________"
    var = pmCounter()
    var['test'] = ((1, 2), 3)
    assert var['test'] == ((1, 2), 3), "pmCounter assignment error"
    assert var['else'] == (None, 0), "pmCounter default error"
    var['test'] = ((2, 1), 4)
    assert var['test'] == ((2, 1), 4), "pmCounter upwards assignment error"
    var['test'] = ((1, 2), 3)
    assert var['test'] == ((2, 1), 4), "pmCounter ignored assignment error"
    print "\t     pmCounter Tests Passed!"
    # TODO: Decide testing TODO
    
    # Tests for classyList
    print "classyList Tests:__________________"
    var = classyList(['A', 1, 'B', 2, 'C', 0.2])
    assert var[int] == [1,2], "classyList error, class extraction int"
    assert var[str] == ['A', 'B', 'C'], "classyList error, class extraction str"
    assert var[float] == [0.2], "classyList error, class extraction float"
    assert var.getClasses() == list(set([str, int, float])), "classyList error, getClasses"
    print "\t    classyList Tests Passed!"
    
    # Tests for manhattan Distance
    print "mDist Tests:_______________________"
    assert mDist((4, 10), (3, 18)) == 9, "mDist error 101"
    assert mDist((2, 20), (4, 15)) == 7, "mDist error 101"
    print "\t         mDest Tests Passed!"
    
