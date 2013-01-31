
import packetutils as utils


POS_TYPE 	= 0
POS_SUBTYPE = 1
POS_SEQ_NR 	= 2
POS_DATA 	= 10

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


class Header:

	def __init__(self, maintype, subtype, number):
		self.maintype = maintype
		self.subtype = subtype
		self.number = number
	
	def incremented(self):
		return Header(self.maintype, self.subtype, self.number + 1)
		

class Packet:
	'''
	HEADER		[ TYPE (8 bit) | SUBTYPE (8 bit) |	SEQ_NUMBER (64 bit)	]
	'''
	

	def __init__(self, header=None, bytedata=None):
		if header and bytedata:
			raise PacketError("cannot specify both header and bytedata")
	
		self.padding = 0
		self.data = {}													# { type : [(value1, len, datatype), (value2, len, datatype), ...] }
		
		if header:
			self.maintype = header.maintype
			self.subtype = header.subtype
			self.number = header.number
		
		elif bytedata:
			self.maintype = utils.byte_from_raw(bytedata, POS_TYPE)
			self.subtype = utils.byte_from_raw(bytedata, POS_SUBTYPE)
			self.number = utils.long_from_raw(bytedata, POS_SEQ_NR)
			offset = POS_DATA
			while True:
				
				try:
					off, tlv = utils.tlv_from_raw(bytedata, offset)
				except ValueError:
					break
					
				offset = offset + off
							
				if not tlv.spectype in self.data:
					self.data[tlv.spectype] = []
					
				self.data[tlv.spectype].append(tlv)
			
		
	def __len__(self):
		length = HEADER_LENGTH
		for value in self.data.itervalues():
			length = 2 + value[1]
		return length
		
	def __getitem__(self, key):
		return self.data[key]
	
	def __setitem__(self, key, value):
		if not key in self.data:
			self.data[key] = []
		self.data[key].append(value)
	
	def __iter__(self):
		return self.iterkeys()
	
	def keys(self):
		return self.iterkeys()
	
	def iterkeys(self):
		return self.data.iterkeys()
		
	def items(self):
		return self.iteritems()
		
	def iteritems(self):
		return self.data.iteritems()
		
	def values(self):
		return self.data.values()
		
	def itervalues(self):
		return self.data.itervalues()
	
	def __repr__(self):
		string = "[main:" + str(self.maintype) + ", sub:" + str(self.subtype) + ", number:" + str(self.number) + ", "
		for value in self.data:
			string = string + str(value) + ":" + str(self.data[value]) + ", "
			
		if self.padding > 0:
			string = string + "padding:" + str(self.padding)
			
		string = string + "]"
		return string

	def put_byte(self, specific_type, value):
		if not specific_type in self.data:
			self.data[specific_type] = []
		self.data[specific_type].append(utils.TLV(utils.DATATYPE_BYTE, specific_type, utils.BYTE_LENGTH_BYTE, value))
		
	def put_char(self, specific_type, value):
		if not specific_type in self.data:
			self.data[specific_type] = []
		self.data[specific_type].append(utils.TLV(utils.DATATYPE_CHAR, specific_type, utils.BYTE_LENGTH_CHAR, value))
		
	def put_int(self, specific_type, value):
		if not specific_type in self.data:
			self.data[specific_type] = []
		self.data[specific_type].append(utils.TLV(utils.DATATYPE_INT, specific_type, utils.BYTE_LENGTH_INT, value))
		
	def put_long(self, specific_type, value):
		if not specific_type in self.data:
			self.data[specific_type] = []
		self.data[specific_type].append(utils.TLV(utils.DATATYPE_LONG, specific_type, utils.BYTE_LENGTH_LONG, value))
		
	def put_string(self, specific_type, value, length):
		if not specific_type in self.data:
			self.data[specific_type] = []
		self.data[specific_type].append(utils.TLV(utils.DATATYPE_STRING, specific_type, length, value))
		
	def put_bytestring(self, specific_type, value, length):
		if not specific_type in self.data:
			self.data[specific_type] = []
		self.data[specific_type].append(utils.TLV(utils.DATATYPE_BYTESTRING, specific_type, length, value))

	def pad(self, padding):
		self.padding = padding
		
	def increment(self):
		self.number = self.number + 1

	def to_byte_string(self):
		ret = utils.byte_to_raw(self.maintype)
		ret = ret + utils.byte_to_raw(self.subtype)
		ret = ret + utils.long_to_raw(self.number)
		for spectype in self.data:
			for tup in self.data[spectype]:
				ret = ret + tup.to_byte_string()
				
		if self.padding > 0 and len(ret) < self.padding:
			ret = ret + (utils.byte_to_raw(0) * (self.padding - len(ret)))
			
		return ret

			
class PacketError(Exception):
	
	def __init__(self, msg):
		self.msg = msg
		
	def __str__(self):
		return self.msg
		
		
		
		
		
		
		
