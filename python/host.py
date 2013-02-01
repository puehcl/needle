
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
import protocol.sting as sting

seq_number = 1;
expected_ack_number = 1

reg_handler = None
channels = []

def shutdown_handler(signal, frame):
	for channel in channels:
		channel.shutdown()
		channel.join()
		print "process", channel.name, "shut down"
	if reg_handler:
		reg_handler.shutdown()
		reg_handler.join()
		print "registration handler shut down"
	sys.exit(0)

class HostDataProvider(multiprocessing.Process):

	RECONNECT_RETRY_COUNT = 5		
	RECONNECT_RETRY_TIMEOUT = 5		

	def __init__(self, processname, reference, mediator_address, relay_address):
		multiprocessing.Process.__init__(self, name=processname)
		self.terminate = False
		self.reference = reference
		self.mediator_address = mediator_address
		self.relay_address = relay_address
		self.sock = None
		
	def run(self):
		print "channel", self.name, "active"
		try:
			self.sock = utils.UDPSocket()
		except socket.error as se:
			print "an error has occured while creating the socket:", repr(se)
			return
		
		tries = 0
			
		if tries >= HostDataProvider.RECONNECT_RETRY_COUNT:
			print "maximum retries reached, connection to server lost, returning"
			return
		
		print "getting rdy packet"
		rdy_header = packet.Header(const.TYPE_CONTROL, const.SUBTYPE_HOST_READY, 1)
		rdy_packet = packet.Packet(rdy_header)
		
		rdy_packet.put_int(const.SPECTYPE_REFERENCE_NR, self.reference)
		
		
		tries = 0
		client_info = None
		while tries < HostDataProvider.RECONNECT_RETRY_COUNT:
			self.sock.sendto(rdy_packet, self.mediator_address)		
			print "rdy packet sent to", self.mediator_address
			client_info = self.wait_for_packet(const.SUBTYPE_AGENT_ADDR, HostDataProvider.RECONNECT_RETRY_TIMEOUT)
			if client_info == None:
				tries = tries + 1
				continue
			break
		
		if not client_info or self.terminate:
			print "data provider shutting down"
			self.shutdown()
			return
			
			
			
		print "got agent info packet, starting sting"
			
		ip_bytes = client_info[const.SPECTYPE_AGENT_IP][0].value
		port = client_info[const.SPECTYPE_AGENT_PORT][0].value
		ip = ".".join([str(b) for b in ip_bytes])
				
		datastream = sting.StreamManager(self.sock, (ip, port), host=True)
		datastream.start()
		
					
		datastream.shutdown()
		datastream.join()

	def wait_for_packet(self, subtype, timeout):
		to = self.sock.gettimeout()
		start_time = time.time()
		pack = None
		self.sock.settimeout(timeout)
		while not self.terminate:
			time_delta = time.time() - start_time
			if time_delta >= timeout:
				break
			try:
				pack, addr = self.sock.recvfrom(65535)
				if addr == self.mediator_address:
					if pack.subtype == subtype:
						break
			except socket.timeout:
				break
		
		self.sock.settimeout(to)
		return pack
			
	def shutdown(self):
		self.terminate = True
		if self.sock:
			self.sock.close()
			

if __name__ == "__main__":
	signal.signal(signal.SIGINT, shutdown_handler)

	sock = utils.UDPSocket();
	
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
		
		
		
		
		
		
		


