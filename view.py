import arcade
import model
import math
import time
from shapely.geometry import Point, Polygon
import terrains
import paths
import const

#height of 1 tile
SCALE = 150

GLOBE_RAD = 500
GLOBAFY = False
EDIT_MODE = True
#PI = 3.141592653

cur_path = None

sprites = []

def dist(x1,y1,x2,y2):
	return math.sqrt((x1-x2)**2+(y1-y2)**2)

def change_rad(dif):
	global GLOBE_RAD
	if dif > 0 or GLOBE_RAD > SCALE/3:
		GLOBE_RAD += dif

def change_scale(dif):
	global SCALE
	SCALE = max(50,min(300,SCALE + dif))

def toggle_edit_mode():
	global EDIT_MODE
	EDIT_MODE = not EDIT_MODE

def toggle_globe():
	global GLOBAFY
	GLOBAFY = not GLOBAFY

def add_sprite(sprite_tuple):
	global sprites
	sprites.append(sprite_tuple)

def reset_sprites():
	global sprites
	sprites = []

def sortSprites(val): 
    return val[0]  

def get_sprites():
	global sprites
	sprites.sort(key = sortSprites,reverse = True)
	return sprites

class MyGame(arcade.Window):
	""" Our custom Window Class"""
	model = None
	tiles = {}
	render_track = False
	center_tile = None
	zero_is_up = True
	cen_x = const.SCREEN_WIDTH/2
	cen_y = const.SCREEN_HEIGHT/2
	mouse_down = False
	right_down = False
	inertia = [0,0]
	#records mouse down position
	down_pos = [0,0]
	mouse_delta_time = 0
	#for detecting an error
	least_one_rendered = False

	selected = None

	render_count = 0

	def __init__(self,model):
		""" Initializer """
		# Call the parent class initializer
		super().__init__(const.SCREEN_WIDTH, const.SCREEN_HEIGHT, "Sprite Example")

		# Set the working directory (where we expect to find files) to the same
		# directory this .py file is in. You can leave this out of your own
		# code, but it is needed to easily run the examples using "python -m"
		# as mentioned at the top of this program.
		#file_path = os.path.dirname(os.path.abspath(__file__))
		#os.chdir(file_path)
		self.model = model
		global cur_path
		cur_path = path([0,1,2,3,4,5])

		# Don't show the mouse cursor
		self.set_mouse_visible(True)

		arcade.set_background_color(arcade.color.BLACK)

	def setup(self):
		#self.game_board = boss("boss")
		self.center_tile = self.model.base_tile
		
		
	def recursive_render(self,start,x,y,zero_is_up = True):
		self.render_count += 1
		#if self.render_count > 1000:
		#	return

		global cur_path
		if start == None:
			return
		
		#find or initalize
		this = None
		if start.tid in self.tiles:
			this = self.tiles[start.tid]
		else:
			this = tile(start)
			self.tiles[start.tid] = this

		#Off of screen
		#if x>const.SCREEN_WIDTH+SCALE or x<-SCALE or y>const.SCREEN_HEIGHT+SCALE or y<-SCALE:
		#	return
		
		if dist(x,y,const.SCREEN_WIDTH/2,const.SCREEN_HEIGHT/2) < dist(self.cen_x,self.cen_y,const.SCREEN_WIDTH/2,const.SCREEN_HEIGHT/2):
			self.cen_x = x
			self.cen_y = y
			self.center_tile = start
			self.zero_is_up = zero_is_up

		#render, if it's already been renderted, closes
		if not this.render(x,y):
			if not self.least_one_rendered:
				print("EERRROOR",flush = True)
				self.inertia[0] = self.inertia[0]/2
				self.inertia[1] = self.inertia[1]/2
			return
		else:
			self.least_one_rendered = True
			#print(this.last_point,flush = True)


		for key, value in start.adjacent.items():
			if value != None:
				if zero_is_up:
					key = 90-key
				else:
					key = key - 90
				new_x = x+math.cos(key/180*math.pi)*SCALE
				new_y = y+math.sin(key/180*math.pi)*SCALE
				#there is a mirror
				if value == start:
					self.recursive_render(value,new_x,new_y,not zero_is_up)
				else:
					self.recursive_render(value,new_x,new_y,zero_is_up)


		


		
			#self.inertia[0] = self.inertia[0]*0.99
			#self.inertia[1] = self.inertia[1]*0.99
			#if inertia < 0.01


	def on_draw(self):

		global cur_path
		""" Draw everything """
		arcade.start_render()

		reset_sprites()
		self.render_count = 0

		#self.coin_list.draw()
		#self.player_list.draw()
		self.render_track = not self.render_track
		self.least_one_rendered = False

		for t in self.tiles.values():
			t.reset_render()
		self.recursive_render(self.center_tile,self.cen_x,self.cen_y,self.zero_is_up)
		#arcade.draw_circle_outline(const.SCREEN_WIDTH/2, const.SCREEN_HEIGHT/2, GLOBE_RAD, arcade.color.WOOD_BROWN, 3)
		#arcade.finish_render()

		#if cur_path != None and cur_path.tids != None:
			#print("HELP",flush = True)
			#print(self.tiles[0].last_point,flush = True)
			#cur_path.render(self.tiles[cur_path.tids[0]])



		sprite_list = get_sprites()
		for s in sprite_list:
			s[1]()




	def on_mouse_motion(self, x, y, dx, dy):
		if self.mouse_down:
			#print(dx,dy,flush = True)
			self.cen_x += dx
			self.cen_y += dy
			self.inertia = [max(min(dx,GLOBE_RAD),-GLOBE_RAD),max(min(dy,GLOBE_RAD),-GLOBE_RAD)]
			self.inertia = [dx,dy]
		#if self.right_down:
		#	change_rad(dx)
		#	change_scale(dy)
		pass

	def on_mouse_release(self,x, y, button, modifiers):
		global cur_path
		if button == 1:
			self.mouse_down = False
			if x == self.down_pos[0] and y == self.down_pos[1]:
				#unselect all other tiles
				for t in self.tiles.values():
					t.selected = False
				self.selected = None
				cur_path = path([])

				click_point = Point(x,y)
				for t in self.tiles.values():
					if t.click(click_point):
						t.selected = True
						self.selected = t
						if EDIT_MODE:
							t.obj.terrain = terrains.terrains[terrains.terrains.index(t.obj.terrain)-1]
						return
		elif button == 4:
			self.right_down = False
			cur_path = path([])
			if self.selected != None:
				click_point = Point(x,y)
				for t in self.tiles.values():
					if t.click(click_point):
						cur_path = path(paths.find(self.selected.obj,t.obj))
						return
		return

	def on_mouse_press(self,x,y,button,modifiers):
		#print(button,modifiers,flush = True)
		if button == 1:
			self.down_pos = [x,y]
			self.mouse_down = True
		elif button == 4:
			self.right_down = True
		pass


	def on_key_press(self, key, modifiers):
		pass

	def on_key_release(self, key, modifiers):
		print(key,modifiers,flush = True)
		if key == arcade.key.EQUAL and modifiers == arcade.key.MOD_SHIFT:
			print("1",flush = True)
			change_rad(10)
		elif key == arcade.key.MINUS and modifiers == arcade.key.MOD_SHIFT:	
			print("2",flush = True)
			change_rad(-10)
		elif key == arcade.key.EQUAL:
			print("3",flush = True)
			change_scale(10)
		elif key == arcade.key.MINUS:
			print("4",flush = True)
			change_scale(-10)
		elif key == arcade.key.BACKSPACE:
			self.model.save()
		elif key == arcade.key.ENTER:
			self.model.load()
			self.reload()
		elif key == arcade.key.G:
			toggle_globe()
		elif key == arcade.key.E:
			toggle_edit_mode()
		pass

	def reload(self):
		self.center_tile = self.model.base_tile
		self.tiles = {}

	def update(self, delta_time):
		#print(delta_time,flush = True)
		if not self.mouse_down and (self.inertia[0] > 0 or self.inertia[1] > 0):
			self.cen_x += self.inertia[0]#*delta_time
			self.cen_y += self.inertia[1]#*delta_time
		""" Movement and game logic """
	   #print(f"updating {delta_time}",flush=True)

		# Call update on all sprites (The sprites don't do much in this
		# example though.)
		pass

