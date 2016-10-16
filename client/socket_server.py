from autobahn.twisted.websocket import WebSocketServerFactory
from autobahn.twisted.websocket import WebSocketServerProtocol

from twisted.internet import reactor, protocol
from twisted.internet.defer import Deferred, inlineCallbacks, returnValue
from twisted.python import log
from txzmq import ZmqEndpoint, ZmqFactory, ZmqPullConnection

import json
import sys

class NotificationProtocol(WebSocketServerProtocol):

    def onOpen(self):
        self.factory.register(self)

    def onConnect(self, request):
        print("Client connecting: {}".format(request.peer))

    def connectionLost(self, reason):
        WebSocketServerProtocol.connectionLost(self, reason)
        self.factory.unregister(self)  

    def onMessage(self, payload, isBinary):
        ## echo back message verbatim
        #print(payload)
        
        message = payload.decode("utf-8")
        print(message)

class NotificationServerFactory(WebSocketServerFactory):
    
    def __init__(self,zpull,host='127.0.0.1',port=9000):
        WebSocketServerFactory.__init__(self,"ws://"+host+":"+str(port))
        self.clients = []
        self.subscriber = zpull
        self.subscriber.onPull = self.recv
                
    def register(self,c):
        self.clients.append(c)
    
    def unregister(self, c):
        self.clients.remove(c)

    def broadcast(self,msg):
        for c in self.clients:
            c.sendMessage(str(json.dumps(msg)).encode('utf8'))

    
    def recv(self,*args):
                
        message = json.loads(str(args[0][0].decode("utf-8")))
        print(message)
        self.broadcast(message)
        

if __name__ == '__main__':

    zf = ZmqFactory()
    endpoint = ZmqEndpoint("connect", "ipc:///tmp/sock")

    pull = ZmqPullConnection(zf, endpoint)

    def doPrint(*args):
        print("message received: %r" % (args, ))

    log.startLogging(sys.stdout)

    ws_factory = NotificationServerFactory(pull,host="localhost")
    ws_factory.protocol = NotificationProtocol

    reactor.listenTCP(9000, ws_factory)
    reactor.run()

