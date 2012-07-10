import socket
import threading


LOCALHOST 	=	"127.0.0.1"
PORT 		= 	20000
BACKLOG 	= 	5


HOST_CONNECTED 	=	False



class ClientConnection:
	"""represents a connection to a client"""

	def __init__(self, tcpconn):
		self.tcpconn = tcpconn


	def handle(self):
		print "handle conn"




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
		return




if __name__ == "__main__":
	
	sock = setup_serversocket(PORT)
	print "socket set up"
	listen(sock)
	sock.close()
	print "socket closed"
	
