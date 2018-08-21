import os


if __name__ == "__main__":

	cmd = "heapDump.exe " + str(os.getpid())

	os.system(cmd)


