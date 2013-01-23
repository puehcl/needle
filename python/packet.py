import re

import utils


POS_TYPE 	= (0, 1)
POS_SUBTYPE = (1, 2)
POS_SEQ_NR 	= (2, 10)

PACKET_SIZE		= 512
HEADER_LENGTH 	= 10
PAYLOAD_SIZE	= PACKET_SIZE - HEADER_LENGTH

TYPE_CONTROL	= 1
TYPE_DATA		= 2

SUBTYPE_HOST_SERVER_REGISTER	= 1		# registration as host of specific service at server
SUBTYPE_HOST_SERVER_RDY			= 4		# socket created and ready to receive client addr

SUBTYPE_CLIENT_SERVER_REQ_HOST 	= 2		# client request host address for specific service

SUBTYPE_SERVER_HOST_OPEN		= 3		# open new socket and contact server through that port
SUBTYPE_SERVER_AGENT_CONNECT 	= 5		# server sends address of host to client and addr of client to host
	
SUBTYPE_AGENT_AGENT_ACK			= 6		# ack packet
SUBTYPE_AGENT_AGENT_NACK		= 7		# noack packet
SUBTYPE_AGENT_AGENT_ERROR		= 8
SUBTYPE_AGENT_AGENT_PROBING		= 9		# client and host try to reach one another
SUBTYPE_AGENT_AGENT_SUCCESS		= 10	# agent has successfully received other agents packet

def getPacket(byteString):
	print repr(byteString)
	maintype = utils.getByte(byteString, POS_TYPE)
	subtype = utils.getByte(byteString, POS_SUBTYPE)
	number = utils.getLong(byteString, POS_SEQ_NR)
	return Packet(maintype, subtype, number, byteString[HEADER_LENGTH:])

'''
	GLOBAL
'''
def getAckPacket(number, acknumber):
	'''
	PAYLOAD		[ ACKNUMBER (64 bit) ]
	'''
	payload = utils.putLong(b"", acknumber)
	return Packet(TYPE_CONTROL, SUBTYPE_AGENT_AGENT_ACK, number, payload)

def getAckData(pack):
	return utils.getLong(pack.payload)
	
	
def getNackPacket(number, nacknumber):
	'''
	PAYLOAD		[ ACKNUMBER (64 bit) ]
	'''
	payload = utils.putLong(b"", nacknumber)
	return Packet(TYPE_CONTROL, SUBTYPE_AGENT_AGENT_NACK, number, payload)

def getNackData(pack):
	return utils.getLong(pack.payload)
	
'''
	GLOBAL END
'''

'''
	FROM SERVER
'''
def getServerHostOpenPacket(number, reference):
	'''
	PAYLOAD		[ REFERENCE_NR (32 bit) ]
	'''
	payload = utils.putInteger(b"", reference)
	return Packet(TYPE_CONTROL, SUBTYPE_SERVER_HOST_OPEN, number, payload)

def getServerHostOpenData(pack):
	return utils.getInteger(pack.payload)
	
	
def get_server_agent_connect_packet(number, agent):
	payload = b""

	payload = utils.putText(payload, agent[0], 64)		# name
	addrbytes = re.split("[.]", agent[1])		# ip
	for b in addrbytes:					
		payload = utils.putByte(payload, int(b))
	payload = utils.putInteger(payload, int(agent[2]))		# port
	
	return Packet(TYPE_CONTROL, SUBTYPE_SERVER_AGENT_CONNECT, number, payload)
	
def get_server_agent_connect_data(pack):

	hostname = utils.getText(pack.payload, 64)
	ip = ""
	for i in range(3):
		ip = ip + str(utils.getByte(pack.payload[64 + i:])) + "."
	ip = ip + str(utils.getByte(pack.payload[64 + 3:]))
	port = utils.getInteger(pack.payload[64 + 4:])
		
	return hostname, ip, port
	
'''
	FROM SERVER END
'''

'''
	HOST TO SERVER
'''
def getHostServerRegisterPacket(number, hostname, service):
	'''
	PAYLOAD		[ HOSTNAME (64 Byte) | SERVICENAME (64 Byte) ]
	'''	
	if len(hostname) > 32:
		raise ValueError("hostname must be 32 characters or less")
	if len(service) > 32:
		raise ValueError("service must be 32 characters or less")
	hname = utils.putText(b"", hostname, 64)
	serv = utils.putText(b"", service, 64)
	payload = hname + serv
	return Packet(TYPE_CONTROL, SUBTYPE_HOST_SERVER_REGISTER, number, payload)

def getHostServerRegisterData(pack):
	return utils.getText(pack.payload, 64), utils.getText(pack.payload[64:], 64)

def getHostServerReadyPacket(number, reference):
	'''
	PAYLOAD		[ REFERENCE_NR (32 Bit) ]
	'''
	payload = utils.putInteger(b"", reference)
	return Packet(TYPE_CONTROL, SUBTYPE_HOST_SERVER_RDY, number, payload)
	
def getHostServerReadyData(pack):
	return utils.getInteger(pack.payload)

'''
	HOST TO SERVER END
'''

'''
	CLIENT TO SERVER
'''
def get_client_server_req_host_packet(number, clientname, hostname, service):
	'''
	PAYLOAD		[ CLIENTNAME (64 byte) | SERVICENAME (64 byte) | HOSTNAME (64 byte)]
	'''
	if len(clientname) > 32:
		raise ValueError("hostname must be 32 characters or less")
	if len(hostname) > 32:
		raise ValueError("hostname must be 32 characters or less")
	if len(service) > 32:
		raise ValueError("service must be 32 characters or less")
		
	cname = utils.putText(b"", clientname, 64)
	hname = utils.putText(b"", hostname, 64)
	serv = utils.putText(b"", service, 64)

	payload = cname + hname + serv
	return Packet(TYPE_CONTROL, SUBTYPE_CLIENT_SERVER_REQ_HOST, number, payload)
	
def get_client_server_req_host_data(pack):
	return 	utils.getText(pack.payload, 64), utils.getText(pack.payload[64:], 64), utils.getText(pack.payload[128:], 64)
	
'''
	CLIENT TO SERVER END
'''

class Packet:
	'''
	HEADER		[ TYPE (8 bit) | SUBTYPE (8 bit) |	SEQ_NUMBER (64 bit)	]
	'''
	

	def __init__(self, maintype, subtype, number, payload):
		self.maintype = maintype
		self.subtype = subtype
		self.number = number
		self.payload = payload
		
	def __repr__(self):
		return str(self.maintype) + " " + str(self.subtype) + " " + str(self.number)

	def toByteArray(self):
		ret = b""
		ret = utils.putByte(ret, self.maintype)
		ret = utils.putByte(ret, self.subtype)
		ret = utils.putLong(ret, self.number)
		return ret + self.payload

			
class PacketError(Exception):
	
	def __init__(self, msg):
		self.msg = msg
		
	def __str__(self):
		return self.msg
