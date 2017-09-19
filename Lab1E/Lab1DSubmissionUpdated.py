import asyncio
from asyncio import Protocol
import playground 
from playground.network.packet import PacketType
from playground.network.packet.fieldtypes import UINT32, STRING, BUFFER, BOOL, ListFieldType
import os, sys

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
	mode = sys.argv[1]# this takes Command line arguments in python.0 = python, 1 = server, 2 = client. 
	#in this scenario, so CL command "python3 Lab1DSubmissionUpdated.py client" runs the client version of this code.  server runs the other.
	print("\n",mode)
	loop = asyncio.get_event_loop()
	if mode == "server" :
		coro = playground.getConnector("passthrough").create_playground_server
		#coro = playground.getConnector().create_playground_server(lambda:ServerProtocol(),'8000')
		# replaced coro for creating server with the getConnector, for 1E
		server = loop.run_until_complete(coro)
		loop.run_forever()
		#server.close()
		loop.close()
	
	if mode == "client" :
		x = playground.getConnector().create_playground_connection (lambda:ClientProtocol(),"20174.1.1.1", '8000')
		loop.run_until_complete(x)
		loop.run_forever()
		loop.close()
		
		#except KeyboardInterrupt:
			#pass
	
		
if __name__=="__main__":
	basicUnitTest()
	#print ("Basic Unit Test Completed")
		
	
