#!python
import json
import libinventory
import libitems
from datetime import datetime
import sys
from extensionlocals import *
class CommandParser:
	def __init__(self,world):
		self.commands={}
		self.environmentVariables={'commandnotfoundmessages':['I\'m not sure I understand you.']}
		self.referenceArguments={'world':world,'commandprocessor':self,'factory':None,'player':None,'protocol':None}
		self.blockingInput=''
	def addCommand(self,name,function,properties_dict):
		self.commands[name]=(function,properties_dict)
	def setEnv(self,envname,value):
		self.environmentVariables[envname]=value
	def registerReferenceArgument(self,name,argument):
		self.referenceArguments[name]=argument
	def registerCommandAlias(self,origin,alias):
		self.commands[alias]=self.commands[origin]
	def nonBlockingInput(self,callback):
		self.referenceArguments['protocol'].state='WAITING_FOR_INPUT'
		self.referenceArguments['protocol'].inputCallback=callback
	def getCurrentRoom(self):
		return self.referenceArguments['player'].room
	def isPlayerInRoom(self,room,player):
		inRoom=False
		if player in room.players.keys():
			inRoom=True
		if player in room.players.values():
			inRoom=True
		return inRoom
	def transmitToCurrentPlayer(self,line):
		self.referenceArguments['protocol'].sendLine(line)
	def transmitToPlayer(self,line,player):
		try:
			for client in self.referenceArguments['factory'].clients:
				if client.player.name==player.name:
					client.sendLine(line.encode('utf8'))
		except KeyError:
			return False
	def transmitToEveryone(self,line,transmittoself):
		try:
			for client in self.referenceArguments['factory'].clients:
				if factory==client and not transmittoself:
					pass
				else:
					client.sendLine(text.encode('utf8'))
			return True
		except KeyError:
			return False
	def getNetworkClients(self):
		try:
			self.referenceArguments['factory'].clients
		except NameError:
			return []
		return list(self.referenceArguments['factory'].clients)
	def getPlayers(self):
		try:
			self.referenceArguments['factory'].clients
		except NameError:
			return []
		client_list=[]
		for client in list(self.referenceArguments['factory'].clients):
			client_list.append(client.player)
		return client_list
	def parseCommand(self,input,player,factory):
		try:
			if self.referenceArguments['factory']==None and factory!=None:
				self.referenceArguments['factory']=factory
				for client in self.referenceArguments['factory'].clients:
					if client.player.name==player.name:
						self.referenceArguments['protocol']=client
				self.referenceArguments['protocol'].commandParser=self
				self.referenceArguments['protocol'].factory.protocol.factory=self.referenceArguments['factory']=factory
			if self.referenceArguments['player']==None and player!=None:
				self.referenceArguments['player']=player
		except BaseException as e:
			log('WARNING!!!: ENCOUNTERED ERROR AS FOLLOWS WHILE SETTING PARSER REFARGS: %s' % str(e))
		splits=input.strip('\n\r').split(' ')
		try:
			command=self.commands[splits[0].lower()][0]
			properties=self.commands[splits[0].lower()][1]
			if 'args' in properties:
				arguments_required=properties['args']
				argument_list={}
				for argument_name in arguments_required:
					if argument_name=='current_player':
						argument_list['current_player']=player
					else:
						argument_list[argument_name]=self.referenceArguments[argument_name]
			return(True,command(splits[1:],**argument_list))
		except KeyError:
			return (False,self.environmentVariables['commandnotfoundmessages'][0])
#Cthulhu was here
def log(text):
	text2="[%s - gamefiles] %s" % ((str(datetime.now())),text)
	sys.stdout.write(text2)
