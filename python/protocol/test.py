
import packet


if __name__ == "__main__":
	
	header = packet.Header(1, 2, 3)
	pack = packet.Packet(header=header)
	
	pack.put_int(2, 232)
	pack.put_string(5, "asdfasdf", 20)
	
	pack.pad(401) 
	
	print repr(pack)
	
	bytestr = pack.to_byte_string()
	
	print repr(bytestr)
	
	incpack = packet.Packet(bytedata=bytestr)
	
	print repr(incpack)
