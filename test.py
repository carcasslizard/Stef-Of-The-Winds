import pyglet
from pyglet.window import key
version = '0.0.4'
window = pyglet.window.Window(caption='Stef of the Winds V%s' % version)
pyglet.resource.path = ['resources']
pyglet.resource.reindex()

image = pyglet.resource.image('zeld.png')
background = pyglet.resource.image('underground1.png')
backgrounds = pyglet.sprite.Sprite(background)
sprite = pyglet.sprite.Sprite(image, x=288,y=0)

@window.event
def on_key_press(symbol, modifiers):
	if symbol == key.LEFT:
		sprite.x += -32
	elif symbol == key.RIGHT:
		sprite.x += 32
	elif symbol == key.UP:
		sprite.y += 32
	elif symbol == key.DOWN:
		sprite.y += -32
	
@window.event
def on_draw():
	window.clear()
	backgrounds.draw()
	sprite.draw()

pyglet.app.run()
