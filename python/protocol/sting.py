
import threading
import time

import constants as const
import packet



class StreamManager(threading.Thread):
		
		def __init__(self, sock, agent_address):
			threading.Thread.__init__(self)
			self.sock = sock
			self.agent_address = agent_address
			self.terminate = False
			
		def run(self):
			pass
			
			
		def shutdown(self):
			self.terminate = True
