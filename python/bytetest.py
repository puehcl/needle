import socket
import struct
import utils

if __name__ == "__main__":
	
	data = ""
	
	print "put int", data, "15"
	a = utils.putInteger(data, 15)
	print repr(a), "len:", len(a) 
	print "put int", repr(a), "127"
	b = utils.putInteger(a, 127)
	print repr(b), "len:", len(b) 
	
	print "get int", repr(b)
	print utils.getInteger(b)
	print "get int", repr(b), "(4, 8)"
	print utils.getInteger(b, (4,8))
	
	print "put byte", data, "-100"
	a = utils.putByte(data, -100)
	print repr(a), "len:", len(a) 
	print "put long", repr(a), "324324234324"
	b = utils.putLong(a, 324324234324)
	print repr(b), "len:", len(b) 
	
	print "get byte", repr(b)
	print utils.getByte(b)
	print "get long", repr(b), "(1, 9)"
	print utils.getLong(b, (1, 9))
	
	print "put long", repr(data), "324324234324"
	a = utils.putLong(data, 324324234324)
	print repr(a), "len:", len(a) 
	print "get long", repr(a)
	print utils.getLong(a)
	
	try:
		print "get long", repr(a), "(0, 9)"
		print utils.getLong(a, (0, 9))
	except ValueError as e:
		print e
