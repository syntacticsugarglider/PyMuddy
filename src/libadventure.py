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
	def move_player(self,room1,room2,playername):
		room1.players[]
		


