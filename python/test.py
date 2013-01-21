import utils
import packet


if __name__ == "__main__":

	a = b""
	print "put text sepp", repr(a), "64"
	b = utils.putText(a, "sepp", 64)
	print repr(b), "len", len(b)
	print "get text", repr(b), "64"
	print utils.getText(b, 64)

	p = packet.getHostServerRegisterPacket(1, "blubname", "blubservice")
	print p.number
	print p.maintype
	print repr(p.payload)
	print repr(p.toByteArray())
	
	print packet.getHostServerRegisterData(p.payload)
