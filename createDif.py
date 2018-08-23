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

	heap_entry_fmt = {
		'x86': 'IIIIIIIII',
		'x64': 'QQQQIIIIQ'
	}

	heap_entry_size = {
		'x86': 36,
		'x64': 56
	}

	with open(heapFile+'.dat', 'rb') as f:

		data = f.read()

		chunk_size_index = 0

		while chunk_size_index < len(data):

			heap_entry = struct.unpack_from(heap_entry_fmt[this_arch], data[chunk_size_index:])

			chunk = {
				'meta_size': heap_entry[0]	,
				'meta_handle': heap_entry[1],
				'meta_address': heap_entry[2],
				'meta_blockSize': heap_entry[3],
				'meta_flags': heap_entry[4],
				'meta_lockCount': heap_entry[5],
				'meta_rsrvd': heap_entry[6],
				'meta_processId': heap_entry[7],
				'meta_heapId': heap_entry[8],
				'meta_data': data[chunk_size_index+heap_entry_size[this_arch]:chunk_size_index+heap_entry_size[this_arch]+heap_entry[3]]
			}

			
			chunk_size_index = chunk_size_index + heap_entry_size[this_arch] + chunk['meta_blockSize']

			chunks.append(chunk)


	return chunks


if __name__ == "__main__":

	with open('static/main.temp.js', 'r') as f:
		template_text = f.read()

	heaps = [file[:-4] for file in os.listdir(os.getcwd()) if file[-4:] == '.dat']

	template = jinja2.Template(template_text)
	
	parsed_heaps_and_chunks = {}

	for heap in heaps:
		parsed_heaps_and_chunks[heap] = parse_heap(heap)

	stream = template.render(parsed_heaps_and_chunks=parsed_heaps_and_chunks, heaps=heaps)

	save_template(stream)


