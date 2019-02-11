import arcade
import os
import globe
import math
import _thread
import view
import model
import random
import time
import event_bus
from frames import actions
from constants import option
import controlers
import sys, traceback

# --- Constants ---
SPRITE_SCALING_PLAYER = 0.5
SPRITE_SCALING_COIN = 0.2
COIN_COUNT = 50

SCREEN_SCALE = 0.5
SCREEN_WIDTH = int(3000*SCREEN_SCALE)
SCREEN_HEIGHT = int(2000*SCREEN_SCALE)
CARD_SCALE = 0.5*SCREEN_SCALE
BASE_TEXTURE = arcade.load_texture("images/back.png")
#BASE_TEXTURE.height = BASE_TEXTURE.height*SCREEN_SCALE
#BASE_TEXTURE.width = BASE_TEXTURE.width*SCREEN_SCALE
BACKGROUND_TEXTURE = arcade.load_texture("images/blue_background2.png")
CPU_TEXTURE = arcade.load_texture("images/cpu_frame.png")
POINT_TEXTURE = arcade.load_texture("images/pointer.png")
BUTTON_TEXTURE = arcade.load_texture("images/button.png")
CARD_BUTTON_TEXTURE = arcade.load_texture("images/largebutton.png")
CARD_BUTTON_GREEN = [86,197,1]
SCROLL_TEXTURE = arcade.load_texture("images/scroll.png")
QUESTION_TEXTURE = arcade.load_texture("images/question.png")

SCROLL_SPEED = 1

display_special = None

class preview_obj():
	last_x = -1
	last_y = -1
	cur_card = None
	consumed = False

PREVIEW = preview_obj()

#Constantly checks if car effects are duplicating or deleting cards



class mouse_obj():
	consumed = False
	x = 0
	y = 0
	silent = False

	def __init__(self,x,y):
		self.x = x
		self.y = y


class MyGame(arcade.Window):
	""" Our custom Window Class"""
	game_board = None

	def __init__(self):
		""" Initializer """
		# Call the parent class initializer
		super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, "Sprite Example")

		# Set the working directory (where we expect to find files) to the same
		# directory this .py file is in. You can leave this out of your own
		# code, but it is needed to easily run the examples using "python -m"
		# as mentioned at the top of this program.
		file_path = os.path.dirname(os.path.abspath(__file__))
		os.chdir(file_path)

		# Variables that will hold sprite lists
		#self.player_list = None
		#self.coin_list = None

		# Set up the player info
		#self.player_sprite = None
		#self.score = 0

		# Don't show the mouse cursor
		self.set_mouse_visible(True)

		arcade.set_background_color(arcade.color.AMAZON)

	def setup(self):
		self.game_board = boss("boss")
		
		""" Set up the game and initialize the variables. """

		# Sprite lists
		#self.player_list = arcade.SpriteList()
		#self.coin_list = arcade.SpriteList()

		# Score
		#self.score = 0

		# Set up the player
		# Character image from kenney.nl
		#self.player_sprite = arcade.Sprite("images/character.png", SPRITE_SCALING_PLAYER)
		#self.player_sprite.center_x = 50
		#self.player_sprite.center_y = 50
		#self.player_list.append(self.player_sprite)

		# Create the coins
		"""for i in range(COIN_COUNT):

			# Create the coin instance
			# Coin image from kenney.nl
			coin = arcade.Sprite("images/coin_01.png", SPRITE_SCALING_COIN)

			# Position the coin
			coin.center_x = random.randrange(SCREEN_WIDTH)
			coin.center_y = random.randrange(SCREEN_HEIGHT)

			# Add the coin to the lists
			self.coin_list.append(coin)"""

	def on_draw(self):
		""" Draw everything """
		arcade.start_render()
		#self.coin_list.draw()
		#self.player_list.draw()

		# Put the text on the screen.
		#output = f"Score: {self.score}"

		#arcade.draw_text(output, 10, 20, arcade.color.WHITE, 14)
		scale = 0.95
		arcade.draw_texture_rectangle(SCREEN_WIDTH/2, SCREEN_HEIGHT/2,SCREEN_WIDTH, \
							  SCREEN_HEIGHT, BACKGROUND_TEXTURE, 0)

		
		self.game_board.draw(SCREEN_WIDTH/2,SCREEN_HEIGHT/2)

		#arcade.finish_render()





	def on_mouse_motion(self, x, y, dx, dy):
		#PREVIEW.last_x = x
		#PREVIEW.last_y = y
		PREVIEW.cur_card = None
		move_move_obj = preview_obj()
		move_move_obj.last_x = x
		move_move_obj.last_y = y
		self.game_board.mouse_move(move_move_obj,x,y)
		#PREVIEW = move_move_obj
		#print("MOVED",PREVIEW.cur_card,flush = True)
		
		""" Handle Mouse Motion """

		# Move the center of the player sprite to match the mouse x, y
		#self.player_sprite.center_x = x
		#self.player_sprite.center_y = y
		#self.game_board.use_mouse_motion(x,y,dx,dy)
		pass

	def on_mouse_release(self,x, y, button, modifiers):
		self.game_board.mouse_up(mouse_obj(x,y),x,y)

	def update(self, delta_time):
		""" Movement and game logic """
	   #print(f"updating {delta_time}",flush=True)

		# Call update on all sprites (The sprites don't do much in this
		# example though.)
		pass




