
import time
import threading
import multiprocessing
import signal
import sys
import socket
import Queue

import protocol.constants as const
import protocol.socketutils as utils
import protocol.packet as packet
import protocol.register as reg
import protocol.sting as sting

def shutdown_handler(signal, frame):
	host.shutdown()
	host.join()
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
		self.relay_socket = None
		
	def run(self):
		print "channel", self.name, "active"
		try:
			self.sock = utils.UDPSocket()
			self.relay_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
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
				
		datastream = sting.StreamManager(self.sock, (ip, port))
		datastream.start()
		
		self.relay_socket.connect(self.relay_address)
		
		while not self.terminate:
			print "reading data from datastream"
			data = datastream.recv()
			if not data:
				print "datastream returned not, connection closed"
				self.shutdown()
				break
			self.relay_socket.send(data)
					
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
		if self.relay_socket:
			self.relay_socket.close()
			

class NeedleHost(threading.Thread):

	def __init__(self, mediator_address, relay_address, hostname, servicename):
		threading.Thread.__init__(self)
		self.mediator_address = mediator_address
		self.relay_address = relay_address
		self.hostname = hostname
		self.servicename = servicename
		self.terminate = False
		self.reg_handler = None
		self.channels = []
		self.setDaemon(True)
		
	def run(self):
		self.sock = utils.UDPSocket();
	
		self.reg_handler = reg.RegisterProtocolManager(self.sock, self.mediator_address, self.hostname, self.servicename)
		self.reg_handler.start()
		while not self.terminate:
			identifier = self.reg_handler.next_open_request()
			if not identifier:
				break
			if self.terminate:
				break
			print "got open request:", identifier
		
			child = HostDataProvider("testprovider", identifier, self.mediator_address, self.relay_address)
			child.start()
			self.channels.append(child)

	def shutdown(self):
		self.terminate = True
		if self.reg_handler:
			print "shutting down register handler"
			self.reg_handler.shutdown()
			self.reg_handler.join()
		for channel in self.channels:
			print "shutting down channel"
			channel.shutdown()
			channel.join()
		

if __name__ == "__main__":
	signal.signal(signal.SIGINT, shutdown_handler)

	local_address = ("127.0.0.1", 10001)
	mediator_address = ("127.0.0.1", 20000)

	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.bind(local_address)
	sock.listen(5)

	host = NeedleHost(mediator_address, local_address, "testhost", "testservice")
	host.start()
		
	tup = sock.accept()
	actual = tup[0]
	print "got socket, reading..."
	while True:
		data, addr = actual.recv(1024)
		print data
		
		
		
		
		
		