class World:
	def __init__(self,initialroom):
		self.commandParser=CommandParser(self)
		self.rooms={}
		self.players={}
		self.rooms[initialroom.name]=initialroom
		self.spawn=self.rooms[initialroom.name]
		self.state=''
		self.registerCommands()
	def registerCommands(self):
		def inputCallbackOne(line,protocol):
			mush=searchForItemInHashTable(line,protocol.player.getCurrentRoomContents())
			protocol.sendLine(str(mush).encode('utf8'))
		def phishCommand(line,world=None,commandprocessor=None):
			self.commandParser.nonBlockingInput(inputCallbackOne)
			return('')
		self.commandParser.addCommand('phish',phishCommand,{'args':['world','commandprocessor']})
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
	def remove_player(self,playername):
		del self.players[playername]
	def saytoplayer(self,playername,text,factory,player2):
		try:
			for c in factory.clients:
				if c.player.name==playername and c.player.name!=player2:
					c.sendLine(text.encode('utf8'))
		except:
			pass
	def process_command(self,command,playername,factory=None,player2=None):
		factory=factory
		try:
			command=command.decode('utf8')
		except:
			return "An error ocurred! Please contact the sysadmin and inform him of the situation in which this ocurred."
		command=str(command)
		if command=='':
			return ''
		command_array=command.split()
		player=self.players[playername]
		parsing_response=self.commandParser.parseCommand(command,player,factory)
		if parsing_response[0]:
			return parsing_response[1]
		else:
			pass
		extra=""
		if self.state=='getting_num_items_grab':
			try:
				int(command)
			except:
				return "That's not a valid number!\n Please give a valid number!\n"
			name=self.arbitrary_data_storage
			for key,value in player.room.contents.iteritems():
				for x in name:
					if x in key:
						if int(command)>len(value):
							return "You can't see that many! Please give a smaller number!"
						if int(command)!=0:
							contents_item=True
							try:
								player.inventory.items[key]
							except:
								contents_item=False
							if not contents_item:
								player.inventory.items[key]=[]
							player.inventory.items[key]+=value[0:int(command)]
							if int(len(value))==int(command):
								del player.room.contents[key]
								self.state=''
								return "Taken"
							del player.room.contents[key][0:int(command)]
						self.state=''
						return "Taken"
		if self.state=='getting_num_items_drop':
			try:
				int(command)
			except:
				return "That's not a valid number!\n Please give a valid number!\n"
			name=self.arbitrary_data_storage
			for key,value in player.inventory.items.iteritems():
				for x in name:
					if x in key:
						if int(command)>len(value):
							return "You can't see that many! Please give a smaller number!"
						if int(command)!=0:
							contents_item=True
							try:
								player.room.contents[key]
							except:
								contents_item=False
							if not contents_item:
								player.room.contents[key]=[]
							player.room.contents[key]+=value[0:int(command)]
							if int(len(value))==int(command):
								del player.inventory.items[key]
								self.state=''
								return "Taken"
							del player.inventory.items[key][0:int(command)]
						self.state=''
						return "Dropped"
		command=command.lower()
		if command[0:2]=="x " or command[0:8]=="examine ":
			if command[0:2]=="x ":
				name=command[2:].strip("\n").split()
			if command[0:8]=="examine ":
				name=command[8:].strip("\n").split()
			for key,value in player.room.contents.iteritems():
				for x in name:
					if x in key:
						return("Examining %s - %s" % (key,value.longdescription))
			for key,value in player.inventory.items.iteritems():
				for x in name:
					if x in key:
						return("Examining %s - %s" % (key,value.longdescription))

			return "You can see no such thing."
		if command[0:4]=="get " or command[0:5]=="take " or command[0:5]=="grab ":
			if command[0:4]=="get ":
				name=command[4:].strip("\n").split()
			if command[0:5]=="take " or command[0:5]=="grab ":
				name=command[5:].strip("\n").split()
			for key,value in player.room.contents.iteritems():
				for x in name:
					if x in key:
						if len(value)>1 and self.state!='getting_num_items_grab':
							self.state='getting_num_items_grab'
							self.arbitrary_data_storage=name
							return "How many do you want to %s?" % command.split()[0]
						contents_item=True
						try:
							player.inventory.items[key]
						except:
							contents_item=False
						if not contents_item:
							player.inventory.items[key]=[]
						player.inventory.items[key].append(value[0])
						del player.room.contents[key]
						return "Taken"
			return "You can see no such thing!"
		if command[0:5]=="drop ":
			name=command[5:].strip("\n").split()
			for key,value in player.inventory.items.iteritems():
					for x in name:
						if x in key:
							if len(value)>1:
								self.state='getting_num_items_drop'
								self.arbitrary_data_storage=name
								return "How many do you want to %s?" % command.split()[0]
							contents_item=True
							try:
								player.room.contents[key]
							except:
								contents_item=False
							if not contents_item:
								player.room.contents[key]=[]
							player.room.contents[key].append(value[0])
							del player.inventory.items[key]
							return "Dropped"
			return "You aren't carrying any such thing!"
		if command=="hapl" or command=="hapl mei":
			return "You are a simple noob, standing in a room. This is PyMuddy, a MUD built with Python, or a Multiplayer Adventure without any graphics built with a coding language. It was made by two 1337 ninja coderz/haxxors, zenerboson and guidepupguy, and one silly noobish, MysteryPig. You can type a command and then press enter to do a thing. N makes you go north. W makes you go west. You can figure out the other two, plus up and down. You can type take blah to get an item called blah, if it is in the room. I checks your inventory and health. Drop lets you put a thing down. If you go west twice, there is free candy and an ornate burning chipmunk."
		if command=="help" or command=="noob" or command=="iamanoob" or command=="h" or command=="info":
			return "This is not the command you are looking for. Try hapl mei."
		if command=="i" or command=="inventory":
			data=''
			for key,value in player.inventory.items.iteritems():
				data+='%sx %s\n' % (str(len(value)),value[0].shortdescription)
			if data=="":
				data='Your inventory is empty'
			data+='Your health is currently %s out of a maximum of %s\n' % (str(player.health),str(player.maxhealth))
			return data
		if command=="1337" or command=="haxxor" or command=="1337haxxor":
			return "You are a 1337 |-|4><><0|2.\n   run(notavirus.trojanhorse)\n   init(godmode)\n   init(sopro) \nTentacles wrapped and locked. The system is now under your control. Type 'hack CIA' to continue."
		if command=="hack CIA" or command=="hack cia":
			return "\n >hack CIA.gov/allthesecrets \n...\nSECRETS: Area 51  Illuminati  9/11\n >9/11\n BUSH DID 9/11. 9/11 = 911. 911 has 3 numbers. A triangle has 3 points. Illuminati confirmed. 911. 911 makes you think of the fire department. Fire trucks are red. Red has 3 letters. Illuminati confirmed. BUSH AND THE ILLUMINATI DID 9/11. \n  /\ \n / O\ \n/____\ "
		if command=="look" or command=="l":
			for key,value in player.room.contents.iteritems():
				if len(value)==1:
					extra+="\nYou can also see a "+value[0].shortdescription+" here"
				else:
					extra+="\nYou can also see %s %ss here" % (str(len(value)),value[0].shortdescription)
			for key,value in player.room.players.iteritems():
				if key!=player.name:
					extra+="\n%s is here too!" % key
			return player.room.name+" : "+player.room.appearance+extra
		elif command=="west" or command=="w" or command=="go w" or command=="go west":
			if player.room.west!=None:
				for key,value in self.players.iteritems():
					if value.room==player.room:
						self.saytoplayer(value.name,"%s leaves to the west" % player.name,factory,player2)
				self.move_player(player.room,self.rooms[player.room.west],player.name)
				for key,value in self.players.iteritems():
					if value.room==player.room:
						self.saytoplayer(value.name,"%s enters from the east" % player.name,factory,player2)
				return self.process_command('look',playername)
			else:
				return "You can't go that way!"
		elif command=="east" or command=="e" or command=="go e" or command=="go east":
			if player.room.east!=None:
				for key,value in self.players.iteritems():
					if value.room==player.room:
						self.saytoplayer(value.name,"%s leaves to the east" % player.name,factory,player2)
				self.move_player(player.room,self.rooms[player.room.east],player.name)
				for key,value in self.players.iteritems():
					if value.room==player.room:
						self.saytoplayer(value.name,"%s enters from the west" % player.name,factory,player2)
				return self.process_command('look',playername)
			else:
				return "You can't go that way!"
		elif command=="north" or command=="n" or command=="go n" or command=="go north":
			if player.room.north!=None:
				for key,value in self.players.iteritems():
					if value.room==player.room:
						self.saytoplayer(value.name,"%s leaves to the north" % player.name,factory,player2)
				self.move_player(player.room,self.rooms[player.room.north],player.name)
				return self.process_command('look',playername)
				for key,value in self.players.iteritems():
					if value.room==player.room:
						self.saytoplayer(value.name,"%s enters from the south" % player.name,factory,player2)
			else:
				return "You can't go that way!"
		elif command=="south" or command=="s" or command=="go s" or command=="go south":
			if player.room.south!=None:
				for key,value in self.players.iteritems():
					if value.room==player.room:
						self.saytoplayer(value.name,"%s leaves to the south" % player.name,factory,player2)
				self.move_player(player.room,self.rooms[player.room.south],player.name)
				return self.process_command('look',playername)
				for key,value in self.players.iteritems():
					if value.room==player.room:
						self.saytoplayer(value.name,"%s enters from the north" % player.name,factory,player2)
			else:
				return "You can't go that way!"
		elif command=="up" or command=="u" or command=="go u" or command=="go up":
			if player.room.up!=None:
				for key,value in self.players.iteritems():
					if value.room==player.room:
						self.saytoplayer(value.name,"%s leaves upwards" % player.name,factory,player2)
				self.move_player(player.room,self.rooms[player.room.up],player.name)
				return self.process_command('look',playername)
				for key,value in self.players.iteritems():
					if value.room==player.room:
						self.saytoplayer(value.name,"%s enters from below" % player.name,factory,player2)
			else:
				return "You jump fruitlessly."
		elif command=="down" or command=="d" or command=="go d" or command=="go down":
			if player.room.down!=None:
				for key,value in self.players.iteritems():
					if value.room==player.room:
						self.saytoplayer(value.name,"%s leaves downwards" % player.name,factory,player2)
				self.move_player(player.room,self.rooms[player.room.down],player.name)
				for key,value in self.players.iteritems():
					if value.room==player.room:
						self.saytoplayer(value.name,"%s enters from above" % player.name,factory,player2)
				return self.process_command('look',playername)
			else:
				return "You can't go that way!"
		elif command=="xyzzy":
			return("Honestly? Really? Are you actually saying that? Yes you are.\a")
		elif command=='quit' or command=='exit':
                        return('#exit#')
		elif command_array[0]=='stab' or command_array[0]=='a' or command_array[0]=='kill' or command_array[0]=='attack':
			print(command_array)
			if len(command_array)<4:
				return "You need to specify what to attack and what to attack with!"
			if command_array[1] in player.room.players.keys():
				pass
			else:
				return "You can't see any such person to attack!"
			bleh=None
			for key,value in player.inventory.items.iteritems():
				if command_array[3] in key:
					bleh=key
			if bleh==None:
				return "You don't have that thing!"
			if player.inventory.items[bleh][0].properties['type']=='weapon':
				pass
			else:
				return "That's a silly thing to attack with."
			if not player.can_attack:
				return "You are in no condition to attack!"
			playername2=player.name
			self.players[command_array[1]].take_damage(player.inventory.items[bleh][0].properties['damage'])
			self.saytoplayer(command_array[1],"%s attacks you with a %s! You lose %s life! You are now at %s life!\a" % (player.name,player.inventory.items[bleh][0].properties['stance'],player.inventory.items[bleh][0].properties['damage'],self.players[command_array[1]].health),factory,playername2)
			return "You attack %s, dealing %s damage!" % (command_array[1],player.inventory.items[bleh][0].properties['damage'])
		else:
			return "I'm not sure I understand you"
