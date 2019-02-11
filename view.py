import arcade
import model
import math

#height of 1 tile
SCALE = 150
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 1000
GLOBE_RAD = 150
#PI = 3.141592653

def dist(x1,y1,x2,y2):
	return math.sqrt((x1-x2)**2+(y1-y2)**2)

def change_rad(dif):
	global GLOBE_RAD
	if dif > 0 or GLOBE_RAD > SCALE/3:
		GLOBE_RAD += dif

class MyGame(arcade.Window):
	""" Our custom Window Class"""
	model = None
	tiles = {}
	render_track = False
	center_tile = None
	cen_x = SCREEN_WIDTH/2
	cen_y = SCREEN_HEIGHT/2
	mouse_down = False
	right_down = False

	def __init__(self,model):
		""" Initializer """
		# Call the parent class initializer
		super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, "Sprite Example")

		# Set the working directory (where we expect to find files) to the same
		# directory this .py file is in. You can leave this out of your own
		# code, but it is needed to easily run the examples using "python -m"
		# as mentioned at the top of this program.
		#file_path = os.path.dirname(os.path.abspath(__file__))
		#os.chdir(file_path)
		self.model = model

		# Don't show the mouse cursor
		self.set_mouse_visible(True)

		arcade.set_background_color(arcade.color.BLACK)

	def setup(self):
		#self.game_board = boss("boss")
		self.center_tile = self.model.base_tile
		
		
		rendered = []
		
		
	def recursive_render(self,start,x,y):
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
		#if x>SCREEN_WIDTH+SCALE or x<-SCALE or y>SCREEN_HEIGHT+SCALE or y<-SCALE:
		#	return
		
		#render, if it's already been renderted, closes
		if not this.render(x,y,start.tid):
			return

		if dist(x,y,SCREEN_WIDTH/2,SCREEN_HEIGHT/2) < dist(self.cen_x,self.cen_y,SCREEN_WIDTH/2,SCREEN_HEIGHT/2):
			self.cen_x = x
			self.cen_y = y
			self.center_tile = start

		for key, value in start.adjacent.items():
			if value != None:
				key = 90-key
				new_x = x+math.cos(key/180*math.pi)*SCALE
				new_y = y+math.sin(key/180*math.pi)*SCALE
				self.recursive_render(value,new_x,new_y)

	def on_draw(self):
		""" Draw everything """
		arcade.start_render()
		#self.coin_list.draw()
		#self.player_list.draw()
		self.render_track = not self.render_track

		for t in self.tiles.values():
			t.reset_render()

		self.recursive_render(self.center_tile,self.cen_x,self.cen_y)
		arcade.draw_circle_outline(SCREEN_WIDTH/2, SCREEN_HEIGHT/2, GLOBE_RAD, arcade.color.WOOD_BROWN, 3)
		#arcade.finish_render()





	def on_mouse_motion(self, x, y, dx, dy):
		if self.mouse_down:
			self.cen_x += dx
			self.cen_y += dy
		if self.right_down:
			change_rad(dx)
		pass

	def on_mouse_release(self,x, y, button, modifiers):
		if button == 1:
			self.mouse_down = False
		elif button == 4:
			self.right_down = False
		pass

	def on_mouse_press(self,x,y,button,modifiers):
		print(button,modifiers,flush = True)
		if button == 1:
			self.mouse_down = True
		elif button == 4:
			self.right_down = True
		pass

	def update(self, delta_time):
		""" Movement and game logic """
	   #print(f"updating {delta_time}",flush=True)

		# Call update on all sprites (The sprites don't do much in this
		# example though.)
		pass

#reterns false if point is not rendered
#returns (x,y) of new point, if rendered
def warp(point):
	radians = dist(point[0],point[1],SCREEN_WIDTH/2,SCREEN_HEIGHT/2)
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
	point_angle = math.atan2(point[1]-SCREEN_HEIGHT/2,point[0]-SCREEN_WIDTH/2)
	new_point = [-1,-1]
	new_point[0] = math.cos(point_angle)*true_d + SCREEN_WIDTH/2
	new_point[1] = math.sin(point_angle)*true_d + SCREEN_HEIGHT/2

	return new_point


class tile:
	obj = None
	render_track = False
	rendered_pos = {}

	def __init__(self,coresponding_object):
		self.obj = coresponding_object
		self.reset_render()
		return

	def render(self,x,y,tid):
		x = int(x)
		y = int(y)
		if x in self.rendered_pos:
			if y in self.rendered_pos[x]:
				return False
			else:
				self.rendered_pos[x].add(y)
		else:
			self.rendered_pos[x] = set([y])
		input_LINES = [((x-(SCALE/2)/math.sqrt(3),y+SCALE/2),
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
				(x-(SCALE/2)/math.sqrt(3),y+SCALE/2))]
		output_points = []
		for i in input_LINES:
			res1 = warp(i[0])
			res2 = warp(i[1])
			if res1 == False or res2 == False:
				pass
			else:
				output_points.append((res1,res2))
		if len(output_points) == 0:
			return False
		for line in output_points:
			arcade.draw_line(line[0][0], line[0][1], line[1][0], line[1][1], arcade.color.WOOD_BROWN, 3)

		#self.render_track = not self.render_track
		"""point_list = ((x-(SCALE/2)/math.sqrt(3),y+SCALE/2),
			  (x+(SCALE/2)/math.sqrt(3),y+SCALE/2),
			  (x+SCALE/math.sqrt(3),y),
			  (x+(SCALE/2)/math.sqrt(3),y-SCALE/2),
			  (x-(SCALE/2)/math.sqrt(3),y-SCALE/2),
			  (x-SCALE/math.sqrt(3), y))
		arcade.draw_line(270, 495, 300, 450, arcade.color.WOOD_BROWN, 3)
		arcade.draw_polygon_outline(point_list, arcade.color.SPANISH_VIOLET)"""
		warped_centerpoint = warp((x,y))
		if not warped_centerpoint==False:
			arcade.draw_text(f"{tid}", warped_centerpoint[0], warped_centerpoint[1], arcade.color.WHITE, 12)
		return True

	def reset_render(self):
		self.rendered_pos = {}