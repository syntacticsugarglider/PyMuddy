#!C:\Python27
class World:
	def __init__(self,initialroom):
		self.rooms={}
		self.players={}
		self.rooms[initialroom.name]=initialroom
		self.spawn=self.rooms[initialroom.name]
	def add_room(self,room):
		self.rooms[room.name]=room
	def add_player(self,player):
		self.players[player.name]=player
		self.spawn.players[player.name]=player
		self.spawn.players[player.name].room=self.spawn
	def move_player(self,room1,room2,playername):
		room2.players[playername]=room1.players[playername]
		room2.players[playername].room=room2
		del room1.players[playername]
	def process_command(self,command,playername):
		player=self.players[playername]
		extra=""
		if command=="look" or command=="l":
			for key,value in player.room.contents.iteritems():
				extra+="\nYou can also see a "+key+" here"
			for key,value in player.room.players.iteritems():
				if key!=player.name:
					extra+="\n%s is here too!" % key
			return player.room.name+" : "+player.room.appearance+extra
		elif command=="west" or command=="w" or command=="go w" or command=="go west":
			if player.room.west!=None:
				self.move_player(player.room,self.rooms[player.room.west],player.name)
				return player.room.name+" : "+player.room.appearance
			else:
				return "You can't go that way!"
		elif command=="east" or command=="e" or command=="go e" or command=="go east":
			if player.room.east!=None:
				self.move_player(player.room,self.rooms[player.room.east],player.name)
				return player.room.name+" : "+player.room.appearance
			else:
				return "You can't go that way!"
		elif command=="north" or command=="n" or command=="go n" or command=="go north":
			if player.room.north!=None:
				self.move_player(player.room,self.rooms[player.room.north],player.name)
				return player.room.name+" : "+player.room.appearance
			else:
				return "You can't go that way!"
		elif command=="south" or command=="s" or command=="go s" or command=="go south":
			if player.room.south!=None:
				self.move_player(player.room,self.rooms[player.room.south],player.name)
				return player.room.name+" : "+player.room.appearance
			else:
				return "You can't go that way!"
		elif command=="up" or command=="u" or command=="go u" or command=="go up":
			if player.room.up!=None:
				self.move_player(player.room,self.rooms[player.room.up],player.name)
				return player.room.name+" : "+player.room.appearance
			else:
				return "You jump fruitlessly."
		elif command=="down" or command=="d" or command=="go d" or command=="go down":
			if player.room.down!=None:
				self.move_player(player.room,self.rooms[player.room.down],player.name)
				return player.room.name+" : "+player.room.appearance
			else:
				return "You can't go that way!"
		else:
			return "I'm not sure I understand you"
class Room:
	def __init__(self,name,appearance,contents={},west=None,east=None,north=None,south=None,up=None,down=None):
		self.appearance=appearance
		self.name=name
		self.contents=contents
		self.players={}
		self.west=west
		self.east=east
		self.north=north
		self.south=south
		self.up=up
		self.down=down
class Player:
	def __init__(self,name):
		self.inventory={}
		self.name=name