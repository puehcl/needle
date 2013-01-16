import socket

ALL_INTERFACES = "";		#all interfaces
RANDOM_PORT = 0;			#let os pick port

class UDPSocket:

	def __init__(self, addr=(ALL_INTERFACES, RANDOM_PORT)):
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.sock.bind(addr)
		
	def getsockname(self):
		return self.sock.getsockname()
		
	def recvfrom(self, bytes):
		return self.sock.recvfrom(bytes)
		
	def sendto(self, data, addr):
		return self.sock.sendto(data, addr)
		
	def close(self):
		return self.sock.close()
		
