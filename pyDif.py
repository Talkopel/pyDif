import os


if __name__ == "__main__":

	cmd = "heapDump64.exe " + str(os.getpid())

	os.system(cmd)


