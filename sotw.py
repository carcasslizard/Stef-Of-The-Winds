'''
Stef of the Winds
Use Case for pyglet lib

images are not mine

'''
import pyglet
import random
import map1
from pyglet.window import key
version = '0.0.2'
window = pyglet.window.Window(caption='Stef of the Winds V%s' % version)
ROOM_MAX_SIZE = 2
ROOM_MIN_SIZE = 2
MAX_ROOMS = 1

class Tile(pyglet.sprite.Sprite):
	# x and y in pixels
	def __init__(self, image, x, y, blocked, block_sight = None):
		super().__init__(image, x, y)
		
		self.blocked = blocked
		#by default, if a tile is blocked, it also blocks sight
		if block_sight is None: block_sight = blocked
		self.block_sight = block_sight

class Rect:
	def __init__(self, x, y, w, h):
		self.x1 = x
		self.y1 = y
		self.x2 = x + w
		self.y2 = y + h
		
	def center(self):
		center_x = (self.x1 + self.x2) // 2
		center_y = (self.y1 + self.y2) // 2
		return (center_x, center_y)

	def intersect(self, other):
		#returns true if this rectangle intersects with another one
		return (self.x1 <= other.x2 and self.x2 >= other.x1 and
				self.y1 <= other.y2 and self.y2 >= other.y1)

#Still need to make a border drawer
def create_border():
	global map
	pass

def create_room(room):
	global map
	
	for x in range(room.x1 + 1, room.x2):
		for y in range(room.y1 + 1, room.y2):
			map[x][y].image = floorimage
			map[x][y].blocked = False
			map[x][y].block_sight = False

def create_v_tunnel(y1, y2, x):
	global map
	for y in range(min(y1,y2),max(y1,y2) + 1):
		map[x][y].image = floorimage
		map[x][y].blocked = False
		map[x][y].block_sight = False

def create_h_tunnel(x1, x2, y):
	global map
	for x in range(min(x1,x2),max(x1,x2)+1):
		map[x][y].image = floorimage
		map[x][y].blocked = False
		map[x][y].block_sight = False		
	
def make_map():
	global map
	map = []
	for x in range(window.width//32):
		map.append([])
		for y in range(window.width//32):
			map[x].append(Tile(blankimage, x*32, y*32, True))
			
	rooms = []
	num_rooms = 0
	
	for r in range(MAX_ROOMS):
		w = random.randint(ROOM_MIN_SIZE, ROOM_MAX_SIZE)
		h = random.randint(ROOM_MIN_SIZE, ROOM_MAX_SIZE)
		
		x = random.randint(0,(window.width//32) - w )
		y = random.randint(0,(window.height//32) - h )
		
		new_room = Rect(x, y, w, h)
		
		failed = False
		for other_room in rooms:
			if new_room.intersect(other_room):
				failed = True
				break
		if not failed:
			
			
			create_room2(new_room)
			
			(new_x, new_y) = new_room.center()
			
			if num_rooms == 0:
				
				player.x = new_x * 32
				player.y = new_y * 32
				
			else:
				#all rooms after the first:
				#connect to previous room with a tunnel
				
				#center coordinates of previous room
				(prev_x, prev_y) = rooms[num_rooms-1].center()
				
				#if random.randint(0,1) == 1:
				if True:
					#create horizontal then vertical hall
					create_h_tunnel(prev_x, new_x, prev_y)
					create_v_tunnel(prev_y, new_y, new_x)
				else:
					#create vertical then horizontal hall
					create_v_tunnel(prev_y, new_y, prev_x)
					create_h_tunnel(prev_x, new_x, new_y)
		rooms.append(new_room)
		num_rooms += 1
	global visible
	visible = map
		
class Actor(pyglet.sprite.Sprite):
	#generic object for player,monster,item, stairs ect.
	#represent by a sprite on screen 32px x 32px transparnet background
	def __init__(self, image, x=0, y=0):
		x = x * 32
		y = y * 32
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
		#only update position if future pos is not blocked
		currpos = self.currpos()
		tx = currpos[0] + x
		ty = currpos[1] + y
		if not map[tx][ty].blocked:
			self.x += x * 32
			self.y += y * 32

@window.event
def on_draw():
	window.clear()
	
	for x in range(window.width//32):
		for y in range(window.height//32):
			visible[x][y].draw()
	print(player.currpos())
	player.draw()

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
blankimage =  pyglet.resource.image('blank.png')

if __name__ == '__main__':
	
	player  = Actor(playerimage, x = 6, y = 4)
	make_map2()
	pyglet.app.run()