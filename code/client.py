from twisted.internet import protocol, reactor
from twisted.protocols import basic
import sys
from twisted.python import log

class TchainClientProtocol(basic.LineReceiver):
  def connectionMade(self):
    self.sendLine("Hello!")
    self.transport.loseConnection()

  def connectionLost(self, reason):
    reactor.stop()

def main():
  host = '127.0.0.1'
  port = 8123

  factory = protocol.ClientFactory()
  factory.protocol = TchainClientProtocol
  reactor.connectTCP(host, port, factory)
  reactor.run()

if __name__ == '__main__':
  main()