#!C:\Python27

class World:
	def __init__(self,initialroom):
		self.rooms={}
		self.players={}
		self.rooms[initialroom.name]=initialroom
		self.spawn=self.rooms[initialroom.name]
	def add_room(self,room):
		self.rooms.append(room)
	def add_player(self,player):
		self.players[player.name]=player
		self.spawn.players[player.name]=player
		self.spawn.players[player.name].room=self.spawn
	def move_player(self,room1,room2,playername):
		room2.players[playername]=room1.players[playername]
		room2.players[playername].room=room2
		del room1.players[]
class Room:
	def __init__(self,name,appearance,contents={}):
		self.appearance=appearance
		self.name=name
		self.contents=contents
		self.players={}
class Player:
	def __init__(self,name):
		self.inventory={}
		


playername