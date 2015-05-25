#!C:\Python27
print("Importing and configuring base modules (datetime,sys)..."),
from datetime import datetime
import sys
def log(text):
	text2="[%s - server] %s" % ((str(datetime.now())),text)
	sys.stdout.write(text2)
print("Done!")
log("Loading twisted.internet.reactor,protocol,endpoints...\n")
from twisted.internet import reactor, protocol, endpoints
log("Done!\n")
log("Loading twisted.protocols.basic...\n")
from twisted.protocols import basic
log("Done!\n")
log("Loading libadventure...\n")
import libadventure
log("Done!\n")
log("Loading json...\n")
import json
log("Done!\n")
log("Loading usercontrol.json...\n")
userfp=open("usercontrol.json","r+")
usercontrol_json=json.load(userfp)
userfp.seek(0)
print(usercontrol_json)
log("Done!\n")
room1=libadventure.Room("Spawn","You are in a plain nondescript room with a single bare lightbulb hanging from the ceiling. A dark and forbidding hallway leads west out of the room.",west="Dark Hallway")
room2=libadventure.Room("Dark Hallway","You are in a dark hallway that leads east-to-west. It opens on a lit door to the east and continues into darkness on the west.",east="Spawn",west="Telegate")
room3=libadventure.Room("Telegate","A white haze surrounds you, and then clears. You are in a 3-metre-by-3-metre white box with no doors or windows. You feel confused.")
world=libadventure.World(room1)
world.add_room(room3)
world.add_room(room2)
class GameProtocol(basic.LineReceiver):
	def __init__(self, factory):
		self.factory = factory
		self.state=""
	def connectionMade(self):
		self.factory.clients.add(self)
		self.state="MENU"
		self.sendLine("""
Welcome to the incredible PyMuddy!\r
1) If you have been here before, log in!\r
2) Otherwise, register an account!\r
Enter your choice > \r
		""".encode('utf8'))
		self.peer=self.transport.getPeer()
		log("Connection recieved from %s\n" % str(self.transport.getPeer()))
		log("Sent menu to %s\n" % str(self.transport.getPeer()))
	def connectionLost(self, reason):
		try:
			world.remove_player(self.username)
		except:
			log('Warning - error removing disconnected player!\n')
		log("Connection lost from %s\n" % str(self.peer))
		for c in self.factory.clients:
			if c!=self:
				c.sendLine(b'%s has left the game\r' % self.username.encode('utf8'))
		try:
			del self.player
		except:
			pass
		self.factory.clients.remove(self)
	def saytoeveryone(self,text):
		for c in self.factory.clients:
				if c!=self:
					c.sendLine(text.encode('utf8'))
	def lineReceived(self, line):
		log("Recieved line \n%s\n from client %s" % (line.decode('utf8'),str(self.transport.getPeer())))
		if self.state=="MENU":
			if line.decode('utf8')=="1":
				self.sendLine("Username > ")
				self.state="USERLOGIN1"
				return
			if line.decode('utf8')=="2":
				self.sendLine("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
				self.sendLine("Please enter a username > ".encode('utf8'))
				return
		if self.state=="PLAYING":
			if line.decode('utf8')[0:3]=="say":
				for c in self.factory.clients:
					if c!=self:
						c.sendLine(("%s>%s" % (self.username,line.decode('utf8')[3:])).encode('utf8'))
			else:
				self.sendLine(world.process_command(line.decode('utf8'),self.username,self.factory,self.username).encode('utf8'))
		if self.state=="USERLOGIN1":
			usercontrol_json=json.load(userfp)
			userfp.seek(0)
			data=usercontrol_json[u'logins']
			for i,x in enumerate(data):
				if x[u'username']==unicode(line.decode('utf8')):
					self.username=x[u'username'.encode('utf8')]
					self.password_correct=x[u'password']
					log(self.password_correct+"\n")
					self.i=i
					self.username=line.decode('utf8')
					self.sendLine(b'Password > ')
					self.state="USERLOGIN2"
					return
			self.sendLine("Bad username")
			self.state="MENU"
			self.sendLine("""
Welcome to the incredible PyMuddy!\r
1) If you have been here before, log in!\r
2) Otherwise, register an account!\r
Enter your choice >\r
		""".encode('utf8'))
		if self.state=="USERLOGIN2":
			usercontrol_json=json.load(userfp)
			userfp.seek(0)
			data=usercontrol_json[u'logins']
			if line.decode('utf8')==self.password_correct:
				self.sendLine(b"Login sucessful. Please press enter to continue.\r")
				self.state="PLAYING"
				self.sendLine(b'Welcome, %s\r!' % self.username.encode('utf8'))
				for c in self.factory.clients:
					if c!=self:
						c.sendLine(b'%s has joined the game\r!' % self.username.encode('utf8'))
				log("Client at %s gave username %s, logged in\n" % (self.peer,self.username))
				new_player=libadventure.Player(self.username)
				new_player.thing=self
				self.player=new_player
				world.add_player(new_player)
				self.sendLine(world.process_command('look',self.username,self.factory).encode('utf8'))
				self.state="PLAYING"
				return
			else:
				self.sendLine(b"Bad password\r")
				self.state="MENU"
				self.sendLine(b'''
Welcome to the incredible PyMuddy!\r
1) If you have been here before, log in!\r
2) Otherwise, register an account!\r
Enter your choice > \r
				''')

	    #for c in self.factory.clients:
	      #  c.sendLine("<{}> {}".format(self.transport.getHost(), world.commandProcessor.process(line,self.transport.getHost())))

class GameFactory(protocol.Factory):
	def __init__(self):
		self.clients = set()

	def buildProtocol(self, addr):
		return GameProtocol(self)

endpoints.serverFromString(reactor, "tcp:1234").listen(GameFactory())
reactor.run()