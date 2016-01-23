#!/usr/bin/end python
""" engineClass.py: the Tkinter based graphical engine used for the Game
  * Part of the IAI project.
  * *
  * Last Edited: 1/18/16
"""
# IMPORTS:
from   os        import path, remove, rmdir
from   Tkinter   import * 
from   gameClass import GameState
import util
import time


#### CLASSES ####
        
######## GUI MODES ########
    
""" Mode: The class representation of a GUI-mode; a Template
  * The mode handles a paticular screen in the GUI, being packed and forgotten
  * as the screen enters and leaves focus respectively, handles keys and drawing
"""
class Mode(Canvas):
    """ __call__: The call function; used for Switching
      * If inbound is False it will switch this mode out of its master
      * If, as is Default, it is True:
      * Then it will switch this module in to its master
    """
    def __call__(self, inbound=True):
        if inbound:
            self.pack(expand=True, fill='both')
        else:
            self.forget()

    """ __init__: The Initialization function for Mode
      * The default function, sets size, and the ID containers.
    """
    def __init__(self, master):
        Canvas.__init__(self, master)
        self['width'], self['height'] = util.config.settings['Screen_Size']
        self.bgis = [] # BackGround IdentifierS
        self.mvis = [] # MoVing IdentifierS
        
    """ __keypress__: Handles Keypress events
      * A Template for the Required __keypress__ function
    """
    def __keypress__(self, event):
        print "MODE: Not Implemented: " + event.keysym
        
""" Prompt: The class representation a Prompt Screen; a Mode Template
  * This mode creates a prompt screen for the given message
  * 
"""
class Prompt(Mode):
    """ __init__:
    """
    def __init__(self, master, question):
        Mode.__init__(self, master)
        self.text     = ""
        # Prompt Box Coordinate Calc:
        size = (300, 20)
        center_x = int(self['width'])/2
        center_y = int(self['height'])/2
        nw   = (center_x - size[0]/2, center_y - size[1]/2)
        se   = (center_x + size[0]/2, center_y + size[1]/2)
        # Setup Starting Graphic:
        self['bg'] = 'black'
        self.bgis += [self.create_text((nw[0], nw[1] - 20),
                                        text = question,
                                        anchor='w',
                                        font = util.config.settings['Font'],
                                        fill = 'white')]
        self.bgis += [self.create_rectangle( nw + se,
                                              outline = 'white',
                                              width   = 3) ]
        
    """ __keypress__
    """
    def __keypress__(self, event):
        if   event.keysym == 'Return':        self.__select__()
        elif event.keysym == 'BackSpace':     self.text = self.text[:-1]
        elif event.keysym in util.alphabet(): self.text += \
                                                    util.translate(event.keysym)
        else:                                 return
        [ self.delete(id) for id in self.mvis ]
        
        self.mvis += [ self.create_text(
                                        (   int(self['width'] )/2 - 145,
                                            int(self['height'])/2),
                                        text   = self.text,
                                        font   = util.config.settings['Font'],
                                        anchor = 'w',
                                        fill   = 'white' ) ]
    
    """ __select__: Preforms the Return key command 
      * Ends the prompt, moving on to the next mode; This is a template
    """
    def __select__(self):
        print "__select__ not implemented"

""" ImgFileName: The prompt-class for the File Location prompt
  * A full mode; Asks for the file location of the background image.
"""
class ImgFileName(Prompt):
    errored = False
    def __init__(self, master):
        prompt = "What image shall we use?"
        Prompt.__init__(self, master, prompt)
    def __select__(self):
        if path.exists(self.text):
            next_mode = NewFileName(self.master)
            next_mode.load_from = self.text
            self.master(next_mode)
        # If Input is Invalid
        else:
            self.text = ""
            if not self.errored:
                self.errored = True
                self.create_text(
                                (   int(self['width'] )/2,
                                    int(self['height'])/2 + 20),
                                text   = "File Not Found! Try Again.",
                                font   = util.config.settings['Font'],
                                fill   = 'white' )
""" NewFileName: The prompt-class for the new Map name.
  * A full mode; Asks for the new directory name to be associated with this map
"""
class NewFileName(Prompt):
    errored = False
    def __init__(self, master):
        prompt = "What will this Map be called?"
        Prompt.__init__(self, master, prompt)
    def __select__(self):
        if not path.exists(util.local_path('source/Maps', self.text)):
            next_mode           = TileDimension(self.master)
            next_mode.load_from = self.load_from
            next_mode.load_to   = self.text
            self.master(next_mode)    
        # If input is invalid:
        else:
            self.text = ""
            if not self.errored:
                self.errored = True
                self.create_text(
                                (   int(self['width'] )/2,
                                    int(self['height'])/2 + 20),
                                text   = "Already Exists! Try Again.",
                                font   = util.config.settings['Font'],
                                fill   = 'white' )
