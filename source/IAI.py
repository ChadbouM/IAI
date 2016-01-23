#!/usr/bin/end python
""" IAI itemizing itelligence project:
  * *
  * Last Edited: 1/16/16
"""
# IMPORTS:
import sys
from   argparse    import ArgumentParser
import util
from   engineClass import *
from   gameClass   import Level

# HEADER INFO:
__author__     = "Michael Chadbourne, Tim Webber, Matt Freyre"
__version__    = "2.0.0"
__maintainer__ = "Michael Chadbourne"
__status__     = "Prototype"

# Setup and run Argument Parser:
parser = ArgumentParser(description="The IAI Project/Game")
parser.add_argument("--as", dest='start', nargs='?', default="run")
parser.add_argument("Mode")
args = parser.parse_args(sys.argv)
# Build Engine with Arguments
if   args.start in ['run', 'game']: pass
elif args.start in ['create', 'creator']: 
    startMode = ImgFileName
    modeName  = "IAI: Map Editor"
elif args.start in ['edit', 'editor']: 
    startMode = LoadMapName
    modeName  = "IAI: Map Editor"
else: pass

if util.config.mode['invisible']:
    startMode = None

game = Engine(startMode, modeName)

# Run Game
game.run()

# Clean Up