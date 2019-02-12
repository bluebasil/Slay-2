import terrains
import random
import const
tid_gen = 0

class tile():
	#based on angle
	#0
	#60
	#120
	#180
	#240
	#300
	adjacent = {}
	terrain = terrains.terrain()
	owner = None
	tid = -1
	tid_gen = [0]
	rendered = None
	x = -1
	y = -1

	def __init__(self,terrain_string = None,tid = None,x=-1,y=-1):
		if terrain_string == None:
			self.terrain = terrains.find_terrain("Water")
			#self.terrain = random.choice(terrains.terrains)
		else:
			self.terrain = terrains.find_terrain(terrain_string)
		if tid == None:
			self.tid = self.tid_gen[0]
			self.tid_gen[0] += 1
		else:
			self.tid = tid
		self.adjacent = {0:None,60:None,120:None,180:None,240:None,300:None}
		self.x = x
		self.y = y


	def set_adj(self,d_0 = None,d_60 = None,d_120 = None,d_180 = None,d_240 = None,d_300 = None):
		if d_0 != None:
			self.adjacent[0] = d_0
			d_0.adjacent[180] = self
		if d_60 != None:
			self.adjacent[60] = d_60
			d_60.adjacent[240] = self
		if d_120 != None:
			self.adjacent[120] = d_120
			d_120.adjacent[300] = self
		if d_180 != None:
			self.adjacent[180] = d_180
			d_180.adjacent[0] = self
		if d_240 != None:
			self.adjacent[240] = d_240
			d_240.adjacent[60] = self
		if d_300 != None:
			self.adjacent[300] = d_300
			d_300.adjacent[120] = self

	def toJson(self):
		adj = {}
		for key,value in self.adjacent.items():
			if value == None:
				adj[key] = None
			else:
				adj[key] = value.tid
		json = {}
		json["adjacent"] = adj
		json["terrain"] = self.terrain.name
		json["tid"] = self.tid
		json["x"] = self.x
		json["y"] = self.y
		return json

	def load_adj(self,adj,tiles):
		for key,value in adj.items():
			if value != None:
				self.adjacent[int(key)] = tiles[value]
		#print(self.terrain,flush = True)

