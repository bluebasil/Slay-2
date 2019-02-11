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
	terrain = "Grass"
	x = -1
	y = -1
	tid = -1
	tid_gen = [0]

	def __init__(self):
		self.tid = self.tid_gen[0]
		self.tid_gen[0] += 1
		self.adjacent = {0:None,60:None,120:None,180:None,240:None,300:None}

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
