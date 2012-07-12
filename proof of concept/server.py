import sys
import socket
import threading
import protocol as p


LOCALHOST 	=	"127.0.0.1"
PORT 		= 	20000
BACKLOG 	= 	5


HOST_CONNECTED 	=	False
HOST		=	None



class WrongConnectionTypeError(Exception):

	def __init__(self, value):
		self.value = value

	def __str__(self):
		return repr(self.value)


class ClientConnection:
	"""represents a connection to a client"""

	def __init__(self, sock):
		self.sock = sock


	def handle(self):
		print "handle conn"

		header = p.get_header(self.sock) 
		
		if not host_connected():
			print "blub"
			if header.connection_type != p.HOST:
				return					# send error msg back
			else:
				set_host(self.sock)



def host_connected():
	return HOST_CONNECTED

def set_host(conn):
	HOST = conn
	HOST_CONNECTED = True
	print "host set to", repr(conn)



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
		cc = ClientConnection(conn)
		thread = threading.Thread(target=cc.handle)
		thread.start()




if __name__ == "__main__":
	
	sock = setup_serversocket(PORT)
	print "socket set up"
	listen(sock)
	sock.close()
	print "socket closed"
	