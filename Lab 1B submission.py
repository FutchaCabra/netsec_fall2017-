from playground.network.packet import PacketType
from playground.network.packet.fieldtypes import UINT32, STRING, BUFFER, BOOL, ListFieldType
class Access(PacketType):
	
		DEFINITION_IDENTIFIER = "network.access"
		DEFINITION_VERSION = "2.0"
	
		FIELDS = [
			("name", STRING),
			("data", BUFFER)
			]
	
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



def basicUnitTest():
	packet1 = Access()
	packet1.name = "RequestUserName"
	packet1.data = (b"What is your name?")
	packet1Bytes = packet1.__serialize__()
	packet1a = Access.Deserialize(packet1Bytes)
	print (Access)
	print (packet1a)
	assert packet1 == packet1a
		
	packet2 = Username()
	packet2.title = "UserName"
	packet2.data = (b"Sean Futch")
	packet2Bytes = packet2.__serialize__()
	packet2a = Username.Deserialize(packet2Bytes)
	print (Username)
	print (packet2a)
	assert packet2 == packet2a
		
	packet3 = PasswordRequest()
	packet3.Request = "Password Request"
	packet3.data = (b"Please Enter Password.")
	packet3Bytes = packet3.__serialize__()
	packet3a = PasswordRequest.Deserialize(packet3Bytes)
	print (PasswordRequest)
	print (packet3a)
	assert packet3 == packet3a
		
	packet4 = UserPassword()
	packet4.data = (b"Password")
	packet4Bytes = packet4.__serialize__()
	packet4a = UserPassword.Deserialize(packet4Bytes)
	print (UserPassword)
	print (packet4a)
	assert packet4 == packet4a
		
if __name__=="__main__":
	basicUnitTest()
		
		
print ("Basic Unit Test Completed")
		
	
