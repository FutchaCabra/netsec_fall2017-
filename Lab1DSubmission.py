import asyncio
import playground 
from playground.network.packet import PacketType
from playground.network.packet.fieldtypes import UINT32, STRING, BUFFER, BOOL, ListFieldType

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
		self.transport.write(outgoingPacket.serialize())
		
		#if isinstance(pkt,Access):
		#	print ("Requesting Access")
		#elif isinstance(pkt, Username):
		#	print ("Username Sent")
		#elif isinstance(pkt, UserPassword):
		#		print ("Password Sent")
		self._deserializer = PacketType.Deserializer()
		
	def data_Received(self, data):
		self.deserializer.update(data)
		
		for pkt in self.deserializer.nextPackets():
			if isinstance(pkt, PasswordRequest):
				print ("Password Requested")
		outgoingPacket = UserPassword()
		outgoingPacket.title = "This is my Password"
		outgoingPacket.data = (b"Password")
		self.transport.write(outgoingPacket.serialize())
					
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
	import asyncio
	from playground.asyncio_lib.testing import TestLoopEx
	from playground.network.testing import MockTransportToStorageStream
	from playground.network.testing import MockTransportToProtocol
	#class EchoServerProtocol(asyncio.Protocol):
		#def connection_made(self, transport):
			#print ("Echo Server Connected to Client")
			
	#class EchoClientProtocol(asyncio.Protocol):
		#def __init__(self, message, loop):
			#3print ("Echo Client Connected to Server")
	
		
	#asyncio.set_event_loop(TestLoopEx())
	#clientProtocol = ClientProtocol()
	#serverProtocol = ServerProtocol()
	#transportToServer = MockTransportToProtocol(myProtocol=ClientProtocol)
	#transportToClient = MockTransportToProtocol(myProtocol=ServerProtocol)
	#transportToServer.setRemoteTransport(transportToClient)
	#transportToClient.setRemoteTransport(transportToServer)
	#ClientProtocol.connection_made(transportToServer)
	#ServerProtocol.connection_made(transportToClient)
		
	loop = asyncio.get_event_loop()
	#loop.create_server(lambda:server(),port=8000)
	#- this is listening protocol in asyncio, creates server using asyncio
	x = playground.getConnector()create_playground_server(lambda:ServerProtocol(),port = 8000)
	#loop.create_connection (lambda: client(), host="127.0.0.1", port=8000) 
	# creates outbound connection in asyncio
	y = playground.getConnector().create_playground_connection (lambda:ClientProtocol(),20174.1.1.1,port = 8000)
	# look at coroutine from python pages. 18.5.4.3.1. TCP echo client protocol for lab1D
	#if loop.is_running: 
		#print ("loop is running")
	
	#assert client.status=1 # checks if client status is set to 1
	loop.run_until_complete(x)
		#except KeyboardInterrupt:
			#pass
	
		
if __name__=="__main__":
	basicUnitTest()
	#print ("Basic Unit Test Completed")
		
	
