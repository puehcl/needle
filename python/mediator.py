import threading
import time

import protocol.socketutils as utils
import protocol.packet as packet
import protocol.exchange as ex

local_port = 20000

hosts_by_service = {}
hosts_by_address = {}
agents_by_reference = {}

ref = 0

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
		self.pack = packet.Packet(header=packet.Header(packet.TYPE_CONTROL, ex.SUBTYPE_ALIVE, 1))

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
		
		if pack.maintype != packet.TYPE_CONTROL:			#mediator doesn't handle data packets
			print "not a control packet, continue"
			continue
			
		if pack.subtype == ex.SUBTYPE_REGISTER:
			hostname = pack[ex.SPECTYPE_HOSTNAME][0].value
			servicename = pack[ex.SPECTYPE_SERVICENAME][0].value

			if not servicename in hosts_by_service:
				hosts_by_service[servicename] = []
				
			host = Host(hostname, servicename, addr)
			hostlock.acquire()
			hosts_by_service[servicename].append(host)
			hosts_by_address[addr] = host
			hostlock.release()
			print "host", hostname, "registered for service", servicename
		
			ack_header = packet.Header(packet.TYPE_CONTROL, ex.SUBTYPE_ACK, 1)
			ack_packet = packet.Packet(ack_header)
			ack_packet.put_long(ex.SEPCTYPE_ACK_SEQ_NR, pack.number)
			sock.sendto(ack_packet, addr)
			print "sent", repr(ack_packet), "to", addr, "(host)"
			
		elif pack.subtype == ex.SUBTYPE_ACK:
			if addr in hosts_by_address:
				host = hosts_by_address[addr]
				host.increment()
			
			
		elif pack.subtype == packet.SUBTYPE_HOST_SERVER_RDY:
			reference = packet.getHostServerReadyData(pack)
			
			if not reference in agents_by_reference:
				continue
				
			agents = agents_by_reference[reference]
			host = agents[0]
			client = agents[1]
			
			if not host.addr[0] == addr[0]:
				print "wrong host ip"
				continue
				
			tohost = packet.get_server_agent_connect_packet(0, (client.clientname, client.addr[0], client.addr[1]))
			toclient = packet.get_server_agent_connect_packet(0, (host.hostname, host.addr[0], host.addr[1]))
			
			sock.sendto(tohost, addr)
			sock.sendto(toclient, client.addr)
			print "sent connect packets"
			
		elif pack.subtype == packet.SUBTYPE_CLIENT_SERVER_REQ_HOST:
		
			clientname, hostname, service = packet.get_client_server_req_host_data(pack)
			
			if not service in hosts_by_service:
				continue
				
			host = None
			for h in hosts_by_service[service]:
			
				if h.hostname == hostname:
					host = h
					break
		
			if host == None:
				continue
				
			reference = ref
			ref = ref + 1
			
			agents_by_reference[reference] = (host, Client(clientname, addr))
			
			op = packet.getServerHostOpenPacket(0, reference)
			sock.sendto(op, host.addr)
			print "sent", repr(op), "to", host.addr, "(host)"
			
	sock.close()
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
