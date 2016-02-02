#!/usr/bin/end python
""" engineClass.py: the Tkinter based graphical engine used for the Game
  * Part of the IAI project.
  * *
  * Last Edited: 01/31/16
"""
# IMPORTS:
from   os        import path
from   Tkinter   import * 
from   gameClass import GameState
import util, itemClass
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
        
    """ __keypress__:
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
            if x == 0 or y == 0: raise IOError("Zero is an invalid Dimension")
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

""" LoadMapName:
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
   
""" NewFileName: The prompt for the image file while creating a new item
"""
class NewItemFile(Prompt):
    errored = False
    """ __init__: The initialization function for the NewItemFile prompt
    """
    def __init__(self, master, old):
        prompt = "What image shall we use for this item?"
        Prompt.__init__(self, master, prompt)
        self.old = old

    """ __select__: The Selection keypress action for this prompt
    """
    def __select__(self):
        if path.exists(self.text):
            width  = int(self['width']) / self.old.size[0]
            height = int(self['height'])/ self.old.size[1]
            new_image = util.load_image(self.text, (width, height))
            next_mode = NewItemStats(self.master, new_image, self.old)
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

""" NewItemStats: A special prompt-mode for creating new items
"""
class NewItemStats(Mode):
    """ __init__: The initialization function for the NewItemStats prompt
    """
    def __init__(self, master, image, old):
        Mode.__init__(self, master)
        self['bg'] = 'black'
        self.image = image
        self.old   = old
        
        # Create Menu Position:
        self.position = util.LoopPos((1, 7))
        
        # Set Initial Field Values:
        self.locked = False
        self.enemy  = True
        self.fields   = { 
                            'Name'  : "",
                            'Health': "",
                            'Attack': "",
                            'Speed' : "",
                            'Range' : "",
                            'Count' : "" 
                        }
        # Initial Draw:
        self.draw()
    
    """ __keypress__: The callback function for handling keys in this mode
    """
    def __keypress__(self, event):
        # Handling for Enemies:
        if self.enemy:
            # When a field is focused:
            if self.locked:
                # Determine name of focused field:
                if   self.position[1] == 1: lock_name = 'Name'
                elif self.position[1] == 2: lock_name = 'Health'
                elif self.position[1] == 3: lock_name = 'Attack'
                elif self.position[1] == 4: lock_name = 'Speed'
                elif self.position[1] == 5: lock_name = 'Range'
                # Assign Events to Field: TODO: REFACTOR OUT
                if   event.keysym == 'Return':
                    self.locked = False
                    self.position[1] += 1
                elif event.keysym == 'BackSpace':     
                    self.fields[lock_name] = self.fields[lock_name][:-1]
                elif event.keysym in util.alphabet():
                    self.fields[lock_name] += util.translate(event.keysym)
                else: return
            else: # When NOTHING is focused:
                if   event.keysym in util.config.keys['Menu_Up']:
                    self.position[1] -= 1
                elif event.keysym in util.config.keys['Menu_Down']:
                    self.position[1] += 1
                elif event.keysym in util.config.keys['Menu_Right']:
                    if self.position[1] == 0:
                        self.enemy = False
                        self.position.max = (1, 4)
                elif event.keysym in util.config.keys['Menu_Select']:
                    if self.position[1] in  range(1, 6): self.locked = True
                    elif self.position[1] == 6: 
                        self.advance()
                        return
                    else: pass
                elif event.keysym in util.config.keys['Menu_Back']:
                    self.master(self.old)
        else: # Handling for Pick-Up Items:
            # When a field is focused:
            if self.locked:
                # Determine name of focused field:
                if   self.position[1] == 1: lock_name = 'Name'
                elif self.position[1] == 2: lock_name = 'Count'
                # Assign Events to Field: TODO: DOUBLE
                if   event.keysym == 'Return': 
                    self.locked = False
                    self.position[1] += 1
                elif event.keysym == 'BackSpace':     
                    self.fields[lock_name] = self.fields[lock_name][:-1]
                elif event.keysym in util.alphabet():
                    self.fields[lock_name] += util.translate(event.keysym)
                else: return
            else: # When NOTHING is focused:
                if   event.keysym in util.config.keys['Menu_Up']:
                    self.position[1] -= 1
                elif event.keysym in util.config.keys['Menu_Down']:
                    self.position[1] += 1
                elif event.keysym in util.config.keys['Menu_Left']:
                    if self.position[1] == 0:
                        self.enemy = True
                        self.position.max = (1, 7)
                elif event.keysym in util.config.keys['Menu_Select']:
                    if self.position[1] in  range(1, 3): self.locked = True
                    elif self.position[1] == 3: 
                        self.advance()
                        return
                    else: pass
                elif event.keysym in util.config.keys['Menu_Back']:
                    self.master(self.old)
        self.draw()
        
    """ advance: Moves the prompt forward, returning to the Editor.
    """
    def advance(self):
        map_name  = self.old.map.name
        item_name = self.fields.pop('Name') ######################## NAME POPPED
        # Popping Off Empty, Converting Rest to Int ############################
        [self.fields.pop(key) for key, val in self.fields.items() if val == ""]
        [self.fields.__setitem__(key, int(val)) for key, val in self.fields.items()]
        # Save Image to Image Folder
        new_path  = util.local_path('source/Maps/%s/items/%s.gif' %
                                    (map_name, item_name))
        self.image.save( util.local_path(new_path), 'GIF', transparency=1 )
        self.image.close()
        # Create Image Item
        if self.enemy: type = 'enemy'
        else:          type = 'pickup' 
        new_item = itemClass.MapItem(map_name, item_name, type, self.fields)
        # Place Image Item
        cur_x = self.old.posit[0]
        cur_y = self.old.posit[1]
        # Check If Item with this name Exisits
        for i, item in enumerate(self.old.map.items):
            if item.name == item_name:
                self.old.map.items[i] = new_item
                self.old.draw()
                self.master(self.old)
                return
        
        self.old.map.items += [new_item]
        self.old.map.spawn[cur_x][cur_y] = len(self.old.map.items)
        self.old.item_pos.max = (1, self.old.item_pos.max[1] + 1)
        # Change Mode
        self.old.draw()
        self.master(self.old)
        
    """ draw: Draws the visual associated with this mode onto the Canvas
    """
    def draw(self):
        # Remove any moveable items on the Canvas:
        [ self.delete(id) for id in self.mvis ]
        # Readability Constants:
        width  = int(self['width'])
        height = int(self['height'])
        # Draw Line 1:
        self.mvis += [ self.create_text(
                       ( width/2, height/7 ),
                       text = "Enemy\t\tPickUp",
                       font = (util.config.settings['Font'][0], 22),
                       fill = 'white') ]
        ## Determine Bounds:
        if self.enemy:
            bounds = (width/2-170, height/7-25, width/2-60, height/7+25)
        else: 
            bounds = (width/2+50, height/7-25, width/2+170, height/7+25)
        ## Determine Color:
        if self.position[1] == 0:
            if self.locked: color = 'red'
            else:           color = 'yellow'
        else:               color = 'white'
        ## Draw Selection Box
        self.mvis += [ self.create_rectangle(
                       bounds,
                       width   = 3,
                       outline = color) ]
        # Draw Line 2:
        self.draw_line('Name', 2)
        
        if self.enemy:
            # Draw Line 3:
            self.draw_line('Health', 3)
            # Draw Line 4:
            self.draw_line('Attack', 4)
            # Draw Line 5:
            self.draw_line('Speed', 5)
            # Draw Line 6:
            self.draw_line('Range', 6)
        else:
            # Draw Line 3:
            self.draw_line('Count', 3)
            
        # Draw Line 7:
        if self.enemy:
            if self.position[1] == 6: color = 'yellow'
            else:                     color = 'white'
        else:
            if self.position[1] == 3: color = 'yellow'
            else:                     color = 'white'
        # Draw Title Text:
        self.mvis += [ self.create_text(
                       ( width/2, height - 50),
                       text   = "Done",
                       font   = (util.config.settings['Font'][0], 22),
                       fill   = color) ]
        # Draw Outline:
        bounds = (width/2-55, height-75, width/2+55, height-25)
        self.mvis += [ self.create_rectangle(
                       bounds,
                       width   = 5,
                       outline = color) ]
           
    """ draw_line: A Helper for the draw function, draws a prompt-line
    """
    def draw_line(self, name, num):
        width  = int(self['width'])
        height = int(self['height'])
        # Set Outline Color:
        if self.position[1] == num - 1:
            if self.locked: color = 'red'
            else:           color = 'yellow'
        else:               color = 'white'
        # Draw Title Text:
        self.mvis += [ self.create_text(
                       ( width/2 - 250, num*height/7),
                       text   = name + ':',
                       anchor = 'w',
                       font   = (util.config.settings['Font'][0], 20),
                       fill   = color) ]
        # Draw Input Box:
        bounds = (width/2-150, num*height/7-20, width/2+150, num*height/7+20)
        self.mvis += [ self.create_rectangle(
                       bounds,
                       width   = 3,
                       outline = color) ]
        # Draw Internal Text:
        self.mvis += [ self.create_text(
                       ( width/2 - 140, num*height/7),
                       text   = self.fields[name],
                       anchor = 'w',
                       font   = (util.config.settings['Font'][0], 18),
                       fill   = 'white') ]
                       
        
        
    ##############################