def sort_by_depth(drawn):
	return drawn.depth

class drawable:
	jminx = 0
	jminy = 0
	jmaxx = 0
	jmaxy = 0
	children = {}
	name = ""
	gone = True
	depth = 0

	def __init__(self,name):
		self.children = {}
		self.name = name

	def draw(self):
		#for c in self.children.values():
		#	c.set_gone()
		#self.children = []
		#self.jminx = self.jminy = self.jmaxx = self.jmaxy = 0
		return

	def clicked(self,x,y):
		return

	def set_juristiction(self,jminx,jminy,jmaxx,jmaxy):
		self.jminx = jminx
		self.jminy = jminy
		self.jmaxx = jmaxx
		self.jmaxy = jmaxy
		self.gone = False
		#arcade.draw_rectangle_outline(self.jminx, self.jminy, self.jmaxx-self.jminx,  self.jmaxy-self.jminy,arcade.color.RED,2,0)
		#arcade.draw_point(self.jminx, self.jminy,arcade.color.BLUE,10)
		#arcade.draw_point(self.jmaxx, self.jmaxy,arcade.color.BLUE,10)

		

	def assemble_juristiction(self):
		self.jminx = math.inf
		self.jminy = math.inf
		self.jmaxx = -math.inf
		self.jmaxy = -math.inf
		self.gone = True

		for c in self.children.values():
			if not c.gone:
				self.gone = False
				if c.jminx < self.jminx:
					self.jminx = c.jminx
				if c.jminy < self.jminy:
					self.jminy = c.jminy
				if c.jmaxx > self.jmaxx:
					self.jmaxx = c.jmaxx
				if c.jmaxy > self.jmaxy:
					self.jmaxy = c.jmaxy

		#if not self.gone:
		#width = self.jmaxx-self.jminx
		#height = self.jmaxy-self.jminy
		#arcade.draw_rectangle_outline(self.jminx+width/2, self.jminy+height/2, width,height,arcade.color.RED,2,0)
		

	def get_drawable(self,type,name):
		if name in self.children:
			return self.children[name]
		else:
			new_drawable = type(name)
			self.children[name] = new_drawable
			return new_drawable

	def set_gone(self):
		self.gone = True
		self.jminx = math.inf
		self.jminy = math.inf
		self.jmaxx = -math.inf
		self.jmaxy = -math.inf
		for c in self.children.values():
			c.set_gone()

	def mouse_move(self,preview,x,y):
		if preview.consumed == False and self.check_collision(x,y):
			vals = list(self.children.values())
			vals.sort(key = sort_by_depth)
			for c in vals:
				#print(c,c.depth,flush = True)
				if not c.gone:
					c.mouse_move(preview,x,y)

	def mouse_up(self,mouse,x,y):
		if mouse.consumed == False and self.check_collision(x,y):
			vals = list(self.children.values())
			vals.sort(key = sort_by_depth)
			for c in vals:
				#print(c,c.depth,flush = True)
				if not c.gone:
					c.mouse_up(mouse,x,y)

	def check_collision(self,x,y):
		if not self.gone and x > self.jminx and x < self.jmaxx \
				and y > self.jminy and y < self.jmaxy:
			return True
		return False


def draw_stack_size(stack,x,y,scale = 1):
	x = x + BASE_TEXTURE.width*CARD_SCALE*0.5*scale-30*SCREEN_SCALE
	y = y + BASE_TEXTURE.height*CARD_SCALE*0.5*scale-30*SCREEN_SCALE
	arcade.draw_rectangle_filled(x,y , 50*SCREEN_SCALE, 50*SCREEN_SCALE, arcade.color.BLACK)
	wid = len(stack.contents)
	text_offset = 4
	if wid>0:
		text_offset = int(math.log(wid,10))*6 + 4
	arcade.draw_text(f"{len(stack.contents)}", x-text_offset, y-5, arcade.color.WHITE, 15)



