#!python
import json
class Entity(object):
	def __init__(self,filye=''):
		self.properties={}
		if filye!='':
			fp=open(filye,"r+")
			json_dict=json.load(fp)
			fp.seek(0)
			for key,value in json_dict.iteritems():
				del json_dict[key]
				json_dict[key.encode('utf8')]=value.encode('utf8')
			for key,value in json_dict.iteritems():
				self.properties[key]=value
		try:
			self.shortdescription=self.properties['shortdescription']
			self.longdescription=self.properties['longdescription']
			self.name=self.properties['name']
		except:
			raise NotImplementedError
	def getProperty(self,property):
		return self.properties[property]
	def destroy(self):
		self.properties=None
		self=None
class Item(Entity):
	def __init__(self,filepath):
		self.additions=''
		super(Item,self).__init__(filepath)
