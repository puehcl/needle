import socket


ADDR 		=	"127.0.0.1"
PORT 		= 	20000



def setup_socket(address, port):
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.connect((address, port))
	return sock


if __name__ == "__main__":
	
	sock = setup_socket(ADDR, PORT)
	print "socket set up"
	sock.close()
	print "socket closed"
