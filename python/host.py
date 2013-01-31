
import time
import threading
import multiprocessing
import signal
import sys
import socket

import protocol.constants as const
import protocol.socketutils as utils
import protocol.packet as packet
import protocol.register as reg

seq_number = 1;
expected_ack_number = 1

reg_handler = None
active_processes = []

def shutdown_handler(signal, frame):
	for process in active_processes:
		process.shutdown()
		process.join()
		print "process", process.name, "shut down"
	if reg_handler:
		reg_handler.shutdown()
		reg_handler.join()
		print "exchange handler shut down"
	sys.exit(0)

class HostDataProvider(multiprocessing.Process):

	RECONNECT_RETRY_COUNT = 5		
	RECONNECT_RETRY_TIMEOUT = 30	#seconds

	def __init__(self, processname, reference, mediator_address, relay_address):
		multiprocessing.Process.__init__(self, name=processname)
		self.terminate = False
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
		
		self.udp_sock.settimeout(HostDataProvider.RECONNECT_RETRY_TIMEOUT)
		
		tries = 0
		while not self.terminate:
			
			if tries >= HostDataProvider.RECONNECT_RETRY_COUNT:
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
		self.terminate = True
		if self.udp_sock:
			self.udp_sock.close()
			

if __name__ == "__main__":
	signal.signal(signal.SIGINT, shutdown_handler)

	sock = utils.UDPSocket();
	
	channels = []
	
	reg_handler = reg.RegisterProtocolManager(sock, ("127.0.0.1", 20000), "testhost", "testservice")
	reg_handler.start()
	while True:
		identifier = reg_handler.next_open_request()
		if not identifier:
			break
		print "got open request:", identifier
		
		child = HostDataProvider("testprovider", identifier, ("127.0.0.1", 20000), None)
		child.start()
		channels.append(child)
		
		
		
		
		
		
		