""" TileDimension: The prompt-class for the Tile dimensions Prompt
  * A full mode; Asks for the dimension of the map in terms of tiles.
"""
class TileDimension(Prompt):
    errored = False
    def __init__(self, master):
        prompt = "What size is this map in terms of tiles '#, #'?"
        Prompt.__init__(self, master, prompt)
    def __select__(self):
        # Test for valid Input
        try:
            x, y = [int(var) for var in self.text.split(",")]
        except Exception as err:
            self.text = ""
            if not self.errored:
                self.errored = True
                msg = "Bad Format! Try Again. (ex. 10, 10)"
                self.create_text(
                                (   int(self['width'] )/2,
                                    int(self['height'])/2 + 20),
                                text   = msg,
                                font   = util.config.settings['Font'],
                                fill   = 'white' )
            return # return after Exception
        # If  Valid, continue to Editor:
        self.master.host.game.level.map.__create__(self.load_from,
                                                    self.load_to,
                                                    (x, y))
        next_mode = Editor(self.master)
        self.master(next_mode)
""" SaveAs: The prompt-class for the saveAs screen.
  * A full mode; Asks for the new directory name to be associated with this map
"""
class SaveAs(Prompt):
    errored = False
    def __init__(self, oldMode):
        prompt = "Save As:"
        Prompt.__init__(self, oldMode.master, prompt)
        self.old = oldMode
    def __select__(self):
        if not path.exists(util.local_path('source/Maps', self.text)):
            self.old.menu = False
            self.old.map.__save__(self.text)
            self.old.map.name = self.text
            self.old.draw()
            self.master(self.old)    
        # If input is invalid:
        else:
            self.text = ""
            if not self.errored:
                self.errored = True
                self.create_text(
                                (   int(self['width'] )/2,
                                    int(self['height'])/2 + 20),
                                text   = "Already Exists! Try Again.",
                                font   = util.config.settings['Font'],
                                fill   = 'white' )
""" 
"""
class LoadMapName(Prompt):
    errored = False
    def __init__(self, master):
        prompt = "Load Map:"
        Prompt.__init__(self, master, prompt)
    def __select__(self):
        if path.exists(util.local_path('source/Maps', self.text)):
            self.master.host.game.level.map.name = self.text
            self.master.host.game.level.map.__load__()
            self.master(Editor(self.master)) #This looks Sick-lical, it isn't    
        # If input is invalid:
        else:
            self.text = ""
            if not self.errored:
                self.errored = True
                self.create_text(
                                (   int(self['width'] )/2,
                                    int(self['height'])/2 + 20),
                                text   = "Map not Found! Try Again.",
                                font   = util.config.settings['Font'],
                                fill   = 'white' )
                                
