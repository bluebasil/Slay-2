import tile

class model:
	width = 1
	height = 1

	tiles = set()
	base_tile = None

	def __init__(self,width,height,wrap = True):
		self.width = width
		self.height = height
		tiles = []

		last_col = [None]*height
		first_col = []
		for w in range(width):
			for h in range(height):
				new_tile = tile.tile()
				if h == 0 and w == 0:
					self.base_tile = new_tile
				if h != 0:
					new_tile.set_adj(d_0 = tiles[-1])
				if h == height - 1:
					new_tile.set_adj(d_180 = last_col[0])
				if w != 0:
					#print(w,h,last_col)
					if w%2 == 0:
						new_tile.set_adj(d_240 = last_col[h])
					else:
						new_tile.set_adj(d_300 = last_col[h])
					if w == width-1:
						if w%2 == 0:
							first_col[h].set_adj(d_300 = new_tile)
						else:
							first_col[h].set_adj(d_240 = new_tile)
				else:
					first_col.append(new_tile)
				last_col[h] = new_tile
				tiles.append(new_tile)

		self.tiles = set(tiles)