class Room:
	def __init__(self,name,appearance,contents={},fromfile=None,west=None,east=None,north=None,south=None,up=None,down=None):
		self.appearance=appearance
		self.name=name
		self.contents={}
		self.players={}
		self.west=west
		self.east=east
		self.north=north
		self.south=south
		self.up=up
		self.down=down
		datatypes=[("appearance",self.set_1),("name",self.set_2),("contents",self.set_3),("east",self.set_4),("north",self.set_5),("south",self.set_6),("west",self.set_7),("up",self.set_8),("down",self.set_9)]
		if fromfile!=None:
			try:
				log("Loading room %s\n" % fromfile)
				self.fp=open(fromfile,"r+")
			except BaseException as e:
				log("Warning - Bad room file path %s!\n" % fromfile)
				del self
				return
			self.fp.seek(0)
			for line in self.fp.readlines():
				for datatype in datatypes:
					if line[0:len(datatype[0])]==datatype[0]:
						if datatype[0]!="contents":
							datatype[1](line[len(datatype[0])+1:].strip("\n"))
						else:
							for x in line[len(datatype[0]):].split():
								item=libitems.Item(x)
								log("Loading item %s" % x)
								contents_item=True
								try:
									self.contents[item.name]
								except:
									contents_item=False
								if not contents_item:
									self.contents[item.name]=[]
								self.contents[item.name].append(item)
			try:
				self.fp.close()
				del self.fp
				log("Done! - loaded room name %s\n" % self.name)
			except:
				pass
	def set_1(self,x):
		self.appearance=x
	def set_2(self,x):
		self.name=x
	def set_3(self,x):
		self.contents=x
	def set_4(self,x):
		if x[0]==" ":
			x=x[1:]
		self.east=x
	def set_5(self,x):
		if x[0]==" ":
			x=x[1:]
		self.north=x
	def set_6(self,x):
		if x[0]==" ":
			x=x[1:]
		self.south=x
	def set_7(self,x):
		if x[0]==" ":
			x=x[1:]
		self.west=x
	def set_8(self,x):
		if x[0]==" ":
			x=x[1:]
		self.up=x
	def set_9(self,x):
		if x[0]==" ":
			x=x[1:]
		self.down=x

class Player:
	def __init__(self,name):
		self.health=100
		self.maxhealth=100
		self.can_attack=True
		self.inventory=libinventory.Inventory()
		self.name=name
	def take_damage(self,damage):
		self.health-=int(damage)
		if self.health<=0:
			items=[libitems.Item('knifeaxe.json')]*100000
			self.room.contents[items[0].name]=items
	def getCurrentRoomContents(self):
		return self.room.contents
