import struct
import jinja2
import os
import base64


def save_template(rendered_template):

	with open('static/main.js', 'w') as f:
		f.write(rendered_template)

def parse_heap(heapId):

	chunks = []

	with open(heapId+'.dat', 'rb') as f:

		data = f.read()

		chunk_size_index = 0

		while chunk_size_index < len(data):

			chunk_size = struct.unpack_from("I", data[chunk_size_index:])[0]

			chunk = data[chunk_size_index+4: chunk_size_index+chunk_size]

			chunk_size_index = chunk_size_index + 4 + chunk_size

			chunks.append(base64.b64encode(chunk))

	return chunks


if __name__ == "__main__":

	with open('static/main.temp.js', 'r') as f:
		template_text = f.read()

	heaps = [file[:-4] for file in os.listdir(os.getcwd()) if file[-4:] == '.dat']

	template = jinja2.Template(template_text)
	
	
	parsed_heaps_and_chunks = {}

	for heap in heaps:
		chunks = parse_heap(heap)
		parsed_heaps_and_chunks[heap] = chunks

	stream = template.render(heaps=heaps, parsed_heaps_and_chunks=parsed_heaps_and_chunks)

	save_template(stream)