class boss(drawable):
	def draw(self,x,y):
		global display_special
		super().draw()


		if PREVIEW.cur_card != None:
			card_ratio = BASE_TEXTURE.height/BASE_TEXTURE.width
			#print("DRAWCARD",card_ratio,SCREEN_HEIGHT-(SCREEN_WIDTH*0.2*card_ratio)/2,SCREEN_WIDTH*0.2,SCREEN_WIDTH*0.2*card_ratio,flush = True)
			arcade.draw_texture_rectangle(SCREEN_WIDTH*0.9, SCREEN_HEIGHT-(SCREEN_WIDTH*0.2*card_ratio)/2, SCREEN_WIDTH*0.2, \
							  SCREEN_WIDTH*0.2*card_ratio, PREVIEW.cur_card.texture, 0)

		

		#player
		new_player = self.get_drawable(player,"player_hand")
		new_player.draw(globe.boss.players[0],0,0,0)
		siz = 200*SCREEN_SCALE
		start = SCREEN_HEIGHT-25*SCREEN_SCALE
		point_scale = 0.25*SCREEN_SCALE
		#Other players
		for i,p in enumerate(globe.boss.players[1:]):
			new_player = self.get_drawable(player_icon,f"player{i}")
			new_player.draw(p,0,start,0)
			#enumerate will start at 0
			if i+1 == globe.boss.whose_turn:
				arcade.draw_texture_rectangle(400*SCREEN_SCALE+100*SCREEN_SCALE, start-100*SCREEN_SCALE, POINT_TEXTURE.width*point_scale, \
							  POINT_TEXTURE.height*point_scale, POINT_TEXTURE, 0)
			start -= siz +25*SCREEN_SCALE

		if 0 == globe.boss.whose_turn:
			arcade.draw_texture_rectangle(400*SCREEN_SCALE+100*SCREEN_SCALE, 800*SCREEN_SCALE, POINT_TEXTURE.width*point_scale, \
						  POINT_TEXTURE.height*point_scale, POINT_TEXTURE, 90)



		lineup = self.get_drawable(pile,"linup")
		lineup.draw(globe.boss.lineup.contents,SCREEN_WIDTH/2,SCREEN_HEIGHT/2+BASE_TEXTURE.height*CARD_SCALE + 15*SCREEN_SCALE,True)

		svstack = self.get_drawable(card,"sv")
		x = SCREEN_WIDTH/2
		y = SCREEN_HEIGHT/2+2.125*(BASE_TEXTURE.height*CARD_SCALE + 15*SCREEN_SCALE)
		if len(globe.boss.supervillain_stack.contents) > 0:
			if globe.boss.supervillain_stack.current_sv == globe.boss.supervillain_stack.contents[-1]: 
				svstack.draw(globe.boss.supervillain_stack.current_sv,x,y,1.25)
			else:
				svstack.draw_down(x,y,1.25)
		draw_stack_size(globe.boss.supervillain_stack,x,y,1.25)

		deck = self.get_drawable(pile,"main_deck")
		if len(globe.boss.main_deck.contents) > 0:
			x = SCREEN_WIDTH/2+2*(BASE_TEXTURE.width*CARD_SCALE + 15)+50*SCREEN_SCALE
			y = SCREEN_HEIGHT/2+2*(BASE_TEXTURE.height*CARD_SCALE + 15*SCREEN_SCALE)
			deck.draw_single_down(globe.boss.main_deck.contents,x,y)
			draw_stack_size(globe.boss.main_deck,x,y)
		else:
			deck.set_gone()

		weaknesses = self.get_drawable(card,"weakness")
		if len(globe.boss.weakness_stack.contents) > 0:
			x = SCREEN_WIDTH/2-(BASE_TEXTURE.width*CARD_SCALE + 15*SCREEN_SCALE)-50*SCREEN_SCALE
			y = SCREEN_HEIGHT/2+2*(BASE_TEXTURE.height*CARD_SCALE + 15*SCREEN_SCALE)
			weaknesses.draw(globe.boss.weakness_stack.contents[-1],x,y)
			draw_stack_size(globe.boss.weakness_stack,x,y)
		weaknesses.set_gone()

		kicks = self.get_drawable(card,"kicks")
		if len(globe.boss.kick_stack.contents) > 0:
			x = SCREEN_WIDTH/2-2*(BASE_TEXTURE.width*CARD_SCALE + 15*SCREEN_SCALE)-50*SCREEN_SCALE
			y = SCREEN_HEIGHT/2+2*(BASE_TEXTURE.height*CARD_SCALE + 15*SCREEN_SCALE)
			kicks.draw(globe.boss.kick_stack.contents[-1],x,y)
			draw_stack_size(globe.boss.kick_stack,x,y)
		else:
			kicks.set_gone()


		destroyed = self.get_drawable(pile,"destroyed")
		if len(globe.boss.destroyed_stack.contents) > 0:
			x = SCREEN_WIDTH/2+(BASE_TEXTURE.width*CARD_SCALE + 15*SCREEN_SCALE)+50*SCREEN_SCALE
			y = SCREEN_HEIGHT/2+2*(BASE_TEXTURE.height*CARD_SCALE + 15*SCREEN_SCALE)
			destroyed.draw_single(globe.boss.destroyed_stack.contents,x,y)
			draw_stack_size(globe.boss.destroyed_stack,x,y)
		else:
			destroyed.set_gone()


		#play area
		for i,p in enumerate(globe.boss.players):
			play = self.get_drawable(pile,f"play{i}")
			play.draw(p.played.contents,SCREEN_WIDTH/2,SCREEN_HEIGHT/2,True)

		#Power display
		power_text = f"{globe.boss.players[globe.boss.whose_turn].played.power} Power"
		if globe.boss.players[globe.boss.whose_turn].discount_on_sv != 0:
			power_text += f" (+{globe.boss.players[globe.boss.whose_turn].discount_on_sv})"

		arcade.draw_text(power_text, SCREEN_WIDTH*0.8,SCREEN_HEIGHT*0.9 , arcade.color.WHITE, 86*SCREEN_SCALE)

		if globe.boss.whose_turn == 0:
			for i,special_option in enumerate(globe.boss.players[globe.boss.whose_turn].played.special_options):
				option = self.get_drawable(button,f"special_action_{i}")
				option.draw(special_option,special_option.button_text,SCREEN_WIDTH*0.9,SCREEN_HEIGHT*0.8 - i*(option.jmaxy-option.jminy +15))

		
		query = self.get_drawable(question,f"question")
		if globe.bus.display != None:
			query.draw(globe.bus.display,SCREEN_WIDTH/2,SCREEN_HEIGHT/2)
		else:
			query.set_gone()

		#print(f"display special {display_special}",flush = True)
		custom = self.get_drawable(question,f"over_display")
		if display_special != None:
			custom_dialog = event_bus.question("",None,display_special.last_contents)
			custom.depth = -100
			custom.draw(custom_dialog,SCREEN_WIDTH/2,SCREEN_HEIGHT/2)
		else:
			custom.set_gone()



		self.assemble_juristiction()


	def mouse_up(self,mouse,x,y):
		global display_special
		query = self.get_drawable(question,f"question")
		if not query.gone and not query.check_collision(x,y):
			mouse.silent = True
		custom = self.get_drawable(question,f"over_display")
		if not custom.gone and not custom.check_collision(x,y):
			display_special = None
			custom.gone = True
		super().mouse_up(mouse,x,y)


