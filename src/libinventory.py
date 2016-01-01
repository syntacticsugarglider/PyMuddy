#!python
class Inventory:
	def __init__(self):
		self.items={}
	def _updatejson(self):
		pass
	def loadfromfile(self,filename):
		pass
	def savetofile(self,filename):
		pass
	def additem(self,name,item):
		self.items[name]=item
	def removeitem(self,name):
		del self.items[name]
	def getItemByName(self,name)
		return self.items[name]
