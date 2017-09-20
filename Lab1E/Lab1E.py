import asyncio
from asyncio import Protocol
import playground 
#import Lab1DSubmissionUpdated
#from Lab1DSubmissionUpdated import ClientProtocol, ServerProtocol
from playground.network.packet import PacketType
from playground.network.common import StackingProtocol, StackingTransport, StackingProtocolFactory
from playground.network.packet.fieldtypes import UINT32, STRING, BUFFER, BOOL, ListFieldType
import os, sys
loop = asyncio.get_event_loop()
loop.set_debug(enabled=True)
import logging
logging.getLogger().setLevel(logging.NOTSET) # this loggs everything going on
logging.getLogger().addHandler(logging.StreamHandler())
# logs to stderr (find out what this is)

			
class LowerStackingProtocol(StackingProtocol):
	def __init__(self):
		self.transport = None
		super().__init__
			
	def connection_made(self,transport):
		self.transport = transport
		self.higherProtocol().connection_made(self.transport)
	
		
	def data_Received(self,data):
		self.higherProtocol().data_Received(data)
						
	def connection_lost(self):
		self.transport = None
		
class EchoControl:
	def buildProtocol(self):
		return ClientProtocol()
	
class HigherStackingProtocol(StackingProtocol):
	def __init__(self):
		self.transport = None
		super().__init__
		
	def connection_made(self,transport):
		self.transport = transport
		self.higherProtocol().connection_made(self.transport)
				
	def data_Received(self,data):
		self.higherProtocol().data_Received(data)
							
	def connection_lost(self):
		self.transport = None
		
class Username(PacketType): 
	
		DEFINITION_IDENTIFIER = "network.Username"
		DEFINITION_VERSION = "2.0"
	
		FIELDS = [
			("title", STRING),
			("data", BUFFER)
			]	
				
class PasswordRequest(PacketType): 

	DEFINITION_IDENTIFIER = "network.PasswordRequest"
	DEFINITION_VERSION = "2.0"

	FIELDS = [
		("Request", STRING),
		("data", BUFFER)
		]	


class UserPassword(PacketType):

	DEFINITION_IDENTIFIER = "network.UserPassword"
	DEFINITION_VERSION = "2.0"

	FIELDS = [
		("data", BUFFER)
		]

class ClientProtocol(asyncio.Protocol):
	def __init__(self):
		self.transport = None
		
	def connection_made(self, transport):
		self.transport = transport
		print ("Connection Made")
		outgoingPacket = Username()
		outgoingPacket.title="This is my user name"
		outgoingPacket.data = (b"My user name is Sean")
		self.transport.write(outgoingPacket.__serialize__())
		
		self._deserializer = PacketType.Deserializer()
		
	def data_Received(self, data):
		self.deserializer.update(data)
		
		for pkt in self.deserializer.nextPackets():
			if isinstance(pkt, PasswordRequest):
				print ("Password Requested")
		outgoingPacket = UserPassword()
		outgoingPacket.title = "This is my Password"
		outgoingPacket.data = (b"Password")
		self.transport.write(outgoingPacket.__serialize__())
					
	def connection_lost(self, exc):
		self.transport = None
		print ("Connection Lost")
	
class ServerProtocol(asyncio.Protocol):
	def __init__(self):
		self.transport = None
		
	def connection_made(self, transport):
		self.transport = transport
		self._deserializer = PacketType.Deserializer()
		
	def data_Received(self, data):
		self.deserializer.update(data)
		for pkt in self.deserializer.nextPackets():
			if isinstance(pkt, Username):
				print ("Username Received")
			elif isinstance(pkt, UserPassword):
				print ("Password Received")
		outgoingPacket = PasswordRequest()
		outgoingPacket.title = "What is the Password?"
		outgoingPacket.data = (b"What is your password?")
		self.transport.write(outgoingPacket.serialize())
		
	def connection_lost(self, exc):
		self.transport = None
		
def basicUnitTest():
	mode = sys.argv[1]# this takes Command line arguments in python.0 = python, 1 = server, 2 = client. 
	#in this scenario, so CL command "python3 Lab1E.py client" runs the client version of this code.  server runs the other.
	print("\n",mode)
	
	

#Client  needs to have below code in both client and server, creating a passthrough connection for the layers to work
	if mode == "client":
		f = StackingProtocolFactory(lambda: HigherStackingProtocol(), lambda: LowerStackingProtocol())
		ptConnector = playground.Connector(protocolStack=f)
		playground.setConnector("passthrough", ptConnector)
		loop = asyncio.get_event_loop()
		conn = EchoControl()
		coro = playground.getConnector("passthrough").create_playground_connection(conn.buildProtocol, "20174.1.1.1", 101)
		client = loop.run_until_complete(coro)
		print("Echo Client Connected.")
		loop.run_forever()
		loop.close()


#Server
	if mode == "server":
		f = StackingProtocolFactory(lambda: HigherStackingProtocol(), lambda: LowerStackingProtocol())
		ptConnector = playground.Connector(protocolStack=f)
		playground.setConnector("passthrough", ptConnector)
		loop = asyncio.get_event_loop()
		coro = playground.getConnector("passthrough").create_playground_server(lambda: ServerProtocol(), 101)
		server = loop.run_until_complete(coro)
		print("Echo Server Started ")
		loop.run_forever()
		loop.close()

if __name__=="__main__":
	basicUnitTest()	