class player_icon(drawable): 
	def draw(self,player,x,y,angle):
		super().draw()
		wid = 330*SCREEN_SCALE
		hight = wid/1.96
		arcade.draw_texture_rectangle(wid/2, y - hight/2+7, wid, \
							  hight, CPU_TEXTURE, 0)
		
		
		#arcade.draw_text(player.persona, 10, 20, arcade.color.WHITE, 14)
		#if player.persona != None:

		#	arcade.draw_text(f"{player.pid} - {player.persona.name}\n Deck:{len(player.deck.contents)}, Discard:{len(player.discard.contents)} \nOngoing:{len(player.ongoing.contents)}, Hand:{len(player.hand.contents)}", x, y, arcade.color.BLACK, 15)

		if player.persona != None:
			if player.persona.texture == None:
				player.persona.texture = arcade.load_texture(player.persona.image)
			MC = self.get_drawable(personas,f"{self.name}-persona")
			MC.draw(player.persona,x+player.persona.texture.width*0.2/2*SCREEN_SCALE,y-player.persona.texture.height*0.2/2*SCREEN_SCALE,0.2)

			text_size = 20
			#text_offset = 5
			if player.vp>0:
				text_offset = int(math.log(player.vp,10))*6 + 5
				arcade.draw_circle_filled(x+player.persona.texture.width*0.2/2*SCREEN_SCALE,y-player.persona.texture.height*0.2/2*SCREEN_SCALE, 25*SCREEN_SCALE, arcade.color.BLUE)
				arcade.draw_text(f"{player.vp}",x+player.persona.texture.width*0.2/2*SCREEN_SCALE - text_offset,y-player.persona.texture.height*0.2/2*SCREEN_SCALE-text_size*0.33,arcade.color.WHITE,text_size)



			discard = self.get_drawable(pile,f"{self.name}-discard")
			if len(player.discard.contents) > 0:
				discard.draw_single(player.discard.contents,x+player.persona.texture.width*0.2*1.25*SCREEN_SCALE,y-BASE_TEXTURE.height*0.2*0.25*SCREEN_SCALE,0.2)
			else:
				discard.set_gone()

			deck = self.get_drawable(pile,f"{self.name}-deck")
			if len(player.deck.contents) > 0:
				deck.draw_single_down(player.deck.contents,x+player.persona.texture.width*0.2*1.25*SCREEN_SCALE,y-player.persona.texture.height*0.2*SCREEN_SCALE+BASE_TEXTURE.height*0.2*0.25*SCREEN_SCALE,0.2)
			else:
				deck.set_gone()

			if len(player.ongoing.contents) > 0:
				ongoing = self.get_drawable(pile,f"{self.name}-ongoing")
				ongoing.draw_squished(player.ongoing.contents,x+player.persona.texture.width*0.2*1.75*SCREEN_SCALE,y-BASE_TEXTURE.height*0.2*0.25*SCREEN_SCALE,150,True,0.2)

			hand = self.get_drawable(pile,f"{self.name}-hand")
			if len(player.hand.contents) > 0:
				hand.draw_squished(player.hand.contents,x+player.persona.texture.width*0.2*1.75*SCREEN_SCALE,y-player.persona.texture.height*0.2*SCREEN_SCALE+BASE_TEXTURE.height*0.2*0.25*SCREEN_SCALE,150,False,0.2)
			else:
				hand.set_gone()

			arcade.draw_text(f"Score: {player.score}",x+400*SCREEN_SCALE,y-player.persona.texture.height*0.1/2*SCREEN_SCALE,arcade.color.WHITE,15)

			on_top = self.get_drawable(pile,f"{self.name}-on_top")
			if len(player.over_superhero.contents) > 0:
				on_top.draw_squished(player.over_superhero.contents,x+player.persona.texture.width*0.2*3.5*SCREEN_SCALE,y-player.persona.texture.height*0.2*SCREEN_SCALE+BASE_TEXTURE.height*0.2*0.25*SCREEN_SCALE,150,True,0.2)
			else:
				on_top.set_gone()

		self.assemble_juristiction()




