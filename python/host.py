
import time
import threading
import signal
import sys
import socket

import utils
import packet
import data

seq_number = 1;
expected_ack_number = 1

clistener = None
active_processes = []

def shutdown_handler(signal, frame):
	for process in active_processes:
		process.shutdown()
		process.join()
		print "process", process.name, "shut down"
	if clistener:
		clistener.shutdown()
		clistener.join()
		print "listener shut down"
	sys.exit(0)

class ControlListener(threading.Thread):
	'''
	listens for incoming packets from the mediator
	'''

	def __init__(self, sock):
		threading.Thread.__init__(self)
		self.shutdown_ = False
		self.sock = sock
		self.setDaemon(True)
		
	def run(self):
		self.sock.settimeout(1)
	
		while not self.shutdown_:
			try:
				pack, addr = self.sock.recvfrom(65535)
			except socket.timeout:
				continue
				
			if pack.maintype != packet.TYPE_CONTROL:
				continue
				
			if pack.subtype == packet.SUBTYPE_AGENT_AGENT_ACK:
				print "received 'ack' packet", repr(pack)
			elif pack.subtype == packet.SUBTYPE_AGENT_AGENT_NACK:
				print "received 'nack' packet", repr(pack)
			elif pack.subtype == packet.SUBTYPE_SERVER_HOST_OPEN:
				print "received 'open' packet", repr(pack), "spawning child process"
				reference = packet.getServerHostOpenData(pack)
				channel = data.HostDataChannel("channel", reference, ("127.0.0.1", 20000), ("relay.net", 10000))
				channel.start()
				active_processes.append(channel)
			else:
				print "received unexpected packet", repr(pack)
				
	def shutdown(self):
		self.shutdown_ = True
		self.sock.close()

if __name__ == "__main__":
	signal.signal(signal.SIGINT, shutdown_handler)

	sock = utils.UDPSocket();
	
	clistener = ControlListener(sock)
	clistener.start()
	
	while True:
	
		print "sending register packet"
		pack = packet.getHostServerRegisterPacket(seq_number, "testhost", "testservice") 
		sock.sendto(pack, ("127.0.0.1", 20000))
		expected_ack_number = seq_number
		time.sleep(60)
		


