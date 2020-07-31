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
	color = (102, 153, 204)
	movement_cost = math.inf

class ice(terrain):
	name = "Ice"
	color = (200,200,200)
	movement_cost = 1.5

class mountain(terrain):
	name = "Mountain"
	color = (110,110,110)
	movement_cost = math.inf

def find_terrain(string):
	for t in terrains:
		if t.name == string:
			return t
	return None

terrains = [grass(),water(),ice()]