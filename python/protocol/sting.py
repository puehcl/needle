
import threading
import time
import socket
import Queue

import constants as const
import packet

PROBING_TIMEOUT = 0.5
RETRY_TIMEOUT = 10


class StreamListener(threading.Thread):
	
	def __init__(self, sock, agent_address):
		self.sock = sock
		self.agent_address = agent_address
		self.terminate = False
		
	def run(self):
		pass
		
	def shutdown(self):
		self.terminate = True
	

class StreamManager(threading.Thread):
		
	def __init__(self, sock, agent_address):
		threading.Thread.__init__(self)
		self.sock = sock
		self.agent_address = agent_address
		self.terminate = False
		self.input_queue = Queue.Queue()
		self.output_queue = Queue.Queue()
		self.timeout = 0
		
	def run(self):
		print "sting activated"
		
		sequence_number = 1
		start_time = time.time()
		self.sock.settimeout(PROBING_TIMEOUT)
		
		# stage one, send probing packets until other end answers or timeout occurs
		while True:
			time_delta = time.time() - start_time
			if time_delta >= RETRY_TIMEOUT:
				print "connection could not be established, exiting"
				self.shutdown()
				return
				
			probe_header = packet.Header(const.TYPE_CONTROL, const.SUBTYPE_PROBING, sequence_number)
			sequence_number = sequence_number + 1
			probe_packet = packet.Packet(probe_header)
			
			print "sending probe packet", probe_packet
			
			self.sock.sendto(probe_packet, self.agent_address)
			try:
				pack, addr = self.sock.recvfrom(65535)
				if addr == self.agent_address:
					if pack.subtype == const.SUBTYPE_PROBING:
						break
					if pack.subtype == const.SUBTYPE_SUCCESS:
						break
			except socket.timeout:
				continue
		
					
		print "received probing packet, entering stage 2", pack
		# stage two, send success packets until other end answers with success packets or timeout occurs	
		probe_header = packet.Header(const.TYPE_CONTROL, const.SUBTYPE_PROBING, sequence_number)
		sequence_number = sequence_number + 1
		probe_packet = packet.Packet(probe_header)		
		print "sending last probe packet", probe_packet	
		self.sock.sendto(probe_packet, self.agent_address)
				
		start_time = time.time()		
		while True:
			time_delta = time.time() - start_time
			if time_delta >= RETRY_TIMEOUT:
				print "connection could not be established, exiting"
				self.shutdown()
				return
				
			success_header = packet.Header(const.TYPE_CONTROL, const.SUBTYPE_SUCCESS, sequence_number)
			sequence_number = sequence_number + 1
			success_packet = packet.Packet(success_header)
			
			print "sending success packet", success_packet
			
			self.sock.sendto(success_packet, self.agent_address)
			pack, addr = self.sock.recvfrom(65535)
			if addr == self.agent_address:
				if pack.subtype == const.SUBTYPE_SUCCESS:
					break
		
		print "got success packet, connection to other agent open"
		
	def recv(self):
		try:
			return self.input_queue.get(True, self.timeout)
		except Queue.Empty:
			raise socket.timeout
		
	def send(data):
		self.output_queue.put(data)
		
	def settimeout(self, timeout):
		self.timeout = timeout
		
	def shutdown(self):
		self.terminate = True
		
		
		
		
		
