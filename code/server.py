'''
	https://twistedmatrix.com/documents/12.0.0/core/howto/servers.html
'''

from twisted.internet.protocol import Factory
from twisted.protocols import basic
from twisted.protocols.basic import LineReceiver
from twisted.internet import reactor
from datetime import datetime
from ecdsa import SigningKey, VerifyingKey
import TorCoin
import StoreHash
import sys
import os
import random
import hashlib
import base64


class Tchain(LineReceiver):

    '''
            Protocol for passing messages between nodes. Capable of handling multiple
            open connections. e.g. If server.pos=1, will have open connection with
            client_0 (node on the left) and client_2 (node on the right). Example:

                            server.pos = 1

                            # Chat with server, client_0
                            server: I am position 1. What's your position?
                            client_0: 0

                            # Chat with server, client_2
                            server: I am position 1. What's your position?
                            client_2: 2

                            # All messages from client_0 go to handler_REC_L ("from the left")
                            # All messages from client_2 go to handler_REC_R ("from the right")

            Tchain protocol is initialized by TchainFactory, which should provide the
            args as specified in the Tchain constructor.
    '''

    def __init__(self, pos, users):
        '''
                pos = integer position of the server
                users = dictionary of currently connected users (left and/or right)
        '''
        self.users = users  # List of connected peers (should be max left, right)
        self.pos = pos			# Integer representation of our position
        # String representation of sender, in {"0","1","2","3"}
        self.sender = None
        self.sender_pos = 0  # Integer representation of sender, in {0,1,2,3}
        # Current state of protocol ("GETSENDER" or else)
        self.state = "GETSENDER"

    def connectionMade(self):
        print 'hello!!!'
        self.sendLine("I am position %d. What's your position?" % self.pos)

    def connectionLost(self, reason):
        if self.users.has_key(self.sender):
            del self.users[self.sender]

    def lineReceived(self, line):
        print 'Received message: ' + line

        if self.state == "GETSENDER":
            self.handle_GETSENDER(line)
        else:
            print "Length of line:" + str(len(line))
            self.handle_REC(line)

    def sendMessage(self, target, sender):
        if target == 2:
            host = '127.0.0.1'
            port = 8122

        factory = protocol.ClientFactory()
        factory.protocol = TchainClientProtocol
        reactor.connectTCP(host, port, factory)
        # reactor.run()

    def handle_GETSENDER(self, sender):
        '''
                Handler for identification. Node on left or right sends its position
                as 'sender'.  e.g. In torcoin chain, if I am client (pos=0), A (pos=1)
                identifies as sender=1. We use this to determine if we received a
                message from the right or the left.
        '''

        try:
            self.sender_pos = int(sender)
            if self.sender_pos < 0 or self.sender_pos > 3:
                raise Exception
            if self.users.has_key(sender):
                raise Exception
        except Exception:
            self.sendLine("Invalid position specified. Must be in {0,1,2,3} and not\
										 already taken.")
            return

        self.sendLine("Welcome, %s!" % (sender,))
        self.sender = sender
        self.users[sender] = self
        self.state = "CHAT"

    def handle_REC(self, message):
        '''
                Determine if message received from left or right, and call the
                appropriate handler.
        '''

        handler = None

        if self.pos < self.sender_pos:
            handler = self.handle_REC_R

        elif self.pos > self.sender_pos:
            handler = self.handle_REC_L

        # Only other possibility is self.pos == sender_pos ... which makes no
        # sense
        if handler is None:
            raise Exception('Cannot receive from myself!')

        # Call the appropriate handler
        handler(message)

    def handle_REC_R(self, message):
        ''' Handler for messages received from right. '''

        print 'Received from right'

        # message_wrapped = "REC_R: <%s> %s" % (self.sender, message)
        # for sender, protocol in self.users.iteritems():
        # if protocol != self:
        # 	protocol.sendLine(message_wrapped)

        # TorCoin verifying code
        # TorCoin Verify packet structure:
        # TCVERIFY:hash_attempt_n:hash_value_n:hash_attempt_n-1:hash_value_n-1
        message_split = message.split(":")
        if message_split[0] == 'TCVERIFY':
            stored_hash_value = StoreHash.retrieveFromTable(
                "value", self.pos + 1)
            # print "SHV: " + stored_hash_value
            stored_hash_attempt = StoreHash.retrieveFromTable(
                "attempt", self.pos + 1)
            if TorCoin.tc_verify(self.pos, stored_hash_value, message_split[1:]):
                # figure out how to get to right relay directly
                for receiver, protocol in self.users.iteritems():
                    if str(receiver) == str(self.pos - 1):
                        protocol.sendLine('TCVERIFY:' + str(stored_hash_attempt) + ":" + str(
                            stored_hash_value) + ":" + ":".join(message_split[1:]))
            else:
                print 'ERROR'

    def handle_REC_L(self, message):
        ''' Handler for messages received from left. '''

        print 'Received from left'

        # message_wrapped = "REC_L: <%s> %s" % (self.sender, message)
        # for sender, protocol in self.users.iteritems():
        # if protocol != self:
        # 	protocol.sendLine(message_wrapped)

        # TorCoin sending code
        # Torcoin packet structure: TCATTEMPT:<HASH>
        message_split = message.split(":")
        # this is how to distinguish torcoin packet
        if message_split[0] == 'TCATTEMPT':
            hash_attempt = self.pos  # my hash attempt
            received_hash = message_split[1]
            hash_value = TorCoin.tc_generate(
                self.pos, hash_attempt, received_hash)
            # self.pos + 1 is a substitute for IP address
            StoreHash.storeInHashTable("value", self.pos + 1, hash_value)
            StoreHash.storeInHashTable("attempt", self.pos + 1, hash_attempt)
            if self.pos == 3:
                # figure out how to get to right relay directly
                for receiver, protocol in self.users.iteritems():
                    if str(receiver) == str(self.pos - 1):
                        protocol.sendLine(
                            'TCVERIFY:' + str(hash_attempt) + ":" + hash_value)
            else:
                # figure out how to get to right relay directly
                for receiver, protocol in self.users.iteritems():
                    # This guy is the relay to the right
                    if str(receiver) == str(self.pos + 1):
                        protocol.sendLine('TCATTEMPT:' + hash_value)

