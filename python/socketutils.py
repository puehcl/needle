import socket

import packet


ALL_INTERFACES = "";		#all interfaces
RANDOM_PORT = 0;			#let os pick port

class UDPSocket:

	def __init__(self, addr=(ALL_INTERFACES, RANDOM_PORT)):
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.sock.bind(addr)
		
	def getsockname(self):
		return self.sock.getsockname()
		
	def recvfrom(self, bytes):
		data, addr = self.sock.recvfrom(bytes)
		return packet.getPacket(data), addr
		
	def sendto(self, packet, addr):
		return self.sock.sendto(packet.toByteArray(), addr)
		
	def settimeout(self, seconds):
		return self.sock.settimeout(seconds)
		
	def gettimeout(self):
		return self.sock.gettimeout()
		
	def close(self):
		return self.sock.close()
