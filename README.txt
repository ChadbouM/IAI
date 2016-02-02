IAI 2.0.0*

A project in AI. Help an agent learn the best strategies as they face an
endless gauntlet of foes! The IAI agent moves through a world, learning and 
shopping on their own, while allowing the player to nudge them toward certain
behaviors.

 * To see the Original version of this project view the "Legacy" branch of the 
repo found at: http://www.github.com/chadbouM/IAI/tree/legacy

# DEPENDENCIES:
python 2.7
PIL
Tkinter

# DEVELOPMENT NOTES #

Currently building a framework for the 2.0 system. Have created a functional
Map Editor, which uses a background image and time dimensions to create a file
for the game and allows the addition of Enemies and Pick-Up Items(In Progress)


The game itself will involve importing elements from the original IAI, as well
as redesigning other components. Which will be added as the rest of the project
takes shape.

# USEAGE #

--Game--
(Not Implemented)

--Map-Creation-- [Creates a new Map File and opens the editor]
> CreateMap.bat
or
> python .\source\IAI.py --as create

---Map-Editor--- [Loads a Map file from the source/Maps/ directory]
> EditMap.bat
or 
> python .\source\IAI.py --as edit

Currently the Map Editor allows the placement of walls and enemies onto a 
background generated from an image.

# CONTROLS:

WASD  -> Move Selection (When selecting a Tile -> Places Walls on Tile)
Space -> Select
E     -> Back
Q     -> Alt
(Can be Changed in the config file [Open in Text Editor])


*  Use Return(Enter) to finish typing in a prompt
** Alt: When Selecting a Tile            -> Removes Enemy from Tile
		When Selecting an Item from Menu -> Edit selected Item


# TODO/UPCOMING #

> PickUp -> Item link
> The IAI Game
-- Will use the Maps made with the editor
-- Built from principles and code found in the 'Legacy' project
> Linux (Ubuntu) Testing/Launcher

# CREDITS: #

Michael Chadbourne
& Tim Webber
& Matt Freyre