############ EDITOR CLASS ############
    ##############################
   
""" Editor:
"""
class Editor(Mode):
    lock_level = 0
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
        self.size     = self.map.size
        self.posit    = util.LoopPos(self.size)
        self.item_pos = util.LoopPos((1, len(self.map.items) + 1))
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
    
    """ close: Shuts the Editor down.
    """
    def close(self):
        self.master.quit()
        self.master.master.destroy()
        if not util.config.mode['testing']: quit()

    """ __keypress__: The keypress handler of the Editor mode
      * Handles switching between sub modes, wall-assignment, tile-selection,
      * and Menu.
    """
    def __keypress__(self, event):
        # Up Key pressed: ######################################################
        if   event.keysym in util.config.keys['Menu_Up']:  
            if   self.lock_level  == -1:############ MENU
                           self.menu_pos[1] -=  1
            elif self.lock_level  ==  0:############ GRID
                           self.posit[1]    -=  1
            elif self.lock_level  ==  1:############ TILE
                           self.map.walls[self.posit[0]][self.posit[1]] =   'Up'
            elif self.lock_level  ==  2:############ ITEM
                           self.item_pos[1] -=  1
            else:################################### ERROR
                           raise AttributeError('lock_level out of range')

        # Down Key Pressed: ####################################################       
        elif event.keysym in util.config.keys['Menu_Down']:
            if   self.lock_level  == -1:           # MENU
                           self.menu_pos[1] +=  1
            elif self.lock_level  ==  0:           # GRID
                           self.posit[1]    +=  1
            elif self.lock_level  ==  1:           # TILE
                           self.map.walls[self.posit[0]][self.posit[1]] = 'Down'
            elif self.lock_level  ==  2:           # ITEM
                           self.item_pos[1] +=  1
            else:                                  # ERROR
                           raise AttributeError('lock_level out of range')

        # Left Key Pressed: ####################################################
        elif event.keysym in util.config.keys['Menu_Left']:
            if   self.lock_level  == -1:############ MENU
                           pass
            elif self.lock_level  ==  0:############ GRID
                           self.posit[0]    -=  1
            elif self.lock_level  ==  1:############ TILE
                           self.map.walls[self.posit[0]][self.posit[1]] = 'Left'
            elif self.lock_level  ==  2:############ ITEM
                           pass
            else:################################### ERROR
                           raise AttributeError('lock_level out of range') 
                           
        # Right Key Pressed: ###################################################        
        elif event.keysym in util.config.keys['Menu_Right']:
            if   self.lock_level  == -1:############ MENU
                           pass
            elif self.lock_level  ==  0:############ GRID
                           self.posit[0]    +=  1
            elif self.lock_level  ==  1:############ TILE
                           self.map.walls[self.posit[0]][self.posit[1]] ='Right'
            elif self.lock_level  ==  2:############ ITEM
                           pass
            else:################################### ERROR
                           raise AttributeError('lock_level out of range')

        # Select Key Pressed: ##################################################        
        elif event.keysym in util.config.keys['Menu_Select']: 
            if   self.lock_level  == -1:############ MENU
                if   self.menu_items[self.menu_pos[1]] == 'Save':
                    self.map.__save__()
                elif self.menu_items[self.menu_pos[1]] == 'Save As': 
                    self.master(SaveAs(self))
                elif self.menu_items[self.menu_pos[1]] == 'Save and Exit':
                    self.map.__save__()
                    self.close()
                    return
                elif self.menu_items[self.menu_pos[1]] == 'Exit':
                    self.close()
                    return
            elif self.lock_level  ==  0:############ GRID
                self.lock_level += 1
            elif self.lock_level  ==  1:############ TILE
                self.lock_level += 1
            elif self.lock_level  ==  2:############ ITEM
                self.lock_level -= 2
                if self.item_pos[1] == self.item_pos.max[1] - 1:
                    self.master(NewItemFile(self.master, self))
                else: 
                    self.map.spawn[self.posit[0]][self.posit[1]] = \
                    self.item_pos[1] + 1
            else:################################### ERROR
                raise AttributeError('lock_level out of range')

        # Back Key Pressed: ####################################################
        elif event.keysym in util.config.keys['Menu_Back']:
            if   self.lock_level  == -1:############ MENU
                           self.lock_level += 1
            elif self.lock_level  ==  0:############ GRID
                           self.lock_level -= 1
            elif self.lock_level  ==  1:############ TILE
                           self.lock_level -= 1
            elif self.lock_level  ==  2:############ ITEM
                           self.lock_level -= 2
            else:################################### ERROR
                           raise AttributeError('lock_level out of range')
                           
        # Alternate Key Pressed: ###############################################
        elif event.keysym in util.config.keys['Menu_Alt']:
            if   self.lock_level  == -1:############ MENU
                    pass
            elif self.lock_level  ==  0:############ GRID
                    pass
            elif self.lock_level  ==  1:############ TILE
                    self.map.spawn[self.posit[0]][self.posit[1]] = 0
            elif self.lock_level  ==  2:############ ITEM
                    item    = self.map.items[self.item_pos[1]]
                    image   = util.load_image(
                        util.local_path('source/Maps/%s/items/%s.gif' %
                            (self.map.name, item.name)))
                    edit_prompt = NewItemStats(self.master, image, self)
                    edit_prompt.fields['Name'] = item.name
                    if item.type == 'enemy':
                        edit_prompt.enemy = True
                        edit_prompt.fields['Health'] = item.health
                        edit_prompt.fields['Attack'] = item.attack
                        edit_prompt.fields['Speed']  = item.speed
                        edit_prompt.fields['Range']  = item.range
                    else:
                        print edit_prompt.enemy
                        edit_prompt.enemy = False
                        print edit_prompt.enemy
                        edit_prompt.fields['Count'] = item.count
                    edit_prompt.draw()
                    self.master(edit_prompt)
                           
            else:################################### ERROR
                           raise AttributeError('lock_level out of range')
        
        self.draw()
      
    """ draw: Draws the Map and GUI on to the Canvas. Updating the Image.
    """
    def draw(self):
        # Remove any moveable items on the Canvas:
        [ self.delete(id) for id in self.mvis ]
        # Readability Variables:
        width       = int(self['width'])
        height      = int(self['height'])
        tile_width  = width/self.size[0]
        tile_height = height/self.size[1]
        tile_x      = self.posit[0] * tile_width
        tile_y      = self.posit[1] * tile_height
        # Determine Border Color
        if   self.lock_level == 1: color = 'blue'
        elif self.lock_level == 2: color = 'green'
        else:                      color = 'black'
        # Draw Selection Reticle:
        self.mvis += [self.create_rectangle(
                                (   tile_x,
                                    tile_y,
                                    tile_x + tile_width,
                                    tile_y + tile_height),
                                outline = color,
                                width = 3)]
        # Draw The Items:
        for x in range(self.size[0]):
            for y in range(self.size[1]):
                value = self.map.spawn[x][y]
                if 0 < value:
                    self.mvis += [ self.create_image(
                        (x*tile_width, y*tile_height),
                        image = self.map.items[value - 1].image,
                        anchor = 'nw' ) ]
        # Draw The Walls:
        for x in range(self.size[0]):
            for y in range(self.size[1]):
                self.draw_bounds(x, y, self.map.walls[x][y])                
        # Draw Lock-Level specific Artifacts.
        if self.lock_level == -1: ######################################### MENU
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
        elif self.lock_level == 0: ######################################## GRID
            pass
        elif self.lock_level == 1: ######################################## TILE
            pass
        elif self.lock_level == 2: ######################################## ITEM
            # Draw Menu-Box on right:
            self.mvis += [self.create_rectangle(
                                    (width - 250, 0, width, height),
                                    fill    = 'black',
                                    outline = 'white',
                                    width   = 5.0 )]
            # Draw Menu-Items:
            for i in range(-2, 3):
                item = self.item_pos[1] + i
                item_count = len(self.map.items)
                if item in range(item_count):    # Draw Exisiting Item Images
                    self.mvis += [  self.create_image(
                                    (width - 125, height/2 + 100*i),
                                    image = self.map.items[item].image) ]
                                    
                elif item == item_count:         # Draw 'Add' Item
                    self.mvis += [  self.create_line(
                                    (   width - 100, height/2 + 100*i,
                                        width - 150, height/2 + 100*i),
                                    fill  = 'yellow',
                                    width = 5) ]
                    self.mvis += [  self.create_line(
                                    (   width - 125, height/2 + 100*i - 25,
                                        width - 125, height/2 + 100*i + 25),
                                    fill  = 'yellow',
                                    width = 5) ]

            # Draw Selection Box:
            self.mvis += [  self.create_rectangle(
                                    (   width - 75, height/2 - 50,
                                        width - 175, height/2 + 50),
                                    outline  = 'white',
                                    width = 3) ]


    """ draw_bounds: Helper for draw which draws the walls   
    """
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

######## END: GUI MODES ########                                      
                                    
    ###########################
############ GUI CLASS ############
    ###########################  
      
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
        
    ##############################
############ ENGINE CLASS ############
    ##############################
        
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
    
