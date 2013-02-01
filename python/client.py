import time
import threading
import multiprocessing
import signal
import sys
import socket

import protocol.constants as const
import protocol.socketutils as utils
import protocol.packet as packet
import protocol.sting as sting

REQ_TIMEOUT = 5
REQ_RETRIES = 5

dataprovider = None
active_processes = []

def shutdown_handler(signal, frame):
	client.shutdown()
	client.join()
	sys.exit(0)

class ClientDataProvider(multiprocessing.Process):
	'''
	queries the mediator for a host address and establishes a connection to that host
	'''

	def __init__(self, tcp_socket, clientname, hostname, servicename, mediator_address):
		multiprocessing.Process.__init__(self)
		self.terminate = False
		self.tcp_socket = tcp_socket
		self.sock = None
		self.clientname = clientname
		self.hostname = hostname
		self.servicename = servicename
		self.mediator_address = mediator_address
		
	def run(self):
		self.sock = utils.UDPSocket();
		self.sock.settimeout(REQ_TIMEOUT)
	
		req_header = packet.Header(const.TYPE_CONTROL, const.SUBTYPE_REQ_HOST, 1)
		req_packet = packet.Packet(req_header)
		req_packet.put_string(const.SPECTYPE_CLIENTNAME, self.clientname, const.LEN_CLIENTNAME)
		req_packet.put_string(const.SPECTYPE_HOSTNAME, self.hostname, const.LEN_HOSTNAME)
		req_packet.put_string(const.SPECTYPE_SERVICENAME, self.servicename, const.LEN_SERVICENAME)
		
		last_req_time = 0
		response = None
		
		tries = 0
		while tries < REQ_RETRIES and not self.terminate:
			self.sock.sendto(req_packet, self.mediator_address)
			last_req_time = time.time()
			while not self.terminate:
				try:
					pack, addr = self.sock.recvfrom(65535)
					if pack.maintype == const.TYPE_CONTROL:
						if pack.subtype == const.SUBTYPE_AGENT_ADDR:
							response = pack
							break
						elif pack.subtype == const.SUBTYPE_NACK:
							print "server sent nack, no so such host/service available"
							self.shutdown()
							return
				except socket.timeout:
					pass
					
				req_delta = time.time() - last_req_time					# break loop to try again 
				if req_delta >= REQ_TIMEOUT:
					break
			if response:												
				break
					
			tries = tries + 1
					
		if not response:
			print "mediator did not answer, aborting"
			self.shutdown()
			return
		
		print "mediator sent agent info:", response
	
		ip_bytes = response[const.SPECTYPE_AGENT_IP][0].value
		port = response[const.SPECTYPE_AGENT_PORT][0].value
		ip = ".".join([str(b) for b in ip_bytes])
	
		datastream = sting.StreamManager(self.sock, (ip, port))
		datastream.start()
		
		datastream.shutdown()
		datastream.join()
				
	def shutdown(self):
		self.terminate = True
		if self.sock:
			self.sock.close()


class NeedleClient(threading.Thread):

	LISTEN_TIMEOUT = 0.5

	def __init__(self, local_address, mediator_address, clientname, hostname, servicename):
		threading.Thread.__init__(self)
		self.local_address = local_address
		self.mediator_address = mediator_address
		self.clientname = clientname
		self.hostname = hostname
		self.servicename = servicename
		self.terminate = False
		self.ready = False
		self.providers = []
		
	def run(self):
		self.tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.tcp_socket.bind(self.local_address)
		self.tcp_socket.listen(5)
		self.tcp_socket.settimeout(NeedleClient.LISTEN_TIMEOUT)
		
		self.ready = True
		
		while not self.terminate:
			try:
				new_sock = self.tcp_socket.accept()		
				dataprovider = ClientDataProvider(new_sock[0], self.clientname, self.hostname, self.servicename, self.mediator_address)
				dataprovider.start()
				self.providers.append(dataprovider)
			except socket.timeout:
				continue
		
	def is_ready(self):
		return self.ready
		
	def shutdown(self):
		self.terminate = True
		for provider in self.providers:
			provider.shutdown()
			provider.join()

if __name__ == "__main__":
	signal.signal(signal.SIGINT, shutdown_handler)

	local_address = ("127.0.0.1", 30000)
	mediator_address = ("127.0.0.1", 20000)

	client = NeedleClient(local_address, mediator_address, "testclient", "testhost", "testservice")
	client.start()
	
	while not client.is_ready():
		time.sleep(1)
	
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.connect(local_address)
	
	print "socket open, waiting for input"
	
	while True:
		inp = raw_input()
		sock.send(inp)
	
	
	
	
	
	
	
	
	
	
	
	
	
