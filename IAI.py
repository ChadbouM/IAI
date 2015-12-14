import gameClass, wiseClass, mapClass
import shopping, items
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

def IAI(invSize=__DFLTINVSZE__, runs=__DFLTRUNCNT__):
    theWisdom = wiseClass.wisdom(items.mainStore)
    theMap    = mapClass.LargeSwarmMap
    
    while runs:
        theShop   = shopping.shopping(invSize, theWisdom)
        theGame   = gameClass.gameState(theMap, theShop.buy(), theWisdom)
        
        while not theGame.gameOver():
            theGame.advance()
            
        theScore  = theGame.score()
        theWisdom = theGame.hero.wisdom
         
        # TODO: TheSage!? TODO
        #theWisdom = theSage.evaluate(theScore, theWisdom)
        
        if 0 < runs: runs -= 1
    
    
    
