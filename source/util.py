#!/usr/bin/env python
""" util.py: Main game file and functions
  * Part of the IAI project.
  * Includes common functions and configurations
  * Sizes and Keybinds based around the Tkinter module
  * *
  * Last Edited: 01/31/16
"""
# IMPORTS:
from os  import path
from PIL import Image, ImageTk

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

""" Grid: A collection, sorted into a grid.
  * The grid is Accessed using [x][y] and is initialized using the height, width
  * and the default value. Defaulting to 0, 0, and None respectivly.
"""
class Grid(list):
    
    def __init__(self, x=0, y=0, default=None):
        list.__init__(self, [[default] * y for i in range(x)])
        self.width  = x
        self.height = y
        
    def __str__(self):
        rtrn = ""
        for row in range(self.height):
            row_str = ""
            for column in range(self.width):
                row_str += "%s, " % (str(list.__getitem__(self[column], row)))
            rtrn += row_str[:-2] + "\n"
        return rtrn[:-1]

""" BitList: The Binary List structure used for BitGrid.
"""
class BitList(list):
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
    # Returns the bit value as the list of strings it represents
    def __getitem__(self, key):
        sides  = ['Right', 'Left', 'Down', 'Up']
        result = []
        value  = list.__getitem__(self, key)
        return [ sides[i] for i in range(len(sides)) if (value >> i) & 1 ]

""" BitGrid: A storage class specifically for storing the Wall Positions
  * Stores the poisitons of the walls as a 4Bit int. Recovering the wall names 
  * when being accessed through __getitem__  
"""        
class BitGrid(Grid):
    def __init__(self, x=1, y=1, default=0):
        list.__init__(self, [BitList([default] * y) for i in range(x)])
        self.width  = x
        self.height = y
    
""" LoopPos: A class deriving from list, which represents a looping position
  * Initialized with the maximum values (exclusive) for each position
  * TODO: use Grid as base. (involves switching out max in code)
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
    
#### FUNCTIONS ####
     
""" alphabet: Returns a list containing all the elements of the alphabet
  * Returns a list containing all of the Key.keysym results for keys which are 
  * used in typing fields for the game.
"""
def alphabet():
    return ['a','A','b','B','c','C','d','D','e','E','f','F','g','G','h','H','i',
            'I','j','J','k','K','l','L','m','M','n','N','o','O','p','P','q','Q',
            'r','R','s','S','t','T','u','U','v','V','w','W','x','X','y','Y','z', 
            'Z','0','1','2','3','4','5','6','7','8','9','comma','period',
            'slash','backslash','space','BackSpace','colon', 'underscore']            
          
""" load_image: Loads an Image from file, into the desired size.
"""
def load_image(file_name, dimensions=None, alt=False):
    image_file = Image.open(file_name)
    if dimensions != None: image_file = image_file.resize(dimensions)
    if alt: image_file = ImageTk.PhotoImage(image_file)
    return image_file
   
""" translate: Translates Tkinter key names into the character they represent
"""            
def translate(input):
    if   input == 'space':     return " "
    elif input == 'comma':     return ","
    elif input == 'slash':     return "/"
    elif input == 'period':    return "."
    elif input == 'backslash': return "\\"
    elif input == 'colon':     return ":"
    elif input == 'underscore': return "_"
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
        typeName = type(Type).__name__
        errorMsg = ( "type_check given "
                    + typeName
                    + ", where it needs type or list of types" )
        raise TypeError(errorMsg)
        
""" __load__: performs start-up for this module.
"""
def __load__(t=False, s=False, c=None):
    global config
    # Grab Default config location when None is supplied
    if c is None: c = __DFLTCONFIG__
    config = Config(Config.Mode(t, s), file=c)
#### SCRIPT ####
__load__()
