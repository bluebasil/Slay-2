import tile
import json
from json import JSONEncoder
import path
import const

class MyEncoder(JSONEncoder):
	def default(self, o):
		return o.toJson()

class model:
	width = 1
	height = 1

	tiles = []
	base_tile = None

	def __init__(self,width,height,wrap = True):
		self.width = width
		self.height = height
		tiles = []

		this_col = [None]*height
		first_col = []
		prev_col = this_col.copy()
		for w in range(width):
			for h in range(height):
				if const.GLOBE_MODE and h == height - 1 and  w%2 != 0:
					pass
				else:
					new_tile = tile.tile(x=w,y=h)
					if h == 0 and w == 0:
						self.base_tile = new_tile
					if const.GLOBE_MODE:
						
						if h != 0:
							new_tile.set_adj(d_0 = tiles[-1])
						elif w%2 == 0:
							new_tile.adjacent[0]=new_tile
						if h == height - 1 and  w%2 == 0:
							new_tile.adjacent[180]=new_tile
						
					else:
						if h != 0:
							new_tile.set_adj(d_0 = tiles[-1])
						if h == height - 1:
							new_tile.set_adj(d_180 = this_col[0])
					"""elif const.GLOBE_MODE and w%2==0:
						new_tile.adjacent[0]=new_tile"""
					"""
						if const.GLOBE_MODE:
							if w%2 == 0:
								new_tile.adjacent[180]=new_tile
						else:
							"""
					if w != 0:
						if const.GLOBE_MODE:
							if w%2 == 0:
								if h != height - 1:
									new_tile.set_adj(d_240 = prev_col[h])
									#filler_tile = tile.tile(x=w-1,y=h+1)
									#tiles.append(filler_tile)
									#filler_tile.set_adj(d_120 = new_tile)
									#filler_tile.adjacent[60] = new_tile
									#filler_tile.set_adj(d_180 = new_tile)
								if h != 0:
									new_tile.set_adj(d_300 = prev_col[h-1])
									#filler_tile = tile.tile(x=w-1,y=h-1)
									#tiles.append(filler_tile)

							else:
								new_tile.set_adj(d_300 = prev_col[h])
								new_tile.set_adj(d_240 = prev_col[h+1])
						else:
							#print(w,h,this_col)
							if w%2 == 0:
								new_tile.set_adj(d_300 = prev_col[h-1])
								new_tile.set_adj(d_240 = prev_col[h])
								pass
							else:
								wrap_h = h+1
								if wrap_h == len(this_col):
									wrap_h = 0
								#print(new_tile.tid,this_col[wrap_h].tid,this_col[h-1].tid,flush = True)
								
								new_tile.set_adj(d_300 = prev_col[h])
								new_tile.set_adj(d_240 = prev_col[wrap_h])
						if w == width-1:
							#since w should be even?
							if w%2 == 0:
								#wrap_h = h+1
								#if wrap_h == len(this_col):
								#	wrap_h = 0
								first_col[h-1].set_adj(d_240 = new_tile)
								first_col[h].set_adj(d_300 = new_tile)
							else:
								wrap_h = h+1
								if wrap_h == len(first_col):
									wrap_h = 0
								#first_col[wrap_h].set_adj(d_240 = new_tile)
								first_col[wrap_h].set_adj(d_300 = new_tile)
								first_col[h].set_adj(d_240 = new_tile)
					else:
						first_col.append(new_tile)
					this_col[h] = new_tile
					tiles.append(new_tile)
			prev_col = this_col.copy()
		self.tiles = tiles

	def toJson(self):
		json = {}
		json["base_tile"] = self.base_tile.tid
		json["width"] = self.width
		json["height"] = self.height
		tiles = {}
		for t in self.tiles:
			tiles[t.tid] = t.toJson()
		json["tiles"] = tiles
		return json

	def fromJson(self,json):
		self.width = json["width"]
		self.height = json["height"]
		self.tiles = []
		for key,value in json["tiles"].items():
			#print(value["terrain"],flush = True)
			new_tile = tile.tile(value["terrain"],int(key),value["x"],value["y"])
			self.tiles.append(new_tile)
		for t in self.tiles:
			#print(json["tiles"],flush = True)
			#print(json["tiles"][str(t.tid)],flush = True)
			#print(json["tiles"][str(t.tid)]["adjacent"],flush = True)
			t.load_adj(json["tiles"][str(t.tid)]["adjacent"],self.tiles)
		self.base_tile = self.tiles[0]



	def save(self,filename = "map.json"):
		with open(filename, 'w') as outfile:
			json.dump(self, outfile, default=lambda o: o.toJson(), 
			sort_keys=False, indent=4)


	def load(self,filename = "map.json"):
		with open(filename) as f:
			data = json.load(f)

		self.fromJson(data)

