import socket
import protocol


ADDR 		=	"127.0.0.1"
PORT 		= 	20000


VERSION		=	0.1
TYPE		=	protocol.HOST


def setup_socket(address, port):
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.connect((address, port))
	return sock


if __name__ == "__main__":
	
	sock = setup_socket(ADDR, PORT)

	sock.send("%s\n%s" % (VERSION,TYPE))
	print "socket set up"
	sock.close()
	print "socket closed"