class player(drawable): 
	def draw(self,player,x,y,angle):
		super().draw()


		self.maxy = 2*(BASE_TEXTURE.height*CARD_SCALE+15*SCREEN_SCALE) 
		self.miny = 0
		buffx = 0
		buffy = 0
		if player.persona != None:
			if player.persona.texture == None:
				player.persona.texture = arcade.load_texture(player.persona.image)

			MC = self.get_drawable(personas,"persona")
			MC.draw(player.persona,x+player.persona.texture.width*SCREEN_SCALE/2,self.maxy/2,0.75)
			buffx += player.persona.texture.width*SCREEN_SCALE

			text_size = 20
			#text_offset = 5
			if player.vp>0:
				text_offset = int(math.log(player.vp,10))*6 + 5
				arcade.draw_circle_filled(x+player.persona.texture.width*SCREEN_SCALE/2,self.maxy/2, 50, arcade.color.BLUE)
				arcade.draw_text(f"{player.vp}",x+player.persona.texture.width*SCREEN_SCALE/2- text_offset,self.maxy/2-text_size*0.33,arcade.color.WHITE,text_size)

			

			on_top = self.get_drawable(pile,"on_top")
			if len(player.over_superhero.contents) > 0:
				on_top.draw_squished(player.over_superhero.contents,x+player.persona.texture.width*0.25*SCREEN_SCALE,self.maxy+60,150,True,0.2)
			else:
				on_top.set_gone()

			on_top = self.get_drawable(pile,"under")
			if len(player.under_superhero.contents) > 0:
				on_top.draw_squished(player.under_superhero.contents,x+player.persona.texture.width*0.25*SCREEN_SCALE,self.maxy,150,True,0.2)
			else:
				on_top.set_gone()

			#Score should be written over the other card piles
			arcade.draw_text(f"Score: {player.score}",x+player.persona.texture.width*SCREEN_SCALE/2-15*SCREEN_SCALE,self.maxy+60*SCREEN_SCALE,arcade.color.WHITE,15)

		discard = self.get_drawable(pile,"discard")
		if len(player.discard.contents) > 0:
			x = buffx+CARD_SCALE*BASE_TEXTURE.width/2
			y = BASE_TEXTURE.height*CARD_SCALE/2
			discard.draw_single(player.discard.contents,x,y)
			draw_stack_size(player.discard,x,y)
		else:
			discard.set_gone()

		deck = self.get_drawable(pile,"deck")
		if len(player.deck.contents) > 0:
			x = buffx+CARD_SCALE*BASE_TEXTURE.width/2
			y = 1.5*(BASE_TEXTURE.height*CARD_SCALE+15)
			deck.draw_single_down(player.deck.contents,x,y)
			draw_stack_size(player.deck,x,y)
		else:
			deck.set_gone()

		end_turn_button = self.get_drawable(button,"end_turn")
		x = buffx+CARD_SCALE*BASE_TEXTURE.width/2
		y = 1.5*(BASE_TEXTURE.height*CARD_SCALE+15)
		end_turn_button.draw(actions.ENDTURN,"End Turn",x,y)


		ongoing = self.get_drawable(pile,"ongoing")
		ongoing.draw(player.ongoing.contents,SCREEN_WIDTH-BASE_TEXTURE.width*CARD_SCALE/2,1.5*(BASE_TEXTURE.height*CARD_SCALE+15))

		hand = self.get_drawable(pile,"hand")
		hand.draw(player.hand.contents,SCREEN_WIDTH-BASE_TEXTURE.width*CARD_SCALE/2,BASE_TEXTURE.height*CARD_SCALE/2)



		self.assemble_juristiction()


