import sys
import socket
import thread
import protocol as p

class VersionInfo:
	VERSION		=	0.1
	COMPATIBLE_WITH	=	0.1


LOCALHOST 	=	"127.0.0.1"
PORT 		= 	20000
BACKLOG 	= 	5


class Host:
	connected 	=	False
	address		=	None



class ConnectionError(Exception):

	def __init__(self, code, msg):
		self.code = code
		self.msg = msg

	def __str__(self):
		return repr(self.msg)

	def error_code(self):
		return self.code

	def return_message(self):
		return str(self.code) + "\n" + self.msg


class HostNotYetConnectedError(ConnectionError):	
	def __init__(self):
		ConnectionError.__init__(self, 20, "host not yet connected, only connections of type HOST are allowed")


class HostAlreadyConnectedError(ConnectionError):	
	def __init__(self):
		ConnectionError.__init__(self, 21, "host already connected, only connections of type CLIENT are allowed")


class Connection:
	"""represents a connection to a client"""

	def __init__(self, sock, addr):
		self.sock = sock
		self.addr = addr


	def handle(self):

		try:
			header = p.get_header(self.sock) 
		except p.ProtocolError as pe:
			self.sock.send(pe.return_message())
			self.sock.close()
			return

		print Host.connected, "before check"
		if not Host.connected:
			print "host not connected"
			if header.connection_type != p.Type.HOST:
				print "rejecting connection from", self.addr, "reason: no host"
				self.sock.send(p.ServerHeader(VersionInfo.VERSION, error=HostNotYetConnectedError()).__str__())
				self.sock.close()
				return					
			else:
				print "registering host:", self.addr
				self.sock.send(p.ServerHeader(VersionInfo.VERSION, host_ip=self.addr[0], host_port=self.addr[1]).__str__())
				Host.address = self.addr
				Host.connected = True
				print Host.connected, "after setting host"

		else:
			if header.connection_type != p.Type.CLIENT:
				print "rejecting connection from", self.addr, "reason: no client"
				self.sock.send(p.ServerHeader(VersionInfo.VERSION, error=HostAlreadyConnectedError()).__str__())
				self.sock.close()
				return					
			else:
				print "sending host data to client"
				self.sock.send(p.ServerHeader(VersionInfo.VERSION, host_ip=Host.address[0], host_port=Host.address[1]).__str__())
				self.sock.close()




def setup_serversocket(port):
	"""sets up a serversocket on the specified port"""

	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.bind((LOCALHOST, port))
	sock.listen(BACKLOG)	
	return sock


def listen(sock):
	"""listens for clients on the given socket and starts a new thread to handle each connection"""

	while True:
		conn, addr = sock.accept()
		print "connection", conn, "at addr:", addr
		c = Connection(conn, addr)
		thread.start_new_thread(c.handle, ())
		#thread.start()




if __name__ == "__main__":
	
	sock = setup_serversocket(PORT)
	print "socket set up"
	listen(sock)
	sock.close()
	print "socket closed"
	
