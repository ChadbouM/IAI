import sys

'''Weapon:
	* An abstract class for weapons
'''
class Weapon(object):
	def __init__(self):
		self.name = ""
		self.range = 0
		self.weight = 0

	def AOE(self):
		raise NotImplementedError('Subclasses must be overidden, yo')

'''Medkit:
	* An abstract class for medkits
'''
class Medkit(object):
	def __init__(self):
		self.name = ""
		self.healPower = 0
		self.weight = 0


'''Ammo:
	* An abstract class for ammo
'''
class Ammo(object):
	def __init__(self):
		self.name = ""
		self.weight = 0


'''Candy:
	* An abstract class for candy
'''
class Candy(object):
	def __init_(self):
		self.name = ""
		self.weight = ""
		self.points = ""

''' ========================= WEAPONS ========================= '''
class Pistol(Weapon):
	def __init_(self):
		self.name = pistol
		self.range = 3
		self.weight = 10

	def AOE(self):
		raise NotImplementedError('MAKE ME BITCH')

a = Pistol()
print type(a)
