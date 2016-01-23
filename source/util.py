#!/usr/bin/env python
""" util.py: Main game file and functions
  * Part of the IAI project.
  * Includes common functions and configurations
  * Sizes and Keybinds based around the Tkinter module
  * *
  * Last Edited: 1/22/16
"""
# IMPORTS:
from os import path, remove

#### CONSTANTS ####

""" local_path: Returns the path relative to the root folder of the project.
"""
def local_path(*plus):
    local = path.dirname(__file__)
    local = path.abspath(path.join(local, '..'))
    for p in plus: local = path.join(local, p)
    return  local
    
__DFLTCONFIG__ = local_path('config')

#### CLASSES ####

""" Config: The class which holds and manages the configuration settings.
"""
class Config(object):
    # Internal Class for handling settings
    class Mode(dict):
        __slots__ = []
        def __init__(self, t=False, s=False, i=False):
            self['testing']   = t
            self['silent']    = s
            self['invisible'] = i 
    # CONFIG body #        
    __slots__ = [ 'keys', 'mode', 'settings' ]
    """ init: the initilization function for Config objects
    """
    def __init__(self, mode=Mode(), file=__DFLTCONFIG__):
        self.mode     = mode
        self.settings = {}
        self.keys     = {}
        self.__r_config__(file)
        
    """ __r_config__: Reads the settings from the config file
      * Open, reads, and loads data from the given file into settings and keys
    """
    def __r_config__(self, file):
        # Helper function used to add the settings where they belong
        def config_add(pos, line):
            # Recursive helper funtion for getting types for config settings
            def get_type(this):
                if this.isdigit(): return int(this)
                if this[0] == '(': 
                    this_list = this[1:-1].split(',')
                    return tuple([get_type(i.strip()) for i in this_list])
                if this[0] == '[':                  
                    return [get_type(i.strip()) for i in this[1:-1].split(',')]
                if False not in [i.isalpha() for i in this.split()]: return this
            
            line = line.strip()
            if line == "" or line[0] == '#' or ':' not in line: return
            line  = line.split(':')
            name  = line[0].strip()
            value = get_type(line[1].strip())
            pos[name] = value
            
        # Open File
        file = open(file, 'r')
        thisLine = file.readline()
        # Seek out the Graphics Section (relies on Section Header)
        while 'Graphics Options' not in thisLine: thisLine = file.readline()
        # Read the graphics section
        thisLine = file.readline()
        while '####' not in thisLine:
            config_add(self.settings, thisLine)
            thisLine = file.readline()
        # Rewind and Search for Key Binds
        file.seek(0)
        thisLine = file.readline()
        while 'Keybinds Options' not in thisLine: thisLine = file.readline()
        thisLine = file.readline()
        while '####' not in thisLine:
            config_add(self.keys, thisLine)
            thisLine = file.readline()

""" Grid4Bit: A list derivative, which is used to store a grid of 4 bit ints
"""
class Grid4Bit(list):
    """ subGrid: an internal class, used to handle atypical item-setting
    """
    class subGrid(list):
        # Set Items using commands:
        def __setitem__(self, key, value):
            term = 0
            if   value ==    'Up': term = 8
            elif value ==  'Down': term = 4
            elif value ==  'Left': term = 2
            elif value == 'Right': term = 1
            else: 
                list.__setitem__(self, key, value%16)
                return
            current = list.__getitem__(self, key)
            list.__setitem__(self, key, ( current ^ term ) % 16)
        #
        def __getitem__(self, key):
            sides  = ['Right', 'Left', 'Down', 'Up']
            result = []
            value  = list.__getitem__(self, key)
            return \
                [ sides[i] for i, side in enumerate(sides) if (value >> i) & 1 ]
    
    """ __init__:
    """
    def __init__(self, x, y):
        list.__init__(self)
        self.width  = x
        self.height = y
        for col in range(x): self.append( self.subGrid([ 0 for i in range(y) ]))
            
    """ __str__:
    """
    def __str__(self):
        result = ""
        for y in range(self.height):
            row_result = ""
            for x in range(self.width): 
                value = str(list.__getitem__(self[x], y))
                row_result += ",   "[:-len(value)] + value
            result += row_result[2:] + '\n'
        return result[:-1]
            
            
""" LoopPos: A class deriving from list, which represents a looping position
  * Initialized with the maximum values (exclusive) for each position
"""
class LoopPos(list):
    __slots__ = [ 'max' ]
    """ __init__: The initialization function for a LoopPos
    """
    def __init__(self, max, start=[0, 0]):
        list.__init__(self, start)
        type_check(tuple, max)
        [ type_check(int, val) for val in max ]
        self.max = max
    """ __setitem__:
    """
    def __setitem__(self, key, value):
        list.__setitem__(self, key, value%self.max[key])
    """ __getitem__:
    """
    def __getitem__(self, key):
        return list.__getitem__(self, key)%self.max[key]

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
        global config
        # When testing is off this function becomes trivial
        if not config.mode['testing']: return
        self.run += 1 #Increment Tests Run
        sprint("Running Test: " + name)
        try:
            assert truth
        except AssertionError:
            self.failed += 1 #Increment Tests failed
            self.failed_tests += [name + ": " + message]
            sprint( "    ERROR in " + name + ": " + message )
            
    """ error_assertion: an assertion test for assertions which return an error
    """
    def error_assertion(self, name, function, error, message):
        global config
        # When testing is off this function becomes trivial
        if not config.mode['testing']: return
        self.run += 1 #Increment Tests Run
        sprint("Running Test: " + name)
        try:
            function()
        except Exception as err:
            try:
                assert type(err) == type(error)
                assert err.message == error.message
            except AssertionError:
                self.failed += 1 #Increment Tests failed
                self.failed_tests += [name + ": " + message]
                sprint( "    ERROR in " + name + ": " + message )
    
