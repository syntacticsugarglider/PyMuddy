#!python
import libadventure
class RoomLoader:
	def __init__(self,filepath,world):
		self.fp=open(filepath)
		self.path=filepath
		self.worldpointer=world
		self.rooms=[]
		for line in self.fp.readlines():
			self.rooms.append(libadventure.Room("","",fromfile=line.strip("\n\r")))
		for room in self.rooms:
			self.worldpointer.add_room(room)
		self.fp.close()
		del self.fp
