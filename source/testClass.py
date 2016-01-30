#!/usr/bin/end python
""" testClass.py
  * part of the IAI project. Performs testing on the IAI modules.
  * *
  * Last Edited: 01/30/16
"""
# IMPORTS:
import util
from os     import path, remove
from shutil import rmtree
from random import randint

file_name = '__temp__'
temp_path = util.local_path('source/Maps/' + file_name)

#### CLASSES ####

""" Tester: class used for testing a section of source code.
  * Runs assertions well tracking the tests run and failed.
"""        
class Tester():
    # Storage for the results:
    run          = 0
    failed       = 0
    failed_tests = []
    
    """ assertion: an assertion test with accompanying (s)print statements
    """
    def assertion(self, name, truth, message):
        # When testing is off this function becomes trivial
        if not util.config.mode['testing']: return
        self.run += 1 #Increment Tests Run
        util.sprint("Running Test: " + name)
        try:
            assert truth
        except AssertionError:
            self.failed += 1 #Increment Tests failed
            self.failed_tests += [name + ": " + message]
            util.sprint( "    ERROR in " + name + ": " + message )
            
    """ error_assertion: an assertion test for assertions which return an error
    """
    def error_assertion(self, name, function, error, message):
        # When testing is off this function becomes trivial
        if not util.config.mode['testing']: return
        self.run += 1 #Increment Tests Run
        util.sprint("Running Test: " + name)
        try:
            function()
        except Exception as err:
            try:
                assert type(err) == type(error)
                assert err.message == error.message
            except AssertionError:
                self.failed += 1 #Increment Tests failed
                self.failed_tests += [name + ": " + message]
                util.sprint( "    ERROR in " + name + ": " + message )

#### FUNCTIONS ####

"""
"""
def clean_map(dir_name):
    dir_path = util.local_path('source/Maps/' + dir_name)
    if path.exists(dir_path): rmtree(dir_path)

"""
"""
def test_util():
    util.sprint("\n#!# LOCAL TESTS: util.py:")
    # Creating Testing Resources
    test      = Tester()
    iList     = [ 4, "hi", [1], (2, 3), False, list ]
    tList     = [ type(i) for i in iList ]
    tFileName = util.local_path('temp_config')
    tFile     = open(tFileName, 'w')
    tFile.write("# Graphics Options:\n Test Setting  :  123\n Other:(12,foo)\n" 
                    + "#### Keybinds Options \n #### EOF")
    tFile.close()
    tConfig = util.Config(file=tFileName)
    tPos    = util.LoopPos((5,10), (2, 3))
    # Run Tests
    # Testing: type_check:
    for i in range(len(iList)):
        test.assertion("type_check test " + str(i),
                    util.type_check(tList[i], iList[i]), 
                    "single item check: " + type(iList[i]).__name__)
                    
    # type_check: Type List Tests
    for i in range(len(iList)):
        test.assertion("type_check list test " + str(i),
                    util.type_check(tList, iList[i]), 
                    "Type-List input with: " + str(iList[i]))
                    
    # Multi-Item Test
    test.assertion("type_check item list test",
                    util.type_check( tList,
                                iList[0],
                                iList[1],
                                iList[2],
                                iList[3] ),
                    "Type-List, Multi-Item Input.")
                    
    # type_check: Fail Tests
    for i in range(len(tList)):
        test.assertion("type_check failure test " + str(i),
                    not util.type_check(tList[:i] + tList[i+1:], iList[i]), 
                    "negative test for: " + type(iList[i]).__name__)
                    
    for i in range(len(tList)):
        test.assertion("type_check multi-item failure test " + str(i),
                    not util.type_check( tList[:i] + tList[i+1:],
                                    iList[0],
                                    iList[1],
                                    iList[2],
                                    iList[3],
                                    iList[4],
                                    iList[5] ), 
                    "negative test excluding: " + type(iList[i]).__name__)
                    
    # type_check: Exception Test
    errorMsg = "type_check given int, where it needs type or list of types"
    test.error_assertion("type_check exception test",
                            lambda: util.type_check(1, int),
                            TypeError(errorMsg),
                            "exception test")
                            
    # Testing config file reader:
    test.assertion("Config file test 0",
                    tConfig.settings['Test Setting'] == 123,
                    "Integer setting failed to load" )
                    
    test.assertion("Config file test 1",
                    type(tConfig.settings['Other']) is tuple,
                    "Tuple type not discovered" )
                    
    test.assertion("Config file test 2",
                    type(tConfig.settings['Other'][0]) is int,
                    "Integer type not discovered" )
                    
    test.assertion("Config file test 3",
                    type(tConfig.settings['Other'][1]) is str,
                    "Str type not Discovered" )
    # Testing LoopPos:
    test.assertion("LoopPos Starting Value Test",
                    tPos[0] == 2 and tPos[1] == 3,
                    "Starting values mismatched")
    tPos[0] += 11
    tPos[1] -= 19
    test.assertion("LoopPos Addition Test",
                    tPos[0] == 3 and tPos[1] == 4,
                    "Addition didn't loop correctly")
    
    
    
    # Clean-up testing resources
    remove(util.local_path('temp_config'))
    
    # End Message
    util.sprint("Util testing Complete! Failed: [" + str(test.failed) + "/"
            + str(test.run) + "]")
            
    # Return testing object
    return test

