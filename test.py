import pyglet
from pyglet.window import key
version = '0.0.5'

#default window is 640 x 480
window = pyglet.window.Window(caption='Stef of the Winds V%s' % version)

TILESIZE = 32
UNIT = TILESIZE

#Game Objects
"""
class Player(pyglet.sprite.Sprite):
	gloabl playerimage

	def __init__(self):
		x = 288
		y = 0
		super().__init__(self.playerimage, x, y)
"""
'''
class Tile(pyglet.sprite.Sprite):
	image = 
	def __init__self(self):
		super().__init(self,image)
'''
'''
class Map(object):
	passs
'''
@window.event
def on_draw():
	window.clear()
	background.draw()
	player.draw()
	
@window.event
def on_key_press(symbol, modifiers):
	if symbol == key.LEFT:
		player.x += -UNIT
	elif symbol == key.RIGHT:
		player.x += UNIT
	elif symbol == key.UP:
		player.y += UNIT
	elif symbol == key.DOWN:
		player.y += -UNIT

# Resource Loading
pyglet.resource.path = ['resources']
pyglet.resource.reindex()

playerimage = pyglet.resource.image('player.png')
backgroundimage = pyglet.resource.image('background.png')

#Start Game
if __name__ == '__main__':
	player  = pyglet.sprite.Sprite(playerimage, x=288)
	background = pyglet.sprite.Sprite(backgroundimage)
	
	pyglet.app.run()