class TchainFactory(Factory):

	def __init__(self, pos):
		self.pos = pos
		self.users = {}
		# step 1 (explained in readme)
		folder = datetime.now().strftime('%Y%m%d%H%M%S')
		if not os.path.exists("operations/"+folder):
			os.makedirs("operations/"+folder)
		# step 2
		self.sk = SigningKey.generate()
		sk_pem = self.sk.to_pem()
		with open("operations/"+folder+"/"+str(self.pos)+"pvt.pem", "w") as text_file:
			text_file.write(sk_pem)
		self.vk = self.sk.get_verifying_key()
		vk_pem = self.vk.to_pem()
		with open("operations/"+folder+"/"+str(self.pos)+"pub.pem", "w") as text_file:
			text_file.write(vk_pem)
		# step 3
		# R = random.randrange(1,1000000000000) # R is defined in paper as temporary key
		self.R = self.pos # for testing
		self.Rprime = hashlib.md5(str(self.R)).hexdigest() # Rprime is hash of R
		# step 4
		with open("operations/"+str(self.pos)+".pem", "w") as text_file:
			text_file.write(vk_pem)

	def buildProtocol(self, addr):
		return Tchain(self.pos, self.users, self.sk, self.vk, self.R, self.Rprime)
>>>>>>> 61165c4f49cfb0ba058e1c1cc783364e058aee27

if __name__ == '__main__':
    reactor.listenTCP(8120 + int(sys.argv[1]), TchainFactory(int(sys.argv[1])))
    reactor.run()