#### FUNCTIONS ####

""" __load__: performs start-up for this module.
"""
def __load__(t=False, s=False, c=None):
    global config
    # Grab Default config location when None is supplied
    if c is None: c = __DFLTCONFIG__
    config = Config(Config.Mode(t, s), file=c)
    if __name__ == '__main__' and __debug__:
        test()
        results = localTest()
        
""" alphabet: Returns a list containing all the elements of the alphabet
  * Returns a list containing all of the Key.keysym results for keys which are 
  * used in typing fields for the game.
"""
def alphabet():
    return ['a','A','b','B','c','C','d','D','e','E','f','F','g','G','h','H','i',
            'I','j','J','k','K','l','L','m','M','n','N','o','O','p','P','q','Q',
            'r','R','s','S','t','T','u','U','v','V','w','W','x','X','y','Y','z', 
            'Z','0','1','2','3','4','5','6','7','8','9','comma','period',
            'slash','backslash','space','BackSpace','colon']            
            
""" translate:
"""            
def translate(input):
    if   input == 'space':     return " "
    elif input == 'comma':     return ","
    elif input == 'slash':     return "/"
    elif input == 'period':    return "."
    elif input == 'backslash': return "\\"
    elif input == 'colon':     return ":"
    else: return input
    
""" sprint: prints the given text so long as the config isn't silenced
"""
def sprint(text):
    global config
    if not config.mode['silent']: print text
    
""" test: Switches Testing to the given state, defaults to true.
  * Activates testing through the global variable
"""
def test(set=True):
    global config
    config.mode['testing'] = set
    if not type_check(bool, set): raise TypeError()    

""" type_check: Checks that the given item is the given type(s).
  * Returns True if the item is of the given type or in the given list of types.
  * Returns False otherwise. Contains configuration check
"""    
def type_check(Type, *items):
    global config
    # When testing is off this function becomes trivial
    if not config.mode['testing']: return True
    # Begin Checks
    if type(Type) is type or type(Type).__name__ == 'classobj':
        return False not in [ item.__class__ is Type for item in items ]
    elif type(Type) is list:
        # The best line of code:
        return False not in [ True in [ item.__class__ is _type for _type in Type] for item in items ]
    else:
        typeName = Type.__name__
        errorMsg = ( "type_check given "
                    + typeName
                    + ", where it needs type or list of types" )
        raise TypeError(errorMsg)
        
#### LOCAL TESTING ####

""" localTest: the testing suite for this file
"""
def localTest():
    global config
    sprint("\n#!# LOCAL TESTS: util.py:")
    # Creating Testing Resources
    test      = Tester()
    iList     = [ 4, "hi", [1], (2, 3), False, list ]
    tList     = [ type(i) for i in iList ]
    tFileName = local_path('temp_config')
    tFile     = open(tFileName, 'w')
    tFile.write("# Graphics Options:\n Test Setting  :  123\n Other:(12,foo)\n" 
                    + "#### Keybinds Options \n #### EOF")
    tFile.close()
    tConfig = Config(file=tFileName)
    tPos    = LoopPos((5,10), (2, 3))
    # Run Tests
    # Testing: type_check:
    for i in range(len(iList)):
        test.assertion("type_check test " + str(i),
                    type_check(tList[i], iList[i]), 
                    "single item check: " + type(iList[i]).__name__)
                    
    # type_check: Type List Tests
    for i in range(len(iList)):
        test.assertion("type_check list test " + str(i),
                    type_check(tList, iList[i]), 
                    "Type-List input with: " + str(iList[i]))
                    
    # Multi-Item Test
    test.assertion("type_check item list test",
                    type_check( tList,
                                iList[0],
                                iList[1],
                                iList[2],
                                iList[3] ),
                    "Type-List, Multi-Item Input.")
                    
    # type_check: Fail Tests
    for i in range(len(tList)):
        test.assertion("type_check failure test " + str(i),
                    not type_check(tList[:i] + tList[i+1:], iList[i]), 
                    "negative test for: " + type(iList[i]).__name__)
                    
    for i in range(len(tList)):
        test.assertion("type_check multi-item failure test " + str(i),
                    not type_check( tList[:i] + tList[i+1:],
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
                            lambda: type_check(1, int),
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
    remove(local_path('temp_config'))
    
    # End Message
    sprint("Util testing Complete! Failed: [" + str(test.failed) + "/"
            + str(test.run) + "]\n")
            
    # Return testing object
    return test
    
#### SCRIPT ####
__load__()