""" Editor:
"""
class Editor(Mode):
    lock       = False
    menu       = False
    menu_items = [ 'Save', 'Save As', 'Save and Exit', 'Exit' ]
    menu_pos   = util.LoopPos((1, len(menu_items)))
    
    """ __init__:
    """
    def __init__(self, master):
        Mode.__init__(self, master)
        self.map = self.master.host.game.level.map
        self.bgis += [self.create_image((0, 0),
                                        image=self.map.img,
                                        anchor='nw')]
        self.size   = self.map.size
        self.posit  = util.LoopPos(self.size)
        # Draw Grid:
        width       = int(self['width'])
        height      = int(self['height'])
        tile_width  = width/self.size[0]
        tile_height = height/self.size[1]
        for tile in range(1, self.size[0]):
            tile_x = tile_width * tile
            self.bgis += [self.create_line((tile_x, 0, tile_x, height),
                                                fill = 'black')]
        for tile in range(1, self.size[1]):
            tile_y = tile_height * tile
            self.bgis += [self.create_line((0, tile_y, width, tile_y),
                                                fill = 'black')]
        self.draw()
    
    """ __keypress__: The keypress handler of the Editor mode
      * Handles switching between sub modes, wall-assignment, tile-selection,
      * and Menu.
    """
    def __keypress__(self, event):
        if   event.keysym in util.config.keys['Menu_Up']:     
            if   self.lock: self.map.grid[self.posit[0]][self.posit[1]] =   'Up'
            elif self.menu: self.menu_pos[1] -= 1
            else:
                self.posit[1] -= 1
        elif event.keysym in util.config.keys['Menu_Down']:
            if   self.lock: self.map.grid[self.posit[0]][self.posit[1]] = 'Down'
            elif self.menu: self.menu_pos[1] += 1
            else:
                self.posit[1] += 1
        elif event.keysym in util.config.keys['Menu_Left']:
            if   self.lock: self.map.grid[self.posit[0]][self.posit[1]] = 'Left'
            elif self.menu: pass
            else:
                self.posit[0] -= 1
        elif event.keysym in util.config.keys['Menu_Right']:
            if   self.lock: self.map.grid[self.posit[0]][self.posit[1]] ='Right'
            elif self.menu: pass
            else:
                self.posit[0] += 1
        elif event.keysym in util.config.keys['Menu_Select']: 
            if self.__select__() == -1: return
        elif event.keysym in util.config.keys['Menu_Back']:   self.__back__()
        self.draw()
        
    """ __select__: Handles the selection key callback
      * Manages the multiple states of the editor, default/locked/menu-open
      * Working with Back to pass between them
    """
    def __select__(self):
        if self.lock:   self.lock = False
        elif self.menu:
            if self.menu_items[self.menu_pos[1]] == 'Save': self.map.__save__()
            elif self.menu_items[self.menu_pos[1]] == 'Save As': 
                self.master(SaveAs(self))
            elif self.menu_items[self.menu_pos[1]] == 'Save and Exit':
                self.map.__save__()
                self.master.quit()
                self.master.master.destroy()
                if not util.config.mode['testing']: quit()
                return -1
            elif self.menu_items[self.menu_pos[1]] == 'Exit':
                self.master.quit()
                self.master.master.destroy()
                if not util.config.mode['testing']: quit()
                return -1
        else:      self.lock = True
            
    """__back__:
    """
    def __back__(self):
        if self.lock:   self.lock = False
        elif self.menu: self.menu = False
        else:
                        self.menu_pos[1] = 0
                        self.menu = True
        
    def draw(self):
        [ self.delete(id) for id in self.mvis ]
        width       = int(self['width'])
        height      = int(self['height'])
        tile_width  = width/self.size[0]
        tile_height = height/self.size[1]
        tile_x      = self.posit[0] * tile_width
        tile_y      = self.posit[1] * tile_height
        # Determine Border Color
        if self.lock: color = 'blue'
        else:         color = 'black'
        # Draw Upper Boundary
        self.mvis += [self.create_rectangle(
                                (   tile_x,
                                    tile_y,
                                    tile_x + tile_width,
                                    tile_y + tile_height),
                                outline = color,
                                width = 3)]
        # Draw The Walls!
        for x in range(self.size[0]):
            for y in range(self.size[1]):
                self.draw_bounds(x, y, self.map.grid[x][y])
                
        if self.menu:
            # Draw Menu-Box on right:
            self.mvis += [self.create_rectangle(
                                    (width - 250, 0, width, height),
                                    fill    = 'black',
                                    outline = 'white',
                                    width   = 5.0 )]
            # Draw Menu Text:
            for i, item in enumerate(self.menu_items):
                self.mvis += [self.create_text(
                                       (width - 125, height*0.25 + 75 * i),
                                       text = item,
                                       font = \
                                          (util.config.settings['Font'][0], 26),
                                       fill = 'white' )]
            # Draw Selection Box:
            self.mvis += [self.create_rectangle(
                                    (   width - 225,
                                        height*0.25-20 + 75*self.menu_pos[1],
                                        width - 25,
                                        height*0.25+20 + 75*self.menu_pos[1]),
                                    outline = 'white',
                                    width   = 2.0 )]
                                       
            
                
    # Helper for draw which draws the walls            
    def draw_bounds(self, col, row, item):
        width       = int(self['width'])
        height      = int(self['height'])
        tile_width  = width/self.size[0]
        tile_height = height/self.size[1]
        tile_x      = col * tile_width
        tile_y      = row * tile_height
        color = 'red'
        
        if 'Up' in item:
        # Draw Upper Boundary
            self.mvis += [self.create_line(
                                    (   tile_x + 2,
                                        tile_y + 2,
                                        tile_x + tile_width - 2,
                                        tile_y + 2),
                                    fill = color,
                                    width = 3)]
        if 'Down' in item:
        # Draw Lower Boundary
            self.mvis += [self.create_line(
                                    (   tile_x + 2,
                                        tile_y + tile_height - 2,
                                        tile_x + tile_width  - 2,
                                        tile_y + tile_height - 2),
                                    fill = color,
                                    width = 3)]
        if 'Left' in item:
        # Draw Left Boundary
            self.mvis += [self.create_line(
                                    (   tile_x + 2,
                                        tile_y + 2,
                                        tile_x + 2,
                                        tile_y + tile_height - 2),
                                    fill = color,
                                    width = 3)]
        if 'Right' in item:
        # Draw Right Boundary
            self.mvis += [self.create_line(
                                    (   tile_x + tile_width  - 2,
                                        tile_y + 2,
                                        tile_x + tile_width  - 2,
                                        tile_y + tile_height - 2),
                                    fill = color,
                                    width = 3)]

