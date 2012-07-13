import socket
import protocol

class VersionInfo:
	VERSION		=	0.1
	COMPATIBLE_WITH	=	0.1

ADDR 		=	"orion.uberspace.de"
PORT 		= 	20000

TYPE		=	protocol.Type.HOST


def setup_socket(address, port):
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.connect((address, port))
	return sock


if __name__ == "__main__":
	
	sock = setup_socket(ADDR, PORT)
	print "socket set up"

	sock.send("%s\n%s" % (VersionInfo.VERSION, TYPE))
	

	re = sock.recv(1024)
	print "received info"
	print re	

	while True:
		pass

