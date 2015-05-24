#!C:\Python27
from twisted.internet import reactor, protocol, endpoints
from twisted.protocols import basic
import libadventure
world=libadventure.World()

class GameProtocol(basic.LineReceiver):
    def __init__(self, factory):
        self.factory = factory

    def connectionMade(self):
        self.factory.clients.add(self)

    def connectionLost(self, reason):
        self.factory.clients.remove(self)

    def lineReceived(self, line):
        for c in self.factory.clients:
            c.sendLine("<{}> {}".format(self.transport.getHost(), line))

class GameFactory(protocol.Factory):
    def __init__(self):
        self.clients = set()

    def buildProtocol(self, addr):
        return GameProtocol(self)

endpoints.serverFromString(reactor, "tcp:1234").listen(GameFactory())
reactor.run()