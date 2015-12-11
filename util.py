''' util.py: IAI Project
  * A small collection of custom mapping agents
  * Used for various tasks
  * *
  * Author(s):
  * Michael Chadbourne
  * Mateo Freyre
& * Tim Webber
  * *
  * Last Edited: 12/10/15
'''
			
class tagon(dict):
    def __missing__(self, key):
        return []

class knowledge(dict):
    self.tags = tagon()
    
    ''' __missing__:
      * Defines the behavior of retrieving a key, when the key does not exist.
      * Defaults to 1, with Feature-based-retrieval.
    '''
    def __missing__(self, key):
        if tag in self.tags.keys():
            return [ self[newkey] for newkey in self.tags[key]                
        return 1
    
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
    
class counter(dict):
    def __missing__(self, key):
        return 0
        
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