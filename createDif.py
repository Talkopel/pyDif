import struct
import jinja



if __name__ == "__main__":

	chunks = []

	with open("dump1.dat", "rb") as f:
		
		nextInLine = 0

		while nextInLine != -1:
			
			print 1

			nextInLine = struct.unpack('i', f.read(4))[0]

			chunks.append(f.read(nextInLine))


	print chunks	