import view
import model
import _thread
import arcade

class main:

	model = None
	view = None

	def __init__(self):
		self.model = model.model(4,4)
		self.view = view.MyGame(self.model)
		self.view.setup()
		arcade.run()

		while True:
			key = input()
			if key == "exit":
				return


if __name__ == "__main__":
	main()

