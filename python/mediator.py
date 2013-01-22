
import socket

import utils
import packet

local_port = 20000

hosts_by_service = {}


class Host:

	def __init__(self, hostname, addr):
		self.hostname = hostname
		self.addr = addr
	

if __name__ == "__main__":
	sock = utils.UDPSocket((utils.ALL_INTERFACES, local_port))
	
	print "socket created on", sock.getsockname()
	

	while True:
		print "listening for packets"
		pack, addr = sock.recvfrom(65535)	
		print "received", repr(pack), "from", addr
		
		if pack.maintype != packet.TYPE_CONTROL:			#mediator doesn't handle data packets
			print "not a control packet, continue"
			continue
			
		if pack.subtype == packet.SUBTYPE_HOST_SERVER_REGISTER:
			hostname, servicename = packet.getHostServerRegisterData(pack)
			hosts_by_service[servicename] = Host(hostname, addr)
			print "host", hostname, "registered for service", servicename
		
			ack = packet.getAckPacket(pack.number+1, pack.number)	
			sock.sendto(ack, addr)
			print "sent", repr(ack), "to", addr, "(host)"
			
			op = packet.getServerHostOpenPacket(0)
			sock.sendto(op, addr)
			print "sent", repr(op), "to", addr, "(host)"
			
		if pack.subtype == packet.SUBTYPE_HOST_SERVER_RDY:
			hostname, servicename = packet.getHostServerReadyData(pack)
			print "received ready packet from", addr, hostname, servicename
			
			
	sock.close()
	
