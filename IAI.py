import gameClass, wiseClass, mapClass
import shopping, items
from items import *
import util

''' IAI.py: IAI Project
  * TODO <Project Description>
  * 
  * *
  * Author(s):
  * Michael Chadbourne
  * Mateo Freyre
& * Tim Webber
  * *
  * Last Edited: 12/13/15
'''
__DFLTINVSZE__ = 100
__DFLTRUNCNT__ = 100

theFile = open('Output.txt', 'w')

def IAI(invSize=__DFLTINVSZE__, runs=__DFLTRUNCNT__):
    theWisdom = wiseClass.wisdom(items.mainStore)
    theMap    = mapClass.LargeSwarmMap
    theAverage = 0
    theRuns = 0
    
    theLast = None
    while runs:
        theShop   = shopping.shopping()
        theEquipment = theShop.shopping(invSize, theWisdom)
        theGame   = gameClass.gameState(theMap, theEquipment, theWisdom)
        
        while not theGame.gameOver():
            theGame.advance()
            
        theScore  = theGame.score()
        theWisdom = theGame.hero.wisdom
        theRemains = theGame.hero.invtry # is this the remaining inventory after a game?

        theWisdom = theWisdom.theSage(theScore, theRemains) # instance of wisdom class
        theOutcome, theScore = theScore
        
        theAverage += theScore
        theRuns += 1
        
        if theOutcome: theOutcome = "WIN  Score("
        else:          theOutcome = "LOSS Score("
       
        theFirstLine  = "Run: " + (str(theRuns) + ";").ljust(7) + theOutcome + str(theScore) + ")"
        theSecondLine = "\t\tAverage: " + str(float(theAverage)/theRuns)
        
        theFile.write(theFirstLine + '\n')
        theFile.write(theSecondLine + '\n')
        
        print theFirstLine
        print theSecondLine
        
        theLast = theEquipment
        if 0 < runs: runs -= 1
        
    theFile.write(str(theLast))
    theFile.close()
    print theLast

IAI()
    
    
