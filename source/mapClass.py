#!/usr/bin/end python
""" mapClass.py: contains the functions and classes used for the game's maps
  * part of the IAI project.
  * Used to build and represent the game's level-maps
  * *
  * Last Edited: 01/30/16
"""
# IMPORTS:
import sys, os
import util
import itemClass
from   random  import randint
from   Tkinter import *
from   PIL     import Image as Img, ImageTk
from   util    import type_check, sprint

#### CLASSES ####

""" Map: the class representation of the physical land of a level
"""
class Map(object):
    __slots__ = [ 'name', 'size', 'walls', 'spawn', 'items', 'img' ]
    
    """ __init__: The initialization function for the Map Class
      * Establishes the attributes as r/w before loading if able.
    """
    def __init__(self, name=None):
        self.name  = name
        self.walls = None
        self.spawn = None
        self.items = None
        self.img   = None
        self.size  = None
        # Load unless nameless
        if self.name != None: self.__load__()
        
    """ __save__: Saves this map to disk.
      * Records the updated background image, config file, and item-images to 
      * the disk.
    """
    def __save__(self, name=None):
        if name is None: name = self.name
        this_path = util.local_path('source/Maps/', name)
        if not os.path.exists( this_path ):
            os.makedirs( this_path )
            os.makedirs( this_path + '/items')
            for item in self.items:
                item.image.write( "%s/%s.%s"%(this_path,image.name, 'gif'),
                                                                  format='gif' )
            self.img.write(this_path + '/background.gif', format='gif')
        temp_file = open(this_path + '/config', 'w')
        temp_file.write("%d, %d\n\n" % (self.size[0], self.size[1]))
        temp_file.write(str(self.walls) + '\n\n')
        temp_file.write(str(self.spawn))

    """ __load__: Loads this object from disk
      * Instantiates this object with the values from the Map folder baring its
      * name. Loads from the config file and various image files.
    """
    def __load__(self):
        this_path  = util.local_path('source/Maps/' + self.name)
        self.img   = PhotoImage(file=this_path + '/background.gif')
        temp_file  = open(           this_path + '/config', 'r')   # FILE OPENED
        # Read from the load file
        x, y       = temp_file.readline().split(',')               # READ LINE 1
        self.size  = (int(x), int(y))
        line       = temp_file.readline()                          # READ LINE 2
        self.walls = util.BitGrid(int(x), int(y))
        self.spawn = util.Grid(int(x), int(y))
        self.items = []
        # READ WALLS ##############################################<#<#<#<#<#<#<
        for row in range(self.size[1]):                            
            line = temp_file.readline()
            for col, value in enumerate(line.split(",")):
                self.walls[col][row] = int(value)
        line = temp_file.readline()                                # READ DIVIDE
        # READ ITEM SPAWNS ########################################<#<#<#<#<#<#<
        item_count = 0
        for row in range(self.size[1]): 
            line = temp_file.readline()
            for col, value in enumerate(line.split(",")):
                self.spawn[col][row] = int(value)
                item_count = max(item_count, int(value))              
        line = temp_file.readline()                                # READ DIVIDE
        # READ ITEM DEFENITIONS ###################################<#<#<#<#<#<#<
        for item in range(item_count):
            self.__load_item__(temp_file)
        temp_file.close()                                          # CLOSE  FILE
            
    """ __load_item__: Loads an item, adding it to this map
      * Loads in a items information using the given open-config-file
      * TODO change to reflect the ITEM class.
    """
    def __load_item__(self, file):
        title_line = file.readline()                              #  READ  TITLE
        _type, item_name  = title_line.split(':')
        args = {}
        arg_line = file.readline()                                # READ ARG(S)
        while '}' not in arg_line:
            key, value = arg_line.split(':')
            args[key] = value
            arg_line = file.readline()
        self.items += [ itemClass.MapItem(self.name, item_name, _type, args) ]
            
    """ __create__: Creates a blank map file with the given name on the disk
      * Using the supplied name, file location, and tile-dimensions, creates and
      * appropriate MAP file on the hard disk, with blank grid positions and no
      * item defenitions.
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
        os.makedirs( this_path + '/items')
        # Save Background
        temp_file.save( this_path + '/background.gif' )
        temp_file.close()
        # Write Config
        temp_file = open( this_path + '/config', 'w')
        ## Write Dimensions
        temp_file.write("%d, %d\n\n" % (size[0], size[1]))
        ## Write wall positions
        for i in range(size[1]):
            temp_file.write((' 0,' * size[0])[1:-1] + '\n')
        temp_file.write('\n')
        ## Write Object Start positions
        for i in range(size[1]):
            temp_file.write((' 0,' * size[0])[1:-1] + '\n')
        temp_file.write('\n')
        ## Write Object Defenitions: None
        ## Close config file and load from created files. 
        temp_file.close()
        self.__load__()

#### FUNCTIONS ####

### SCRIPT ####
            
        
        
