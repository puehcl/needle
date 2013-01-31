
import multiprocessing
import utils
import socket
import packet

class HostDataChannel(multiprocessing.Process):

	RECONNECT_RETRY_COUNT = 5		
	RECONNECT_RETRY_TIMEOUT = 30	#seconds

	def __init__(self, processname, reference, mediator_address, relay_address):
		multiprocessing.Process.__init__(self, name=processname)
		self.shutdown_ = False
		self.reference = reference
		self.mediator_address = mediator_address
		self.relay_address = relay_address
		self.udp_sock = None
		
	def run(self):
		print "channel", self.name, "active"
		try:
			self.udp_sock = utils.UDPSocket()
		except socket.error as se:
			print "an error has occured while creating the socket:", repr(se)
			return
		
		self.udp_sock.settimeout(HostDataChannel.RECONNECT_RETRY_TIMEOUT)
		
		tries = 0
		while True:
			
			if self.shutdown_:
				return
			
			if tries >= HostDataChannel.RECONNECT_RETRY_COUNT:
				print "maximum retries reached, connection to server lost, returning"
				return
			
			print "getting rdy packet"
			rdy = packet.getHostServerReadyPacket(0, self.reference)
			self.udp_sock.sendto(rdy, self.mediator_address)
			
			print "rdy packet sent to", self.mediator_address
			
			try:
				pack, addr = self.udp_sock.recvfrom(65535)
			except socket.timeout as to:
				tries = tries + 1
				continue
			except socket.error as se:
				print "an error has occured while listening for packets:", repr(se)
				
			print "received packet:", repr(pack)
			break
						
	def shutdown(self):
		self.shutdown_ = True
		if self.udp_sock:
			self.udp_sock.close()
