'''
Stef of the Winds
Use Case for pyglet lib

images are not mine

'''
import pyglet
from pyglet.window import key
version = '0.0.2'

window = pyglet.window.Window(caption='Stef of the Winds V%s' % version)

class Tile(pyglet.sprite.Sprite):
	
	def __init__(self, image, x, y, blocked, block_sight = None):
		super().__init__(image, x, y)
		
		self.blocked = blocked
		#by default, if a tile is blocked, it also blocks sight
		if block_sight is None: block_sight = blocked
		self.block_sight = block_sight

def make_map():
	global map
	map = []
	#fill map with unlbocked tiles
	'''
	map = [[ Tile(False)
		for y in range(window.height//32)]
			for x in range(window.width//32) ]
	'''
	for x in range(window.width//32):
		map.append([])
		for y in range(window.width//32):
			map[x].append(Tile(floorimage, x*32, y*32, False))
	
	#test map
	
	map[8][0].blocked = True
	map[8][0].block_sight = True
	map[8][0].image = wallimage
	map[10][0].blocked = True
	map[8][1].blocked = True
	map[10][1].blocked = True
	map[8][2].blocked = True
	map[10][2].blocked = True
	
class Actor(pyglet.sprite.Sprite):
	#generic object for player,monster,item, stairs ect.
	#represent by a sprite on screen 32px x 32px transparnet background
	def __init__(self, image, x=0, y=0):
		super().__init__(image, x, y)
	
	def currpos(self):
		x = self.x // 32
		y = self.y // 32
		return (x,y)
	
	def updateimage(self,image):
		self.image = image
		return self
	
	def move(self, x, y):
		#move by tiles ie) (1,0) is a step right
		
		#check if intended location is passable
		currpos = self.currpos()
		'''
		tx = currpos[0] + 1
		ty = currpos[1] + 1
		if !map[tx][ty].blocked:
			self.x += x * 32
			self.y += y * 32
		'''
		#if passable(
		self.x += x * 32
		self.y += y * 32

@window.event
def on_draw():
	window.clear()
	
	for x in range(window.width//32):
		for y in range(window.height//32):
			map[x][y].draw()
	
	player.draw()
	#print(player.currpos())

@window.event
def on_key_press(symbol, modifiers):
	if symbol == key.LEFT:
		player.move(-1,0)
	elif symbol == key.RIGHT:
		player.move(1,0)
	elif symbol == key.UP:
		player.move(0,1)
	elif symbol == key.DOWN:
		player.move(0,-1)

# Resource Loading
pyglet.resource.path = ['resources']
pyglet.resource.reindex()

playerimage = pyglet.resource.image('player.png')
wallimage = pyglet.resource.image('wall.png')
floorimage = pyglet.resource.image('floor_hall.png')

if __name__ == '__main__':
	player  = Actor(playerimage, x=288) #288 / 32 = 9    starpos(9,0)
	test='test'
	make_map()
	pyglet.app.run()