######## GUI CLASS ########  
      
""" GUI: The class representation of the GUI
"""
class GUI(Frame):
    """ __call__: The call function for the GUI. Moves the GUI to another mode. 
      * Moves the GUI into the mode with the given name.
    """
    def __call__(self, mode):
        # Switch out the old mode for the new mode
        self.mode(False)
        self.mode = mode
        self.mode(True)

    """ __init__: The initialization function for the GUI
    """
    def __init__(self, host, mode=TileDimension, title=""):
        # Setup Attributes:
        Frame.__init__(self, Tk())
        self.master.title(title)
        self.host = host
        self.mode = mode(self)
        self.mode(True)
        # Bind Keys:
        self.keys = util.config.keys
        self.master.bind('<Key>', lambda event: self.mode.__keypress__(event))
        # Pack and Focus the GUI:
        self.pack(expand=True, fill='both')
        self.focus_force()
        
""" Engine: The class representation of the Tkinter based game Engine
"""
class Engine(object):
    __slots__ = [ 'GUI', 'game' ]
    
    """ __init__:
    """
    def __init__(self, mode, name="IAI"):
        self.game = GameState()
        if mode is not None: 
            self.GUI = GUI(self, mode, name)
        else: self.GameState().run()
       
    """ run:
    """
    def run(self):
        if util.config.mode['invisible']: pass
        else: 
            self.GUI.mainloop()
    
#### FUNCTIONS ####

#### LOCAL TESTING ####

"""
"""
def localTest():
    util.sprint("\n#!# LOCAL TESTS: engineClass.py:")
    # Creating Testing Resources
    up, down, left, right, select=[Event(), Event(), Event(), Event(), Event()]
    test          = util.Tester()
    up.keysym     = 'Up'
    down.keysym   = 'Down'
    left.keysym   = 'Left'
    right.keysym  = 'Right'
    select.keysym = 'Return'
    
    
    # Run a Simulation of the Editor
    try:
        util.sprint("Creating Editor Simulation")
        # Build and Handle Prompt 1
        engine = Engine(ImgFileName, "Testing!")
        key = Event()
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
                    util.type_check(NewFileName, engine.GUI.mode),
                    "Prompt failed to advance " + str(type(engine.GUI.mode)))
    # Handle Prompt 2
    try:
        util.sprint("Simulating new file name prompt")
        for char in "TeMp":
            key.keysym = char
            engine.GUI.mode.__keypress__(key)
        engine.GUI.mode.__keypress__(select)
    except:
        util.sprint("Exception raised during prompt simulation 2")
    test.assertion("NewFileName completion test",
                    util.type_check(TileDimension, engine.GUI.mode),
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
                    util.type_check(Editor, engine.GUI.mode),
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
        test_file = open(util.local_path("source/Maps/TeMp/config"))
    except: util.sprint("Exception raised while reading config file")
    contents = test_file.readlines()
    test.assertion("config contents test",
                    int(contents[10].split(",")[9]) == 4 
                        and int(contents[12].split(",")[9]) == 5,
                    "bad config file contents")
                    
    # Clean-up testing resources
    test_file.close()
    remove(util.local_path('source/Maps/TeMp/config'))
    remove(util.local_path('source/Maps/TeMp/background.gif'))
    rmdir(util.local_path('source/Maps/TeMp'))
    
    # End Message
    util.sprint("Engine testing Complete! Failed: [" + str(test.failed) + "/"
            + str(test.run) + "]\n")
            
    # Return testing object
    return test
    
### SCRIPT ####

if __name__ == '__main__':
    util.test()
    results = localTest()
    
