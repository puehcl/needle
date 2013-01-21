
import socket

import utils
import packet

local_port = 20000

hosts_by_service = {}

host_addr = None

if __name__ == "__main__":
	sock = utils.UDPSocket((utils.ALL_INTERFACES, local_port))
	
	print "socket created on", sock.getsockname()
	

	while True:
		pack, addr = sock.recvfrom(65535)	
		print "received", repr(pack), "from", addr
		
		ack = packet.getAckPacket(pack.number+1, pack.number)
		
		sock.sendto(ack, addr)
		print "sent", repr(ack), "to", addr, "(client)"
			
	sock.close()
	
