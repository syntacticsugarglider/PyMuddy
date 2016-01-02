#!python
import json
class Item:
	def __init__(self,filepath):
		self.shortdescription=""
		self.longdescription=""
		self.name=""
		self.additions=[]
		self.properties={}
		fp=open(filepath,"r+")
		json_dict=json.load(fp)
		fp.seek(0)
		for key,value in json_dict.iteritems():
			del json_dict[key]
			json_dict[key.encode('utf8')]=value.encode('utf8')
		for key,value in json_dict.iteritems():
			if key=='shortdescription':
				self.shortdescription=value
			elif key=='name':
				self.name=value
			elif key=="longdescription":
				self.longdescription=value
			else:
				self.properties[key]=value
	def getProperty(self,property):
		return self.properties[property]
