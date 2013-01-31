
import socket
import threading
import Queue
import time

import packet
import constants as const

QUEUE_TIMEOUT = 0.5
SOCKET_TIMEOUT = 0.5

MEDIATOR_REGISTER_RETRIES = 5
MEDIATOR_REGISTER_TIMEOUT = 5

MEDIATOR_COMM_TIMEOUT = 60



class RegisterProtocolListener(threading.Thread):
	
	def __init__(self, sock, mediator_address, requests):
		threading.Thread.__init__(self)
		self.terminate = False
		self.sock = sock
		self.mediator_address = mediator_address
		self.requests = requests
		
	def run(self):
		timeout = self.sock.gettimeout()
		self.sock.settimeout(SOCKET_TIMEOUT)
		
		while not self.terminate:
			try:
				pack, addr = self.sock.recvfrom(65535)	
				if addr != self.mediator_address:		
					continue
				if pack.maintype != const.TYPE_CONTROL:
					continue
				self.requests.put(pack)	
			except socket.timeout:
				continue
			
		# restore previous timeout
		self.sock.settimeout(timeout)
	
	def shutdown(self):
		self.terminate = True
			
	

class RegisterProtocolManager(threading.Thread):

	def __init__(self, sock, mediator_address, hostname, servicename):
		threading.Thread.__init__(self)
		self.sock = sock
		self.mediator_address = mediator_address
		self.hostname = hostname
		self.servicename = servicename
		self.requests = Queue.Queue()					# all requests from mediator, filled by listener
		self.open_requests = Queue.Queue()				# open requests from mediator, filled by manager
		self.listener = None
		self.terminate = False
		self.setDaemon(True)
		
	def run(self):
		self.listener = RegisterProtocolListener(	self.sock, 
													self.mediator_address, 
													self.requests)										
		self.listener.start()
		
		register_seq_nr = 1
		register_header = packet.Header(const.TYPE_CONTROL, const.SUBTYPE_REGISTER, register_seq_nr)
		register_packet = packet.Packet(register_header)
		register_packet.put_string(const.SPECTYPE_HOSTNAME, self.hostname, const.LEN_HOSTNAME)
		register_packet.put_string(const.SPECTYPE_SERVICENAME, self.servicename, const.LEN_SERVICENAME)
		
		ack_header = packet.Header(const.TYPE_CONTROL, const.SUBTYPE_ACK, 1)
		
		# send register packet
		self.sock.sendto(register_packet, self.mediator_address)
		register_tries = 1
		register_success = False
		
		time_at_last_packet = time.time()
		time_at_last_register = time.time()
		
		while not self.terminate:
			try:
				request = self.requests.get(True, QUEUE_TIMEOUT)
				print "received response", request
				
				time_at_last_packet = time.time()
				
				# if registration not yet acknowledged
				if not register_success:
					if not request.subtype == const.SUBTYPE_ACK:
						continue
					
					ack_nr = request[const.SEPCTYPE_ACK_SEQ_NR][0].value
					if ack_nr == register_seq_nr:
						register_success = True
						print "register success"
						
					continue
					
				if request.subtype == const.SUBTYPE_ALIVE:
					pack = packet.Packet(ack_header)
					ack_header = ack_header.incremented()
					pack.put_long(const.SEPCTYPE_ACK_SEQ_NR, request.number)
					self.sock.sendto(pack, self.mediator_address)
					print "alive ack sent"
					
				#if open request
				#add request to open_requests
			except Queue.Empty:		
				if register_success:
					comm_delta = time.time() - time_at_last_packet
					if comm_delta >= MEDIATOR_COMM_TIMEOUT:
						print "communication timeout exceeded (" + str(comm_delta) + "), reinitiating registration procedure"
						register_success = False
						register_tries = 0
					else:
						continue
					
				time_delta = time.time() - time_at_last_register
				if time_delta >= MEDIATOR_REGISTER_TIMEOUT:
					if register_tries >= MEDIATOR_REGISTER_RETRIES:
						print "no response from server, returning"
						self.shutdown()
						break
					print "registration timeout exceeded (" + str(time_delta) + "), resending register packet"
					self.sock.sendto(register_packet, self.mediator_address)
					time_at_last_register = time.time()
					register_tries = register_tries + 1
		
		self.listener.shutdown()
		self.listener.join()
		

	def next_open_request(self):
		while not self.terminate:
			try:
				return self.open_requests.get(True, QUEUE_TIMEOUT)			# block 
			except Queue.Empty:
				continue
				
		return None
			
	def shutdown(self):
		self.terminate = True
		if self.listener:
			self.listener.shutdown()
			
			
		
		
