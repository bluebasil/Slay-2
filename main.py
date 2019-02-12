import view
import model
import _thread
import arcade
import const

class main:

	model = None
	view = None

	def __init__(self):
		#These must be even!
		self.model = model.model(const.BOARD_WIDTH,const.BOARD_HEIGHT)
		self.view = view.MyGame(self.model)
		self.view.setup()
		arcade.run()

		while True:
			key = input()
			if key == "exit":
				return


if __name__ == "__main__":
	main()

