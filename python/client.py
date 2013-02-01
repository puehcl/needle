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
	for process in active_processes:
		process.shutdown()
		process.join()
		print "process", process.name, "shut down"
	if dataprovider:
		dataprovider.shutdown()
		dataprovider.join()
		print "listener shut down"
	sys.exit(0)

class ClientDataProvider(multiprocessing.Process):
	'''
	queries the mediator for a host address and establishes a connection to that host
	'''

	def __init__(self, sock, clientname, hostname, servicename, mediator_address):
		multiprocessing.Process.__init__(self)
		self.terminate = False
		self.sock = sock
		self.clientname = clientname
		self.hostname = hostname
		self.servicename = servicename
		self.mediator_address = mediator_address
		
	def run(self):
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
		self.sock.close()

if __name__ == "__main__":
	signal.signal(signal.SIGINT, shutdown_handler)

	sock = utils.UDPSocket();
	
	dataprovider = ClientDataProvider(sock, "testclient", "testhost", "testservice", ("127.0.0.1", 20000))
	dataprovider.start()
	
	dataprovider.join()
	
	
	
	
	
	
	
	
	
	
	
	
