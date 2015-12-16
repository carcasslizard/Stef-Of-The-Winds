'''
Stef of the Winds
Use Case for pyglet lib

images are not mine

'''
import pyglet
import random
from pyglet.window import key
VERSION = '0.0.4'
#Screen Size in pixels
SCREEN_WIDTH = 960
SCREEN_HEIGHT = 736
window = pyglet.window.Window(SCREEN_WIDTH, SCREEN_HEIGHT, caption='Stef of the Winds V%s' % VERSION)
#map width in tiles
MAP_WIDTH = 960 // 32
MAP_HEIGHT = 480 // 32
#GUI panel width in tiles
PANEL_WIDTH = 960 // 32
PANEL_HEIGHT = 256 // 32
#info box dimenisons in tiles
INFOBOX_WIDTH = round(PANEL_WIDTH * )
INFOBOX_HEIGHT = PANEL_HEIGHT
#status box dimensions in tiles
STATBOX_WIDTH = 
STATBOX_HEIGHT = PANEL_HEIGHT
#dungeon generator settings
ROOM_MAX_SIZE = 4
ROOM_MIN_SIZE = 3
MAX_ROOMS = 20
MAX_ROOM_MONSTERS = 1

class Actor(pyglet.sprite.Sprite):
	#generic object for player,monster,item, stairs ect.
	#represent by a sprite on screen 32px x 32px transparnet background
	def __init__(self, image, x=0, y=0, blocks = False):
		x = x * 32
		y = y * 32
		super().__init__(image, x, y)
		self.blocks = blocks
	
	def currpos(self):
		x = self.x // 32
		y = self.y // 32
		return (x,y)
	
	def updateimage(self,image):
		self.image = image
		return self
		
	def toggle_visible(self):
		self.visible = not self.visible
		return self
	
	def move(self, x, y):
		#move by tiles ie) (1,0) is a step right
		#only update position if future pos is not blocked
		currpos = self.currpos()
		tx = currpos[0] + x
		ty = currpos[1] + y
		if not is_blocked(tx, ty):
			self.x += x * 32
			self.y += y * 32
			
			
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

def place_actors(room):
	#choose random num of monsters
	num_monsters = random.randint(0,MAX_ROOM_MONSTERS)
	
	for i in range(num_monsters):
		#choose random spot for monster
		x = random.randint(room.x1 + 1, room.x2 - 1)
		y = random.randint(room.y1 + 1, room.y2 - 1)
		
		if random.randint(0,100) < 80: #80 percent change of goblin
			#create goblin
			monster = Actor(goblinimage, x, y, True)
		else:
			#create soldier
			monster = Actor(soldierimage, x, y, True)
		actors.append(monster)
	
def place_stairs(room):
	global dmap,stairs
	x,y = room.center()
	stairs = Actor(stairimage, x, y)
	
