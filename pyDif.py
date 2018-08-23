import os


if __name__ == "__main__":

	cmd = "heapDump64.exe " + str(os.getpid())

	a = {
		1: "hello wolrd!",
		2: "eyal is super gay"
	}

	os.system(cmd)