def test_maps():
    import mapClass as m
    util.sprint("\n#!# LOCAL TESTS: mapClass.py:")
    # Creating Testing Resources
    test = Tester()
    root = m.Tk()
    # Attempt to create Map Class
    try:
        test_map = m.Map()
    except Exception as err:
        util.sprint("Failed to Initialize map::Terminating")
        return
    # Attempt to make that Map class realize it's potential
    try:
        test_map.__create__(util.local_path("rsc/basicMap.gif"),
                            '__temp__',
                            (10, 5))
    except Exception as err:
        util.sprint("Failed to Create Map::Terminating")
        return
    #Test creation
    test.assertion("Directory creation test",
                    path.exists(temp_path),
                    "Failed to create directory")
    test.assertion("Background creation test",
                    path.exists(temp_path + '/background.gif'),
                    "Failed to create Background image")
    test.assertion("Config creation test",
                    path.exists(temp_path + '/config'),
                    "Failed to create Config File")
    # Rearrange testing resources:
    for i in range(10):
        test_map.walls[randint(0,9)][randint(0,4)] = i
    #try:
    test_map.__save__('__temp2__')
    temp_map = m.Map('__temp2__')
    #except Exception as err:
    #    sprint("Failed during Load/Save")
    # Continue testing:
    test.assertion("Save/Load test",
                    test_map.walls == temp_map.walls,
                    "Grid comparison failed, ")
    # Cleanup testing resources:
    clean_map(file_name)
    clean_map('__temp2__')
    root.destroy()
        
    # End Message
    util.sprint("Map Class testing Complete! Failed: [" + str(test.failed) + "/"
            + str(test.run) + "]")
            
    # Return Testing Object
    return test
 
def test_engine():
    import engineClass as e
    util.sprint("\n#!# LOCAL TESTS: engineClass.py:")
    # Creating Testing Resources
    up, down, left, right, select = [lambda: e.Event() for i in range(5)]
    test          = Tester()
    up.keysym     = 'Up'
    down.keysym   = 'Down'
    left.keysym   = 'Left'
    right.keysym  = 'Right'
    select.keysym = 'Return'

    # Run a Simulation of the Editor
    try:
        util.sprint("Creating Editor Simulation")
        # Build and Handle Prompt 1
        engine = e.Engine(e.ImgFileName, "Testing!")
        key    = e.Event()
        util.sprint("Simulating Image location prompt")
        for char in util.local_path("rsc/basicMap.gif"):
            if char == '.':    char = 'period'
            elif char == '\\': char = 'backslash'
            elif char == ':':  char = 'colon'
            elif char == '/':  char = 'slash'
            key.keysym = char
            engine.GUI.mode.__keypress__(key)
        engine.GUI.mode.__keypress__(select)
    except:
        util.sprint("Excepetion raised during prompt simulation 1")
    test.assertion("ImgFileName completion test", 
                    util.type_check(e.NewFileName, engine.GUI.mode),
                    "Prompt failed to advance " + str(type(engine.GUI.mode)))
    # Handle Prompt 2
    try:
        util.sprint("Simulating new file name prompt")
        for char in file_name:
            if char == '_': char = 'underscore'
            key.keysym = char
            engine.GUI.mode.__keypress__(key)
        engine.GUI.mode.__keypress__(select)
    except:
        util.sprint("Exception raised during prompt simulation 2")
    test.assertion("NewFileName completion test",
                    util.type_check(e.TileDimension, engine.GUI.mode),
                    "Prompt failed to advance")
    # Handle Prompt 3
    try:        
        util.sprint("Simulating tile dimension prompt")
        for char in "10,11":
            if char == ',': char = 'comma'
            key.keysym = char
            engine.GUI.mode.__keypress__(key)
        engine.GUI.mode.__keypress__(select)
    except:
        util.sprint("Exception raised during prompt simulation 3")
    test.assertion("TileDimension completion test",
                    util.type_check(e.Editor, engine.GUI.mode),
                    "Prompt failed to advance")
    # Handle Main Editor:
    try:
        # Placing a 5 in [9][8] and a 4 in [9][10]
        util.sprint("Simulating main Editor")
        engine.GUI.mode.__keypress__(up)
        engine.GUI.mode.__keypress__(left)
        engine.GUI.mode.__keypress__(select)
        engine.GUI.mode.__keypress__(down)
        engine.GUI.mode.__keypress__(right)
        engine.GUI.mode.__keypress__(select)
        engine.GUI.mode.__keypress__(up)
        engine.GUI.mode.__keypress__(up)
        engine.GUI.mode.__keypress__(select)
        engine.GUI.mode.__keypress__(down)
        engine.GUI.mode.__keypress__(select)
        key.keysym = 'BackSpace'
        engine.GUI.mode.__keypress__(key)
        engine.GUI.mode.__keypress__(down)
        engine.GUI.mode.__keypress__(down)
    except: 
        util.sprint("Exception raised during prompt simulation 3")
    engine.GUI.mode.__keypress__(select)
    try:
        test_file = open( temp_path + '/config' )
    except: util.sprint("Exception raised while reading config file")
    contents = test_file.readlines()
    test.assertion("config contents test",
                    int(contents[10].split(",")[9]) == 4 
                        and int(contents[12].split(",")[9]) == 5,
                    "bad config file contents")
                    
    # Clean-up testing resources
    test_file.close()
    clean_map(file_name)
    
    # End Message
    util.sprint( "Engine testing Complete! Failed: [" + str(test.failed) + "/"
            + str(test.run) + "]" )
            
    # Return testing object
    return test
    
### SCRIPT ####

if __name__ == '__main__':
    util.test()
    util_test = test_util()
    clean_map(file_name)
    clean_map('__temp2__')
    util_test = test_maps()
    clean_map(file_name)
    util_test = test_engine()