class scroller_left(drawable):
	depth = -60
	parent = None
	scolling = False
	def draw(self,pile_parent,x,y):
		if self.parent == None:
			self.parent = pile_parent
		width = BASE_TEXTURE.width*CARD_SCALE
		height = BASE_TEXTURE.height*CARD_SCALE
		#arcade.draw_rectangle_filled(x-width*0.25, y, width/2,height,arcade.color.RED)
		arcade.draw_texture_rectangle(x-width*0.25, y, width/2,height,SCROLL_TEXTURE,0)
		
		self.set_juristiction(x-width/2,y-height/2,x,y+height/2)

	def mouse_up(self, mouse, x, y):
		if not mouse.consumed and self.check_collision(x,y):
			
			mouse.consumed = True
			self.parent.scroll_offset = min(self.parent.scroll_offset + SCROLL_SPEED,self.parent.max_offset)

class scroller_right(drawable):
	depth = -60
	parent = None
	scolling = False
	def draw(self,pile_parent,x,y):
		if self.parent == None:
			self.parent = pile_parent
		width = BASE_TEXTURE.width*CARD_SCALE
		height = BASE_TEXTURE.height*CARD_SCALE
		#arcade.draw_rectangle_filled(x+width*0.75, y, width/2+15,height,arcade.color.GREEN)
		arcade.draw_texture_rectangle(x+width*0.75, y, width/2+15,height,SCROLL_TEXTURE,180)
		#arcade.draw_point(x+width/2-15/2,y-height/2,arcade.color.BLUE,10)
		#arcade.draw_point(x+width+15/2,y+height/2,arcade.color.BLUE,10)

		self.set_juristiction(x+width/2-15*SCREEN_SCALE/2,y-height/2,x+width+15*SCREEN_SCALE/2,y+height/2)

	def mouse_up(self, mouse, x, y):
		if not mouse.consumed and self.check_collision(x,y):
			
			mouse.consumed = True
			self.parent.scroll_offset = max(self.parent.scroll_offset - SCROLL_SPEED,0)



class pile(drawable):
	scroll_offset = 0
	max_offset = 0
	last_contents = []
	depth = -1
	single = False

	def __init__(self,name):
		self.last_contents = []

	def ready_card(self,c,x,y,i):
		if c == option.OK or c == option.NO or c == option.DONE or c == option.EVEN or c == option.ODD:
			new_option = self.get_drawable(button,f"option {c}")
			text = "No"
			if c == option.OK:
				text = "OK"
			elif c == option.DONE:
				text = "Done"
			elif c == option.EVEN:
				text = "Even"
			elif c == option.ODD:
				text = "Odd"
			new_option.draw(c,text,x,y,True)
		else:
			new_card = self.get_drawable(card,f"{i}")
			new_card.draw(c,x,y)

	def draw(self,pile_contents,x,y,center = False):
		super().draw()
		self.children = {}

		pos = x - BASE_TEXTURE.width*CARD_SCALE/2
		if center:
			pos = x + min(len(pile_contents),7)/2*(BASE_TEXTURE.width*CARD_SCALE + 15*SCREEN_SCALE) 
		seperation = BASE_TEXTURE.width*CARD_SCALE + 15*SCREEN_SCALE

		if len(pile_contents) > 6:
			self.max_offset = 1 + 2*(len(pile_contents)-7)
			left = self.get_drawable(scroller_left,f"{self.name}-left")
			right = self.get_drawable(scroller_right,f"{self.name}-right")
			start_pos = pos
			pos += (self.scroll_offset%2)*(BASE_TEXTURE.width*CARD_SCALE + 15*SCREEN_SCALE)/2 #- (BASE_TEXTURE.width*CARD_SCALE + 15)/2
			for i,c in enumerate(pile_contents):
				#if i >= self.scroll_offset - 1 - (self.scroll_offset%2) and i <= self.scroll_offset + 6 - (self.scroll_offset%2):
				if i >= int(self.scroll_offset/2) and i <= int(self.scroll_offset/2) + 6:
					self.ready_card(c,pos,y,i)
					
					#new_card = self.get_drawable(card,f"{i}")
					#new_card.draw(c,pos,y)
					#arcade.draw_text(f"{i}",pos,y,arcade.color.WHITE,14)
					pos -= seperation
			left.draw(self,start_pos-6*(BASE_TEXTURE.width*CARD_SCALE + 15*SCREEN_SCALE),y)
			right.draw(self,start_pos,y)
		else:
			self.scroll_offset = 0
			for i,c in enumerate(pile_contents):
				#new_card = self.get_drawable(card,f"{i}")
				#new_card.draw(c,pos,y)
				self.ready_card(c,pos,y,i)
				pos -= seperation
		#for c in self.children.values():
		#	print(c.name,c.jminx,c.jminy,c.jmaxx,c.jmaxy)
		

		self.assemble_juristiction()




	def draw_squished(self,pile_contents,x,y,width,visible,scale = 1):
		# For debug purposes
		self.single = True
		super().draw()
		self.last_contents.clear()
		for c in pile_contents:
			self.last_contents.append(c)


		self.children = {}

		seperation = width/len(pile_contents)
		pos = x
		for i,c in enumerate(pile_contents):
			new_card = self.get_drawable(card,f"{i}")
			
			if visible:
				new_card.draw(c,pos,y,scale)
			else:
				new_card.draw_down(pos,y,scale)
			pos += seperation

		self.assemble_juristiction()


	def draw_single(self,pile_contents,x,y,scale = 1):
		self.single = True
		super().draw()
		self.last_contents.clear()
		for c in pile_contents:
			self.last_contents.append(c)

		if len(pile_contents) > 0:
			top = self.get_drawable(card,f"top_card")
			top.draw(pile_contents[-1],x,y,scale)
		else:
			display_special = None

		self.assemble_juristiction()

