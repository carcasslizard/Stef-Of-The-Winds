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


'''
I need to split up the code fro drawing the room and border for the functions below.
Should make it easier to get them to do what they need to without being complex;
Maybe sperate function? ie create_room() and create_roomborder()				
'''

def create_room(room):
	global map
	for x in range(room.x1 + 1, room.x2):
		for y in range(room.y1, room.y2):
			if x in [room.x1, room.x2-1] or y in [room.y1, room.y2-1]:
				if map[x][y].image != floorimage:
					map[x][y].image = wallimage
					map[x][y].blocked = True
					map[x][y].block_sight = True
			else:
				#make floor
				map[x][y].image = floorimage
				map[x][y].blocked = False
				map[x][y].block_sight = False

def create_room2(room):
	global map
	
	for x in range(room.x1 + 1, room.x2):
		for y in range(room.y1 + 1, room.y2):
			map[x][y].image = floorimage
			map[x][y].blocked = False
			map[x][y].block_sight = False

def create_v_tunnel(y1, y2, x):
	global map
	'''
	#create floor
	for y in range(min(y1,y2),max(y1,y2)):
		map[x][y].image = wallimage
				map[x][y].blocked = True
				map[x][y].block_sight = True
	#create wall around floor except where there is floor
	
	'''
	
	hall = Rect(x, min(y1, y2), 3, abs(y2-y1))
	create_room(hall)
	'''
	#x is middle on tunnel
	#willmake walls on either side
	for x2 in range((x - 1),((x + 1) + 1)):
		for y in range(min(y1, y2), max(y1, y2) + 1):
			if map[x2][y].image in [blankimage,wallimage]:
				if x2 in [x-1, x+1]:
					map[x2][y].image = wallimage
					map[x2][y].blocked = True
					map[x2][y].block_sight = True
				
				else:
					map[x2][y].image = floorimage
					map[x2][y].blocked = False
					map[x2][y].block_sight = False
	'''
					
def create_h_tunnel(x1, x2, y):
	global map
	hall = Rect(min(x1, x2), y , abs(x2-x1), 3 )
	create_room(hall)
	'''
	#y is middle on tunnel
	#willmake walls on either side
	for y2 in range((y - 1),(y + 1) + 1):
		for x in range(min(x1, x2), max(x1, x2) + 1):
			if map[x][y2].image in [blankimage,wallimage]:
				if y2 in [y-1, y+1]:
					map[x][y2].image = wallimage
					map[x][y2].blocked = True
					map[x][y2].block_sight = True
				
				else:
					map[x][y2].image = floorimage
					map[x][y2].blocked = False
					map[x][y2].block_sight = False
	'''

def create_v_tunnel2(y1, y2, x):
	global map
	for y in range(min(y1,y2),max(y1,y2) + 1):
		map[x][y].image = floorimage
		map[x][y].blocked = False
		map[x][y].block_sight = False

def create_h_tunnel2(x1, x2, y):
	global map
	for x in range(min(x1,x2),max(x1,x2)+1):
		map[x][y].image = floorimage
		map[x][y].blocked = False
		map[x][y].block_sight = False		
	
def make_map():
	global map
	map = []	
	#create map and set tile sprites
	for x in range(window.width//32):
		map.append([])
		for y in range(window.width//32):
			#convert map x coord into pix x coord by *32
			'''
			#creates map based on map1.py vars
			if (x,y) in map1.floorlist:
				map[x].append(Tile(floorimage, x*32, y*32, False))
			elif (x,y) in map1.walllist:
				map[x].append(Tile(wallimage, x*32, y*32, True))
			else:
				map[x].append(Tile(blankimage, x*32, y*32, True))
			'''
			#makes a blank map
			map[x].append(Tile(blankimage, x*32, y*32, True))
	room = Rect(0,0,10,10)
	room2 = Rect(0, 6, 10, 10)
	create_room(room)
	create_room(room2)
	create_v_tunnel(4,8,4)
	create_h_tunnel(4,18,4)
	create_v_tunnel(4,10,16)

def make_map2():
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