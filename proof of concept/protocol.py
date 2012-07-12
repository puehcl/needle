
MAX_HEADER_SIZE	=	2048

SERVER	=	"SERVER"
HOST	=	"HOST"
CLIENT	=	"CLIENT"




class ProtocolError(Exception):
	
	def __init__(self, value):
		self.value = value

	def __str__(self):
		return repr(self.value)

class Header:

	def __init__(self, version, conn_type):
		self.version = version
		if is_allowed(conn_type):
			self.connection_type = conn_type
		else:
			raise ProtocolError("connection type %s not allowed" % conn_type)

	def __str__(self):
		return "(%s, %s)" % (self.version, self.connection_type)


def is_allowed(conn_type):
	if conn_type == SERVER or conn_type == HOST or conn_type == CLIENT:
		return True
	return False


def get_header(conn):
	header = conn.recv(MAX_HEADER_SIZE)
	parts = header.split("\n")

	header = Header(parts[0], parts[1])
	
	return header

