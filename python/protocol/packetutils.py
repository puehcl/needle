
import struct

DATATYPE_BYTE 		= 1
DATATYPE_CHAR 		= 2
DATATYPE_INT  		= 3
DATATYPE_LONG 		= 4
DATATYPE_STRING 	= 5
DATATYPE_BYTE_SEQ 	= 6
DATATYPE_BYTESTRING = 7

BYTE_LENGTH_BYTE = 1
BYTE_LENGTH_CHAR = 2
BYTE_LENGTH_INT  = 4
BYTE_LENGTH_LONG = 8

TLV_DATATYPE_POS = 0
TLV_SPECTYPE_POS = 1
TLV_LENGTH_POS	 = 2
TLV_DATA_POS	 = 6


class TLV:
	
	def __init__(self, datatype, spectype, length, value):
		self.datatype = datatype
		self.spectype = spectype
		self.length = length
		self.value = value
		
	def __eq__(self, value):
		return self.value == value
		
	def __len__(self):
		return TLV_DATA_POS + self.length
		
	def __repr__(self):
		return "(" + str(self.datatype) + ", " + str(self.spectype) + ", " + str(self.length) + ", " + str(self.value) + ")"	
	
	def to_byte_string(self):
		dt = byte_to_raw(self.datatype)
		st = byte_to_raw(self.spectype)
		le = int_to_raw(self.length)
		if self.datatype == DATATYPE_BYTE:				
			val = byte_to_raw(self.value)
		elif self.datatype == DATATYPE_CHAR:
			val = char_to_raw(self.value)
		elif self.datatype == DATATYPE_INT:
			val = int_to_raw(self.value)
		elif self.datatype == DATATYPE_LONG:
			val = long_to_raw(self.value)
		elif self.datatype == DATATYPE_STRING:	
			val = string_to_raw(self.value, self.length)
		elif self.datatype == DATATYPE_BYTE_SEQ:
			val = b""
			for i in range(self.length):
				val = val + byte_to_raw(self.value[i])	
		else:
			val = self.value
		return dt + st + le + val
		
		
def to_raw_bytes(byte_format, value):
	return struct.pack(byte_format, value)

def from_raw_bytes(byte_format, data, offset):
	size = struct.calcsize(byte_format)
		
	if (offset + size) > len(data):
		raise ValueError("data too short, to get datatype " + byte_format + " a len(data) of at least " + str(size) + " is needed.")
	
	return struct.unpack(byte_format, data[offset:(offset + size)])[0]


	
def byte_to_raw(byte_value):
	return to_raw_bytes("!b", byte_value)
		
def byte_from_raw(data, offset):
	return from_raw_bytes("!b", data, offset)
	
def char_to_raw(char_value):
	return to_raw_bytes("!h", char_value)
		
def char_from_raw(data, offset):
	return from_raw_bytes("!h", data, offset)
	
def int_to_raw(int_value):
	return to_raw_bytes("!i", int_value)
		
def int_from_raw(data, offset):
	return from_raw_bytes("!i", data, offset)
	
def long_to_raw(long_value):
	return to_raw_bytes("!q", long_value)
		
def long_from_raw(data, offset):
	return from_raw_bytes("!q", data, offset)
	
def string_to_raw(data, padding_length=-1):
	padding = b""
	if padding_length != -1:
		if len(data)*BYTE_LENGTH_CHAR > padding_length:
			raise ValueError("padding_length must be greater or equal to 2 * len(text)")
		else:
			padding = byte_to_raw(0) * (padding_length - len(data)*BYTE_LENGTH_CHAR)

	ret = b""
	for ch in data:
		ret = ret + char_to_raw(ord(ch))
	ret = ret + padding
	
	return ret

		
def string_from_raw(data, length, offset=0):			# length in bytes (1 char = 2 bytes)

	if (offset + length) > len(data):
		raise ValueError("data too short, given length: " + str(length) + ", data length: " + str(len(data)))
		
	text = ""
	for i in range(length):
		char = char_from_raw(data, offset)
		if char == 0:
			break
		text = text + chr(char)
		offset = offset + BYTE_LENGTH_CHAR
		
	return text
	
	
def tlv_from_raw(data, offset):
	if (offset + 1 + 1 + 2 + 1) > len(data):
		raise ValueError("data too short, at least 5 bytes are needed to read a tlv encoded value, only " + str((len(data) - offset)) + " bytes were available")
		
	datatype = byte_from_raw(data, offset + TLV_DATATYPE_POS)
	specific_type = byte_from_raw(data, offset + TLV_SPECTYPE_POS)
	length = int_from_raw(data, offset + TLV_LENGTH_POS)
	
	offset = offset + TLV_DATA_POS
	if datatype == DATATYPE_BYTE:				
		le = 1
		value = byte_from_raw(data, offset)
	elif datatype == DATATYPE_CHAR:
		le = 2
		value = char_from_raw(data, offset)
	elif datatype == DATATYPE_INT:
		le = 4
		value = int_from_raw(data, offset)
	elif datatype == DATATYPE_LONG:
		le = 8
		value = long_from_raw(data, offset)
	elif datatype == DATATYPE_STRING:
		le = length
		value = string_from_raw(data, length, offset)
	elif datatype == DATATYPE_BYTE_SEQ:
		le = length
		value = []
		for i in range(length):
			value.append(byte_from_raw(data, offset))
			offset = offset + BYTE_LENGTH_BYTE
	else:			
		le = length								
		value = data[offset:(offset + length)]
		
	if length != le:
			raise ValueError("datatype and length don't correspond: datatype=" + str(datatype) + ", length=" + str(length))

	return (TLV_DATA_POS + length), TLV(datatype, specific_type, length, value)			# new offset, spectype, tlv tupel
	
	
	
	
	
	
	
	
	
	
	