#reterns false if point is not rendered
#returns (x,y) of new point, if rendered
def warp(point):
	radians = dist(point[0],point[1],const.SCREEN_WIDTH/2,const.SCREEN_HEIGHT/2)
	#point is off globe
	if radians > math.pi*GLOBE_RAD/2:
		return False
	#determine rads 
	#d = radians
	radians = radians/GLOBE_RAD
	base_angle = (math.pi-radians)/2
	fin_angle = math.pi/2 - base_angle
	base = 2*GLOBE_RAD*math.cos(base_angle)
	true_d = math.cos(fin_angle)*base

	#atan2 is suposed to comput angle with the quadrant known
	point_angle = math.atan2(point[1]-const.SCREEN_HEIGHT/2,point[0]-const.SCREEN_WIDTH/2)
	new_point = [-1,-1]
	new_point[0] = math.cos(point_angle)*true_d + const.SCREEN_WIDTH/2
	new_point[1] = math.sin(point_angle)*true_d + const.SCREEN_HEIGHT/2

	return new_point


class path:
	tids = []
	#points = []
	def __init__(self,tid_path):
		self.tids = tid_path

	def in_path(self,tile):
		if tile.tid in self.tids:
			inx = self.tids.index(tile.tid)
			if inx != len(self.tids) - 1:
				for key,t in tile.adjacent.items():
					if t != None and t.tid == self.tids[inx+1]:
						return key
				print("PATH ERROR",flush=True)
		return None
	#		points.append()


	def render(self,start_tile):
		self.render_step(start_tile,1)

	def find_adj(self,tile,idx):
		#print(tile.last_point,flush = True)
		for t in tile.obj.adjacent.values():
			if t != None and t.tid == self.tids[idx]:
				return t.rendered
		return None

	def render_step(self,tile,idx):
		if idx == len(self.tids):
			#print(f"Done {idx}",flush = True)
			return
		next_tile = self.find_adj(tile,idx)
		#print(next_tile.last_point,next_tile.last_point,flush = True)
		if next_tile.last_point != None and tile.last_point != None:
			#print(tile.last_point[0], tile.last_point[1], next_tile.last_point[0], next_tile.last_point[1],flush = True)
			def draw():
				arcade.draw_line(tile.last_point[0], tile.last_point[1], next_tile.last_point[0], next_tile.last_point[1], arcade.color.RED, 10)
			add_sprite((-10000,draw))

		self.render_step(next_tile,idx+1)

