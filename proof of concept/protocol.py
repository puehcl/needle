
MAX_HEADER_SIZE	=	2048


class Type:
	SERVER	=	"SERVER"
	HOST	=	"HOST"
	CLIENT	=	"CLIENT"




class ProtocolError(Exception):
	
	def __init__(self, code, msg):
		self.code = code
		self.msg = msg

	def __str__(self):
		return repr(self.msg)

	def error_code(self):
		return self.code

	def return_message(self):
		return "%s\n%s" % (self.code, self.msg)


class TypeNotAllowedError(ProtocolError):

	def __init__(self, wrong_type):
		ProtocolError.__init__(self, 10, "connection type %s not allowed" % wrong_type)
		
		

class Header:

	def __init__(self, version, conn_type):
		self.version = version
		if is_allowed(conn_type):
			self.connection_type = conn_type
		else:
			raise TypeNotAllowedError(conn_type)

	def __str__(self):
		return "%s\n%s" % (self.version, self.connection_type)


class ServerHeader(Header):
	
	def __init__(self, version, error=None, host_ip="0.0.0.0", host_port="-1"):
		Header.__init__(self, version, Type.SERVER)
		self.error = error
		self.host_ip = host_ip
		self.host_port = host_port

	def __str__(self):
		if not self.error:
			return Header.__str__(self) + "\n%s\n%s\n%s" % ("OK", self.host_ip, str(self.host_port))
		else:
			return Header.__str__(self) + "\nERROR\n" + self.error.return_message()


class HostHeader(Header):
	def __init__(self, version):
		Header.__init__(self, version, Type.HOST)


class ClientHeader(Header):
	def __init__(self, version):
		Header.__init__(self, version, Type.CLIENT)



def is_allowed(conn_type):
	if conn_type == Type.SERVER or conn_type == Type.HOST or conn_type == Type.CLIENT:
		return True
	return False


def get_header(conn):
	info = conn.recv(MAX_HEADER_SIZE)
	parts = info.split("\n")
		
	header = Header(parts[0], parts[1])
	
	return header