def create_border():
	global dmap
	for x in range(window.width//32):
		for y in range(window.width//32):
			if dmap[x][y].image == floorimage:
				for x2 in range(x - 1, x + 2):
					for y2 in range(y - 1, y + 2):
						if dmap[x2][y2].image == blankimage:
							dmap[x2][y2].image = wallimage

def create_room(room):
	global dmap
	#go through the tiles in the rectangle and make them passable and floor image
	for x in range(room.x1 + 1, room.x2):
		for y in range(room.y1 + 1, room.y2):
			dmap[x][y].image = floorimage
			dmap[x][y].blocked = False
			dmap[x][y].block_sight = False

def create_v_tunnel(y1, y2, x):
	global dmap
	#vertical tunnel min() and max() are used in case y1>y2
	for y in range(min(y1,y2), max(y1,y2) + 1):
		dmap[x][y].image = floorimage
		dmap[x][y].blocked = False
		dmap[x][y].block_sight = False

def create_h_tunnel(x1, x2, y):
	global dmap
	#horizontal tunnel
	for x in range(min(x1,x2), max(x1,x2) + 1):
		dmap[x][y].image = floorimage
		dmap[x][y].blocked = False
		dmap[x][y].block_sight = False		
	
def make_map():
	global dmap, player, labels, actors
	labels = []
	actors = []
	#fill map with "blocked" blank image tiles
	dmap = []
	for x in range(window.width//32):
		dmap.append([])
		for y in range(window.width//32):
			dmap[x].append(Tile(blankimage, x*32, y*32, True))
			
	rooms = []
	num_rooms = 0
	
	for r in range(MAX_ROOMS):
		#random width and height
		w = random.randint(ROOM_MIN_SIZE, ROOM_MAX_SIZE)
		h = random.randint(ROOM_MIN_SIZE, ROOM_MAX_SIZE)
		#random position without going out of the boundaries of the map
		x = random.randint(0,((window.width//32) - w - 1))
		y = random.randint(0,((window.height//32) - h - 1))
		
		#"Rect" class makes rectangles easier to work with
		new_room = Rect(x, y, w, h)
		
		#run through the other rooms and see if they intersect with this one
		failed = False
		for other_room in rooms:
			if new_room.intersect(other_room):
				failed = True
				break
				
		if not failed:
			#this means there are no intersections, so this room is valid
			create_room(new_room)
			
			#center coordinates of new room, will be useful later
			(new_x, new_y) = new_room.center()
			
			#label rooms
			room_no = chr(65+num_rooms)
			labels.append(pyglet.text.Label(room_no,
						  font_name='Times New Roman',
						  font_size=12, color = (0, 0, 0, 255),
						  x = new_x * 32, y = new_y * 32))
			
			if num_rooms == 0:
				#this is the first room, where the player starts at
				player.x = new_x * 32
				player.y = new_y * 32
				
			else:
				#all rooms after the first:
				#connect to previous room with a tunnel
				
				#center coordinates of previous room
				(prev_x, prev_y) = rooms[num_rooms - 1].center()
				
				if random.randint(0,1) == 1:
					#create horizontal then vertical hall
					create_h_tunnel(prev_x, new_x, prev_y)
					create_v_tunnel(prev_y, new_y, new_x)
				else:
					#create vertical then horizontal hall
					create_v_tunnel(prev_y, new_y, prev_x)
					create_h_tunnel(prev_x, new_x, new_y)
					
				place_actors(new_room)
					
			rooms.append(new_room)
			num_rooms += 1
	place_stairs(rooms[-1])
	create_border()

def is_blocked(x, y):
	if dmap[x][y].blocked:
		return True
	for actor in actors:
		if actor.blocks and actor.x // 32 == x and actor.y // 32== y:
			return False
	return False
@window.event
def on_draw():
	window.clear()
	#make new level if player on stairs
	if player.currpos() == stairs.currpos():
		make_map()
	for x in range(window.width//32):
		for y in range(window.height//32):
			dmap[x][y].draw()
	stairs.draw()
	for actor in actors:
		actor.draw()
	for label in labels:
		#break
		label.draw()
	print(player.currpos())
	player.draw()

@window.event
def on_text_motion(motion):
	if motion ==  pyglet.window.key.MOTION_UP:
		player.mover(0,1)
'''
def on_key_press(symbol, modifiers):
	if symbol == key.LEFT:
		player.move(-1,0)
	elif symbol == key.RIGHT:
		player.move(1,0)
	elif symbol == key.UP:
		player.move(0,1)
	elif symbol == key.DOWN:
		player.move(0,-1)
'''

# Resource Loading
pyglet.resource.path = ['resources']
pyglet.resource.reindex()

playerimage = pyglet.resource.image('player.png')
wallimage = pyglet.resource.image('wall.png')
floorimage = pyglet.resource.image('floor_hall.png')
blankimage =  pyglet.resource.image('blank.png')
stairimage = pyglet.resource.image('stairs.png')
soldierimage = pyglet.resource.image('soldier.png')
goblinimage = pyglet.resource.image('goblin.png')

if __name__ == '__main__':
	
	player  = Actor(playerimage, x = 6, y = 4, blocks=True)
	make_map()
	pyglet.app.run()
	print('done')