class tile:
	obj = None
	render_track = False
	rendered_pos = {}
	polys = []
	tid = -1
	selected = False
	last_point = None

	def __init__(self,coresponding_object):
		
		#print(f"Recreated {coresponding_object.terrain.name}",flush = True)
		self.obj = coresponding_object
		coresponding_object.rendered = self
		self.tid = coresponding_object.tid
		self.rendered_pos = {}
		self.polys = []
		self.reset_render()
		return

	def render(self,x,y):
		global cur_path
		#self.rendered_points = []
		x = int(x)
		y = int(y)
		self.last_point = None
		if x in self.rendered_pos:
			if y in self.rendered_pos[x]:
				#print(f"already rendered",flush = True)
				return False
			else:
				self.rendered_pos[x].add(y)
		else:
			self.rendered_pos[x] = set([y])
		"""input_LINES = [((x-(SCALE/2)/math.sqrt(3),y+SCALE/2),
				(x+(SCALE/2)/math.sqrt(3),y+SCALE/2)),
				((x+(SCALE/2)/math.sqrt(3),y+SCALE/2),
				(x+SCALE/math.sqrt(3),y)),
				((x+SCALE/math.sqrt(3),y),
				(x+(SCALE/2)/math.sqrt(3),y-SCALE/2)),
				((x+(SCALE/2)/math.sqrt(3),y-SCALE/2),
				(x-(SCALE/2)/math.sqrt(3),y-SCALE/2)),
				((x-(SCALE/2)/math.sqrt(3),y-SCALE/2),
				(x-SCALE/math.sqrt(3), y)),
				((x-SCALE/math.sqrt(3), y),
				(x-(SCALE/2)/math.sqrt(3),y+SCALE/2))]"""
		scale = SCALE - 2
		input_points = [(x-(scale/2)/math.sqrt(3),y+scale/2),
			  (x+(scale/2)/math.sqrt(3),y+scale/2),
			  (x+scale/math.sqrt(3),y),
			  (x+(scale/2)/math.sqrt(3),y-scale/2),
			  (x-(scale/2)/math.sqrt(3),y-scale/2),
			  (x-scale/math.sqrt(3), y)]
		output_points = []
		poly_points = []
		for i in input_points:
			res1 = i
			if GLOBAFY:
				res1 = warp(i)
			#res2 = warp(i[1])
			if res1 == False \
					or res1[0] < -SCALE \
					or res1[0] > const.SCREEN_WIDTH + SCALE \
					or res1[1] < -SCALE \
					or res1[1] > const.SCREEN_HEIGHT + SCALE:
				output_points.append(None)
			else:
				#self.rendered_points.append(res1)
				poly_points.append(res1)
				output_points.append(res1)
		if len(poly_points) >= 3:
			self.polys.append(Polygon(poly_points))
			#print(self.obj,flush = True)
			def draw():
				arcade.draw_polygon_filled(poly_points,self.obj.terrain.color)
			
			add_sprite((10000,draw))

		output_lines = []
		for p in range(len(output_points)-1):
			if output_points[p] != None and output_points[p+1] != None:
				output_lines.append((output_points[p],output_points[p+1]))
		if output_points[0] != None and output_points[-1] != None:
			output_lines.append((output_points[0],output_points[-1]))
		if len(output_lines) == 0:
			#print(f"are there out lines {len(output_lines)}",flush = True)
			return False
		def draw():
			for line in output_lines:
				if self.selected:
					dline = ((line[0][0],line[0][1]),(line[1][0],line[1][1]))
					#def draw():
					arcade.draw_line(dline[0][0], dline[0][1], dline[1][0], dline[1][1], arcade.color.RED, 3)
					#print(-dist(line[0][0], line[0][1],const.SCREEN_WIDTH/2,const.SCREEN_HEIGHT/2)-500,flush = True)
					#
				else:
					if self.obj.owner != None:
						#def draw():
						arcade.draw_line(line[0][0], line[0][1], line[1][0], line[1][1], arcade.color.WOOD_BROWN, 3)
						#add_sprite((-dist(line[0][0], line[0][1],const.SCREEN_WIDTH/2,const.SCREEN_HEIGHT/2),draw))
		add_sprite((-dist(x,y,const.SCREEN_WIDTH/2,const.SCREEN_HEIGHT/2)-500,draw))
		#self.render_track = not self.render_track
		"""point_list = ((x-(SCALE/2)/math.sqrt(3),y+SCALE/2),
			  (x+(SCALE/2)/math.sqrt(3),y+SCALE/2),
			  (x+SCALE/math.sqrt(3),y),
			  (x+(SCALE/2)/math.sqrt(3),y-SCALE/2),
			  (x-(SCALE/2)/math.sqrt(3),y-SCALE/2),
			  (x-SCALE/math.sqrt(3), y))
		arcade.draw_line(270, 495, 300, 450, arcade.color.WOOD_BROWN, 3)
		arcade.draw_polygon_outline(point_list, arcade.color.SPANISH_VIOLET)"""
		warped_centerpoint = (x,y)
		if GLOBAFY:
			warped_centerpoint = warp(warped_centerpoint)
		if not warped_centerpoint==False:
			self.last_point = warped_centerpoint
			def draw():
				arcade.draw_text(f"{self.tid}", warped_centerpoint[0], warped_centerpoint[1], arcade.color.WHITE, 12)
			add_sprite((-10000000,draw))
		
			#print(self.last_point,flush = True)
			key = cur_path.in_path(self.obj)
			if key != None:

				key = 90-key
				new_x = x+math.cos(key/180*math.pi)*SCALE
				new_y = y+math.sin(key/180*math.pi)*SCALE
				point = (new_x,new_y)
				if GLOBAFY:
					point = warp(point)
				if not point == False:
					def draw():
						arcade.draw_line(warped_centerpoint[0], warped_centerpoint[1], point[0], point[1], arcade.color.RED, 10)
					add_sprite((-100000,draw))

		return True

	def reset_render(self):
		self.rendered_pos = {}
		self.polys = []

	def click(self,click_point):
		#click_point = Point(x,y)
		for pol in self.polys:
			if click_point.within(pol):
				#self.selected = True
				#print(f"Clicked {self.tid} ({len(self.polys)})",flush = True)
				#print(self.obj.terrain,terrains.terrains,flush = True)
				#if EDIT_MODE:
				#	self.obj.terrain = terrains.terrains[terrains.terrains.index(self.obj.terrain)-1]
				return True
		return False