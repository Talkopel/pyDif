import struct
import jinja2
import os


if __name__ == "__main__":

	with open('static/main.js', 'r') as f:
		template_text = f.read()

	heaps = [file for file in os.listdir(os.getcwd()) if file.split('.')[1] == 'dat']

	print heaps

	# template = jinja2.Template(template_text)
	# heaps = "Hello world!"
	# stream = template.render(text=text)
	
	# print stream