#For debug purposes
	def draw_single_down(self,pile_contents,x,y,scale = 1):
		self.single = True
		super().draw()
		self.last_contents.clear()
		for c in pile_contents:
			self.last_contents.append(c)

		if len(pile_contents) > 0:
			top = self.get_drawable(card,f"top_card")
			top.draw_down(x,y,scale)
		else:
			display_special = None

		self.assemble_juristiction()


	def mouse_up(self, mouse, x, y):
		global display_special
		if not self.single:
			super().mouse_up(mouse,x,y)
		elif not self.gone and self.check_collision(x,y) and len(self.last_contents) > 0 and not mouse.consumed:
			#print(f"(Opening display)",flush = True)
			mouse.consumed = True
			display_special = self
			


		

class card(drawable):
	card = None
	depth = -2
	def draw(self,card,x,y,scale = 1):
		super().draw()
		self.card = card
		#print(card.name)
		width = BASE_TEXTURE.width*CARD_SCALE*scale
		height = BASE_TEXTURE.height*CARD_SCALE*scale
		arcade.draw_texture_rectangle(x, y, width, height, card.texture, card.rotation)

		self.set_juristiction(x-width/2,y-height/2,x+width/2,y+height/2)
		#print(self.name,self.jminx,self.jminy,self.jmaxx,self.jmaxy,self)
		#arcade.draw_point(x-width/2, y-height/2, arcade.color.RED, 10)
		#arcade.draw_point(x+width/2, y+height/2, arcade.color.RED, 10)
		if hasattr(card, 'frozen') and len(card.frozen) > 0:
			arcade.draw_circle_filled(x,y,width*0.33,[255,255,255,200])

	def draw_down(self,x,y,scale = 1):
		super().draw()
		self.card = None
		width = BASE_TEXTURE.width*CARD_SCALE*scale
		height = BASE_TEXTURE.height*CARD_SCALE*scale

		arcade.draw_texture_rectangle(x, y, width, height, BASE_TEXTURE, 0)
		#arcade.draw_point(x, y, arcade.color.RED, 10)

		self.set_juristiction(x-width/2,y-height/2,x+width/2,y+height/2)


	def mouse_up(self, mouse, x, y):
		if not mouse.consumed and self.check_collision(x,y) and self.card != None:
			mouse.consumed = True

			if not mouse.silent:
				#print("(Card click)",flush = True)
				globe.bus.card_clicked(self.card)

	def mouse_move(self,preview, x, y):
		if not preview.consumed and self.check_collision(x,y) and self.card != None:
			preview.consumed = True
			preview.cur_card = self.card
			PREVIEW.cur_card = self.card



class personas(drawable):
	persona = None
	def draw(self,persona,x,y,scale = 1):
		super().draw()
		self.persona = persona
		#print(card.name)
		width = persona.texture.width*scale*SCREEN_SCALE
		height = persona.texture.height*scale*SCREEN_SCALE
		if persona.active:
			arcade.draw_texture_rectangle(x, y, width, height, persona.texture, 0)
		else:
			arcade.draw_texture_rectangle(x, y, width, height, BASE_TEXTURE, 0)
		#arcade.draw_point(x, y, arcade.color.RED, 10)
		self.set_juristiction(x-width/2,y-height/2,x+width/2,y+height/2)


	def mouse_move(self,preview, x, y):
		if not preview.consumed and self.check_collision(x,y) and self.persona != None:
			preview.consumed = True
			preview.cur_card = self.persona
			PREVIEW.cur_card = self.persona



