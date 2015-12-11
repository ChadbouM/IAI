#IMPORTS: None

''' util.py: IAI Project
  * A small collection of custom mapping agents 
  * and other utilities used for various tasks
  * *
  * Author(s):
  * Michael Chadbourne
  * Mateo Freyre
& * Tim Webber
  * *
  * Last Edited: 12/10/15
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
    
    #Tests for the Tagon Class
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
    print "\t        Passed Tagon Tests!"
    
    #Tests for the Knowledge Class
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
    print "\t    Passed Knowledge Tests!"
    
    #Tests for the counter Class
    print "Counter Tests:_____________________"
    var = counter()
    var['simple'] += 1
    var['example'] += 2
    assert var['simple'] == 1, "counter assignment error"
    var.normalize()
    assert var['simple'] == float(1)/3, "counter normalization error"
    assert var['example'] == float(2)/3, "counter normaliztion error"
    assert var[3] == 0, "counter default error"
    print "\t      Passed Counter Tests!"
    
    #Tests for manhattan Distance
    print "mDist Tests:_______________________"
    assert mDist((4, 10), (3, 18)) == 9, "mDist error 101"
    assert mDist((2, 20), (4, 15)) == 7, "mDist error 101"
    print "\t        Passed mDest Tests!"
    
