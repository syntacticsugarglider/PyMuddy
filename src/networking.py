#!C:\Python27
from twisted.internet import reactor, protocol, endpoints
from twisted.protocols import basic
import libadventure
room1=libadventure.Room("Spawn","You are in a plain nondescript room with a single bare lightbulb hanging from the ceiling. A dark and forbidding hallway leads west out of the room.",west="Dark Hallway")
room2=libadventure.Room("Dark Hallway","You are in a dark hallway that leads east-to-west. It opens on a lit door to the east and continues into darkness on the west.",east="Spawn")
world=libadventure.World(room1)
world.add_room(room2)
class GameProtocol(basic.LineReceiver):
    def __init__(self, factory):
        self.factory = factory
        self.state=""
    def connectionMade(self):
        self.factory.clients.add(self)
        self.state="USERNAME"
        self.sendLine(b'Enter a username > ')
        self.peer=self.transport.getPeer()
        print("Connection recieved from %s" % str(self.transport.getPeer()))
        print("Requesting username")
    def connectionLost(self, reason):
    	world.remove_player(self.username)
        print("Connection lost from %s" % str(self.peer))
        for c in self.factory.clients:
    		if c!=self:
    			c.sendLine(b'%s has left the game' % self.username.encode('utf8'))
        self.factory.clients.remove(self)

    def lineReceived(self, line):
    	if self.state=="PLAYING":
    		if line.decode('utf8')[0:3]=="say":
    			for c in self.factory.clients:
    				if c!=self:
    					c.sendLine(("%s>%s" % self.username,line.decode(utf8)[3:]).encode('utf8'))
    		else:
    			self.sendLine(world.process_command(line.decode('utf8'),self.username).encode('utf8'))
    	if self.state=="USERNAME":
    		self.username=line.decode('utf8')
    		self.sendLine(b'Welcome, %s!' % self.username.encode('utf8'))
    		for c in self.factory.clients:
    			if c!=self:
    				c.sendLine(b'%s has joined the game!' % self.username.encode('utf8'))
    		print("Client at %s gave username %s, logged in" % (self.peer,self.username))
    		world.add_player(libadventure.Player(self.username))
    		
    		self.sendLine(world.process_command('look',self.username).encode('utf8'))
    		self.state="PLAYING"
    	
        #for c in self.factory.clients:
          #  c.sendLine("<{}> {}".format(self.transport.getHost(), world.commandProcessor.process(line,self.transport.getHost())))

class GameFactory(protocol.Factory):
    def __init__(self):
        self.clients = set()

    def buildProtocol(self, addr):
        return GameProtocol(self)

endpoints.serverFromString(reactor, "tcp:1234").listen(GameFactory())
reactor.run()