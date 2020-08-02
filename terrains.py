#for colors
import arcade
import math



class terrain:
	name = "Terrain Name"
	color = arcade.color.BLACK
	owner = None
	movement_cost = 1

class grass(terrain):
	name = "Grass"
	color = (0, 171, 102)

class water(terrain):
	name = "Water"
	color = (59,74,217)
	movement_cost = math.inf

class deep_water(terrain):
	name = "Deep Water"
	color = (34,47,168)
	movement_cost = math.inf

class ice(terrain):
	name = "Ice"
	color = (182,233,250)
	movement_cost = 1.5

class mountain(terrain):
	name = "Mountain"
	color = (150,150,150)
	movement_cost = math.inf

class marsh(terrain):
	name = "Marsh"
	color = (109,138,85)
	movement_cost = 3

class forest(terrain):
	name = "Forest"
	color = (38,89,43)
	movement_cost = 3

def find_terrain(string):
	for t in terrains:
		if t.name == string:
			return t
	return None

terrains = [deep_water(),water(),ice(),grass(),forest(),marsh(),mountain()]