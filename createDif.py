import struct
import jinja2
import os
import base64

def save_template(rendered_template):

	with open('static/main.js', 'w') as f:
		f.write(rendered_template)

def parse_heap(heapFile):

	chunks = []

	this_arch = heapFile[:3]

	struct_by_arch = {
		'x64': {
			"HANDLE": "Q",
			"ULONG_PTR": "Q"

		},

		'x86': {
			"HANDLE": "I",
			"ULONG_PTR": "I"
		}
	}

	element_size_packed = {
		'x64': {
			"HANDLE": 8,
			"ULONG_PTR": 8
		},
		'x86': {
			"HANDLE": 4,
			"ULONG_PTR": 4
		}
	}

	with open(heapFile+'.dat', 'rb') as f:

		data = f.read()

		chunk_size_index = 0

		while chunk_size_index < len(data):

			next_object_index = 0

			meta_size = struct.unpack_from("I", data[chunk_size_index:])[0]
			next_object_index = next_object_index + 4
			print "meta_size: "+str(meta_size)

			meta_handle = struct.unpack_from(struct_by_arch[this_arch]["HANDLE"], data[chunk_size_index+next_object_index:])[0]
			next_object_index = next_object_index + element_size_packed[this_arch]["HANDLE"]
			print "next object in: "+str(next_object_index+chunk_size_index)

			meta_address = struct.unpack_from(struct_by_arch[this_arch]["ULONG_PTR"], data[chunk_size_index+next_object_index:])[0]
			next_object_index = next_object_index + element_size_packed[this_arch]["ULONG_PTR"]

			meta_blockSize = struct.unpack_from("I",data[chunk_size_index+next_object_index:])[0]
			next_object_index = next_object_index + 4

			meta_flags = struct.unpack_from("I",data[chunk_size_index+next_object_index:])[0]
			next_object_index = next_object_index + 4

			meta_lockCount = struct.unpack_from("I",data[chunk_size_index+next_object_index:])[0]
			next_object_index = next_object_index + 4

			meta_rsrvd = struct.unpack_from("I",data[chunk_size_index+next_object_index:])[0]
			next_object_index = next_object_index + 4

			meta_processId =  struct.unpack_from("I",data[chunk_size_index+next_object_index:])[0]
			next_object_index = next_object_index + 4

			meta_heapId =  struct.unpack_from(struct_by_arch[this_arch]["ULONG_PTR"], data[chunk_size_index+next_object_index:])[0]
			next_object_index = next_object_index + element_size_packed[this_arch]["ULONG_PTR"]

			meta_data = data[chunk_size_index+next_object_index: chunk_size_index+meta_blockSize]
			meta_data = base64.b64encode(meta_data)

			chunk_size_index = chunk_size_index + next_object_index + meta_blockSize
			# print "data length: "+ str(len(data))
			# print "next chunk index: "+str(chunk_size_index)
			chunk = {
				'meta_size': meta_size,
				'meta_handle': meta_handle,
				'meta_address': meta_address,
				'meta_blockSize': meta_blockSize,
				'meta_flags': meta_flags,
				'meta_lockCount': meta_lockCount,
				'meta_rsrvd': meta_rsrvd,
				'meta_processId': meta_processId,
				'meta_heapId': meta_heapId,
				'meta_data': "this is data"
			}



			chunks.append(chunk)


	return chunks


if __name__ == "__main__":

	with open('static/main.temp.js', 'r') as f:
		template_text = f.read()

	heaps = [file[:-4] for file in os.listdir(os.getcwd()) if file[-4:] == '.dat']

	template = jinja2.Template(template_text)
	
	chunks = parse_heap(heaps[0])
	print chunks[0]
	raw_input()
	
	# parsed_heaps_and_chunks = {}

	# for heap in heaps:
	# 	chunks = parse_heap(heap)
	# 	parsed_heaps_and_chunks[heap] = chunks

	# stream = template.render(heaps=heaps, parsed_heaps_and_chunks=parsed_heaps_and_chunks)

	# save_template(stream)


