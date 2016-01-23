#!/usr/bin/end python
""" mapClass.py: contains the functions and classes used for the game's maps
  * part of the IAI project.
  * Used to build and represent the game's level-maps
  * *
  * Last Edited: 01/18/16
"""
# IMPORTS:
import sys, os
import util
from   random  import randint
from   Tkinter import *
from   PIL     import Image as Img, ImageTk
from   util    import type_check, sprint

#### CLASSES ####

""" Map: the class representation of the physical land of a level
"""
class Map(object):
    __slots__ = [ 'name', 'size', 'grid', 'img' ]
    """ __init__:
    """
    def __init__(self, name=None):
        self.name = name
        self.grid = None
        self.img  = None
        self.size = None
        if self.name != None: self.__load__()
        
    """ __save__:
    """
    def __save__(self, name=None):
        if name is None: name = self.name
        this_path = util.local_path('source/Maps/', name)
        if not os.path.exists( this_path ):
            os.makedirs( this_path )
            self.img.write(this_path + '/background.gif', format='gif')
        temp_file = open(this_path + '/config', 'w')
        temp_file.write("%d, %d\n\n" % (self.size[0], self.size[1]))
        temp_file.write(str(self.grid))
               
    """ __load__:
    """
    def __load__(self):
        this_path = util.local_path('source/Maps/' + self.name)
        self.img  = PhotoImage(file=this_path + '/background.gif')
        temp_file = open(           this_path + '/config', 'r')
        # Read from the load file
        x, y      = temp_file.readline().split(',')
        self.size = (int(x), int(y))
        line      = temp_file.readline()
        self.grid = util.Grid4Bit(int(x), int(y))
        for row in range(self.size[1]):
            line = temp_file.readline()
            for col, value in enumerate(line.split(",")):
                self.grid[col][row] = int(value)
            
    """ __create__:
    """     
    def __create__(self, file, name, size):
        # Open the generation Image:
        temp_file = Img.open(file)
        temp_file = temp_file.resize(util.config.settings['Screen_Size'])
        # Create new Folder
        self.name = name
        this_path = util.local_path('source/Maps', self.name)
        if os.path.exists( this_path ): return -1
        os.makedirs( this_path )
        temp_file.save( this_path + '/background.gif' )
        temp_file.close()
        temp_file = open( this_path + '/config', 'w')
        temp_file.write("%d, %d\n\n" % (size[0], size[1]))
        for i in range(size[1]):
            temp_file.write((' 0,' * size[0])[1:-1] + '\n')
        temp_file.close()
        self.__load__()
        

#### FUNCTIONS ####

#### LOCAL TESTING ####

""" localTest: Performs testing local to this source file.
"""
def localTest(): 
    sprint("\n#!# LOCAL TESTS: mapClass.py:")
    # Creating Testing Resources
    test = util.Tester()
    root = Tk()
    # Attempt to create Map Class
    try:
        test_map = Map()
    except Exception as err:
        sprint("Failed to Initialize map::Terminating")
        return
    # Attempt to make that Map class realize it's potential
    try:
        test_map.__create__(util.local_path("rsc/basicMap.gif"),
                            '__temp__',
                            (10, 5))
    except Exception as err:
        sprint("Failed to Create Map::Terminating")
        return
    # Test creation
    temp_path = util.local_path('source/Maps/__temp__')
    test.assertion("Directory creation test",
                    os.path.exists(temp_path),
                    "Failed to create directory")
    test.assertion("Background creation test",
                    os.path.exists(temp_path + '/background.gif'),
                    "Failed to create Background image")
    test.assertion("Config creation test",
                    os.path.exists(temp_path + '/config'),
                    "Failed to create Config File")
    # Rearrange testing resources:
    for i in range(10):
        test_map.grid[randint(0,9)][randint(0,4)] = i
    try:
        test_map.__save__('__temp2__')
        temp_map = Map('__temp2__')
    except Exception as err:
        sprint("Failed during Load/Save")
    # Continue testing:
    test.assertion("Save/Load test",
                    test_map.grid == temp_map.grid,
                    "Grid comparison failed, ")
    # Cleanup testing resources:
    try:
        os.remove(util.local_path('source/Maps/__temp__/config'))
        os.remove(util.local_path('source/Maps/__temp__/background.gif'))
        os.rmdir( util.local_path('source/Maps/__temp__' ))
        os.remove(util.local_path('source/Maps/__temp2__/config'))
        os.remove(util.local_path('source/Maps/__temp2__/background.gif'))
        os.rmdir( util.local_path('source/Maps/__temp2__' ))
    except Exception as err:
        sprint("Failed removing temp files.")
        
    # End Message
    sprint("Map Class testing Complete! Failed: [" + str(test.failed) + "/"
            + str(test.run) + "]\n")
            
    # Return Testing Object
    return test
        

    

### SCRIPT ####
 
if __name__ == '__main__':
        util.test()
        results = localTest()
            
        
        