class button(drawable):
	action = None
	depth = -55
	silent = False


	def draw(self,action,text,x,y,card_size = False):
		super().draw()
		self.action = action
		#print(card.name)
		width = BASE_TEXTURE.width*CARD_SCALE*0.75
		#golden ratio
		height = width/1.61
		text_offset = (len(text)*6+4)*SCREEN_SCALE
		text_size = 22*SCREEN_SCALE
		if card_size:
			width = BASE_TEXTURE.width*CARD_SCALE
			height = BASE_TEXTURE.height*CARD_SCALE
			arcade.draw_texture_rectangle(x, y, width,height,CARD_BUTTON_TEXTURE,0)
			arcade.draw_text(f"{text}", x-text_offset, y-text_size/3, CARD_BUTTON_GREEN, text_size)
		else:
			#arcade.draw_rectangle_filled(x, y, width, height,[0,0,100], 0)
			arcade.draw_texture_rectangle(x, y, width,height,BUTTON_TEXTURE,0)
			arcade.draw_text(f"{text}", x-text_offset, y-text_size/3, arcade.color.WHITE, text_size)
		
		#print("FHSJFHSJFHSJFHJSF",self.gone,flush= True)

		self.set_juristiction(x-width/2,y-height/2,x+width/2,y+height/2)
		#print(self.name,self.jminx,self.jminy,self.jmaxx,self.jmaxy,self)
		#arcade.draw_point(x-width/2, y-height/2, arcade.color.RED, 10)
		#arcade.draw_point(x+width/2, y+height/2, arcade.color.RED, 10)



	def mouse_up(self, mouse, x, y):
		#print(self.depth)
		if not mouse.consumed and self.check_collision(x,y):
			mouse.consumed = True
			if not mouse.silent and not self.silent:
				globe.bus.button_clicked(self.action)

class question(drawable):
	depth = -50
	question = None
	def draw(self,question,x,y):
		super().draw()
		self.question = question



		width = SCREEN_WIDTH
		height = SCREEN_HEIGHT*0.5

		#arcade.draw_rectangle_filled(x, y, width, height,[0,0,0,225])
		arcade.draw_texture_rectangle(x,y,width,height,QUESTION_TEXTURE,alpha = 0.8)

		if PREVIEW.cur_card != None:
			card_ratio = BASE_TEXTURE.height/BASE_TEXTURE.width
			#print("DRAWCARD",card_ratio,SCREEN_HEIGHT-(SCREEN_WIDTH*0.2*card_ratio)/2,SCREEN_WIDTH*0.2,SCREEN_WIDTH*0.2*card_ratio,flush = True)
			arcade.draw_texture_rectangle(SCREEN_WIDTH*0.2/2, y, SCREEN_WIDTH*0.2, \
							  SCREEN_WIDTH*0.2*card_ratio, PREVIEW.cur_card.texture, 0)


		text_size = 22
		#text_offset = len(question.text)*6+4
		arcade.draw_text(f"{question.text}", x, y+height*0.25, arcade.color.WHITE, text_size)
		if question.card != None:
			choices = self.get_drawable(card,"explain")
			choices.draw(question.card,x-BASE_TEXTURE.width*CARD_SCALE,y+height*0.25)


		choices = self.get_drawable(pile,"choices")
		choices.draw(question.options,x,y-height*0.25,True)



		self.set_juristiction(x-width/2,y-height/2,x+width/2,y+height/2)
		#print(self.name,self.jminx,self.jminy,self.jmaxx,self.jmaxy,self)
		#arcade.draw_point(x-width/2, y-height/2, arcade.color.RED, 10)
		#arcade.draw_point(x+width/2, y+height/2, arcade.color.RED, 10)



##############################################

def thread_game(thread_name,delay):
	try:
		globe.boss.start_game()
	except Exception as e:
		print("ERR:", e)
		print("Exception in user code:")
		print('-'*60)
		traceback.print_exc(file=sys.stdout)
		print('-'*60)


	for i, p in enumerate(globe.boss.player_score):
		print(f"{i}-{globe.boss.players[i].persona.name} got a score of {p}",flush = True)
	print(f"Completed in {globe.boss.turn_number} turns",flush = True)
	
	#time.sleep(1)
	#arcade.run()
	
def main():
	model.choose_sets()
	print("Setting up even bus...",flush = True)
	globe.bus = event_bus.event_bus()
	print("Setting up controlers...",flush = True)
	globe.view = view.view_controler()
	print("Setting up game...",flush = True)
	globe.boss = model.model()



	""" Main method """
	print("Setting up window (1/2)...",flush = True)
	window = MyGame()
	print("Setting up window (2/2)...",flush = True)
	window.setup()
	
	print("About to start game thread.",flush = True)
	_thread.start_new_thread(thread_game,("Game", 2, ))
	print("Game thread started.",flush = True)
	time.sleep(1)
	arcade.run()
	#globe.boss.start_game()
	
	#_thread.start_new_thread(,("View", 2, ))
	
	print("Game ended")
	#arcade.run()


if __name__ == "__main__":
	main()


