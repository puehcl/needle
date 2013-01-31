import threading
import time

import protocol.constants as const
import protocol.socketutils as utils
import protocol.packet as packet
import protocol.register as reg

local_port = 20000

hosts_by_service = {}
hosts_by_address = {}
agents_by_reference = {}

ref = 1

class Host:

	def __init__(self, hostname, service, addr):
		self.hostname = hostname
		self.service = service
		self.addr = addr
		self.alive_counter = 5
		
	def increment(self):
		if self.alive_counter < 5:
			self.alive_counter = self.alive_counter + 1
			
	def decrement(self):
		if self.alive_counter > 0:
			self.alive_counter = self.alive_counter - 1
	
	def isalive(self):
		if self.alive_counter > 0:
			return True
		return False
		
	def __repr__(self):
		return self.hostname + ", " + self.service + ", " + str(self.addr) + ", alive_counter: " + str(self.alive_counter)
	
class Client:
	
	def __init__(self, clientname, addr):
		self.clientname = clientname
		self.addr = addr
		
class Watchdog(threading.Thread):

	TIMEOUT = 20

	def __init__(self, sock, lock):
		threading.Thread.__init__(self)
		self.sock = sock
		self.lock = lock
		self.terminate = False
		self.setDaemon(True)
		self.pack = packet.Packet(header=packet.Header(const.TYPE_CONTROL, const.SUBTYPE_ALIVE, 1))

	def run(self):
		while not self.terminate:
			time.sleep(Watchdog.TIMEOUT)
			if self.terminate:
				break
			remove = []
			self.lock.acquire()
			for host in hosts_by_address.itervalues():
				if not host.isalive():
					print "host is dead, removing: ", host
					remove.append(host)
				else:
					print "sending alive request to host", host
					host.decrement()
					self.sock.sendto(self.pack, host.addr)
					self.pack.increment()
				
			for host in remove:
				del hosts_by_address[host.addr]
				if host.service in hosts_by_service:
					hosts_by_service[host.service].remove(host)
				print "hosts_by_address:", hosts_by_address
				print "hosts_by_service:", hosts_by_service
						
			self.lock.release()
		
	def shutdown(self):
		self.terminate = True


if __name__ == "__main__":
	sock = utils.UDPSocket((utils.ALL_INTERFACES, local_port))
	print "socket created on", sock.getsockname()
	
	hostlock = threading.Lock()
	watchdog = Watchdog(sock, hostlock)
	watchdog.start()

	while True:
		print "listening for packets"
		pack, addr = sock.recvfrom(65535)	
		print "received", repr(pack), "from", addr
		
		if pack.maintype != const.TYPE_CONTROL:			#mediator doesn't handle data packets
			print "not a control packet, continue"
			continue
			
		if pack.subtype == const.SUBTYPE_REGISTER:
			hostname = pack[const.SPECTYPE_HOSTNAME][0].value
			servicename = pack[const.SPECTYPE_SERVICENAME][0].value

			if not servicename in hosts_by_service:
				hosts_by_service[servicename] = []
				
			host = Host(hostname, servicename, addr)
			hostlock.acquire()
			hosts_by_service[servicename].append(host)
			hosts_by_address[addr] = host
			hostlock.release()
			print "host", hostname, "registered for service", servicename
		
			ack_header = packet.Header(const.TYPE_CONTROL, const.SUBTYPE_ACK, 1)
			ack_packet = packet.Packet(ack_header)
			ack_packet.put_long(const.SEPCTYPE_ACK_SEQ_NR, pack.number)
			sock.sendto(ack_packet, addr)
			print "sent", repr(ack_packet), "to", addr, "(host)"
			
		elif pack.subtype == const.SUBTYPE_ACK:
			if addr in hosts_by_address:
				host = hosts_by_address[addr]
				host.increment()
			
		elif pack.subtype == const.SUBTYPE_REQ_HOST:
			clientname = pack[const.SPECTYPE_CLIENTNAME][0].value
			hostname = pack[const.SPECTYPE_HOSTNAME][0].value
			servicename = pack[const.SPECTYPE_SERVICENAME][0].value
			
			if not servicename in hosts_by_service:
				continue
				
			host = None
			for h in hosts_by_service[servicename]:
			
				if h.hostname == hostname:
					host = h
					break
		
			if host == None:
				continue
				
			reference = ref
			ref = ref + 1
			
			agents_by_reference[reference] = (host, Client(clientname, addr))
			
			ref_header = packet.Header(const.TYPE_CONTROL, const.SUBTYPE_HOST_OPEN, 1)
			ref_packet = packet.Packet(ref_header)
			
			ref_packet.put_int(const.SPECTYPE_REFERENCE_NR, reference)
			
			sock.sendto(ref_packet, host.addr)
			print "sent", repr(ref_packet), "to", host.addr, "(host)"
			
		elif pack.subtype == const.SUBTYPE_HOST_READY:
			reference_nr = pack[const.SPECTYPE_REFERENCE_NR][0].value
			
			if not reference in agents_by_reference:
				nack_header = packet.Header(const.TYPE_CONTROL, const.SUBTYPE_NACK, 1)
				nack_packet = packet.Packet(nack_header)
				nack_packet.put_long(const.SPECTYPE_NACK_SEQ_NR, pack.number)
				sock.sendto(nack_packet, addr)
				continue
				
			agents = agents_by_reference[reference]
			host = agents[0]
			client = agents[1]
			
			if not host.addr[0] == addr[0]:
				print "wrong host ip"
				continue
				
			host_header = packet.Header(const.TYPE_CONTROL, const.SUBTYPE_AGENT_ADDR, 1)
			host_packet = packet.Packet(host_header)
			host_packet.put_ip(const.SPECTYPE_AGENT_IP, client.addr[0])
			host_packet.put_int(const.SPECTYPE_AGENT_PORT, client.addr[1])
			
			client_header = packet.Header(const.TYPE_CONTROL, const.SUBTYPE_AGENT_ADDR, 1)
			client_packet = packet.Packet(client_header)
			client_packet.put_ip(const.SPECTYPE_AGENT_IP, addr[0])
			client_packet.put_int(const.SPECTYPE_AGENT_PORT, addr[1])
			
			sock.sendto(host_packet, addr)
			sock.sendto(client_packet, client.addr)
			print "sent connect packets"
			
		
			
	sock.close()
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
