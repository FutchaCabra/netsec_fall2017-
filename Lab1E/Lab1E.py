import asyncio
from asyncio import Protocol
import playground 
from playground.network.packet import PacketType
from playground.network.common import StackingProtocol, StackingTransport, StackingProtocolFactory
from playground.network.packet.fieldtypes import UINT32, STRING, BUFFER, BOOL, ListFieldType
import os, sys
import logging 
log = logging.getLogger(__name__)
 
			
class LowerStackingProtocol(playground.StackingProtocol):
	def __init__(self):
		self.transport = None
		log.debug("Lower Stacking Protocol Initiated")
		
	def connection_made(higher_transport):
		self.higherProtocol().connection_made()
		log.debug("Lower Connection Made")
		
	def data_Received(higher_transport):
		self.higherProtocol().data_Received(data)
		#self.transport.write(outgoingPacket.serialize())
		log.debug("data received from higher")
					
	def connection_lost(higher_transport):
		self.higherProtocol().connection_lost()
		log.debug("Connection Lost from higher")
		

class HigherStackingProtocol(playground.StackingProtocol):
	def __init__(self):
		self.transport = None
		
	def connection_made(lower_transport):
		self.lowerProtocol().connection_made()
		#self.transport.write(outgoingPacket.serialize())
		#self._deserializer = PacketType.Deserializer()
		log.debug("Higher Connection Made")
		
	def data_Received(lower_transport):
		self.lowerProtocol().data_Received(data)
		#self.deserializer.update(data)
		#self.transport.write(outgoingPacket.serialize())
		log.debug("data received from lower")
					
	def connection_lost(lower_transport):
		self.lowerProtocol()connection_lost()
		log.debug ("Higher Connection Lost")

f=StackingProtocolFactory(lambda:LowerStackingProtocol(),lambda:HigherStackingProtocol())

ptConnector=playground.Connector(protocolStack=f)
playground.setConnector("Passthrough",ptConnector)
		
	
