import gameObjects
from items import *
import shopping

''' IAI.py: IAI Project
  * TODO <Project Description>
  * 
  * *
  * Author(s):
  * Michael Chadbourne
  * Mateo Freyre
& * Tim Webber
  * *
  * Last Edited: 12/10/15
'''

class IAI():
	def __init__(self):
		store = {}
		pistol = Pistol()
		shotgun = Shotgun()
		rifle = Rifle()
		store.update({pistol.getName(): pistol})
		store.update({shotgun.getName(): shotgun})
		store.update({rifle.getName(): rifle})
		