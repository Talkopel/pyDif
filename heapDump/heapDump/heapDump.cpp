// heapDump.cpp : Defines the entry point for the console application.
//

#include "stdafx.h"
#include "windows.h"
#include "tlhelp32.h"
#include "stdlib.h"

#define null NULL

static char* fileOut = null;


int openGivenProcess(int pid, HANDLE *processHandle)
{

	*processHandle = OpenProcess(
		PROCESS_VM_READ | PROCESS_QUERY_INFORMATION | PROCESS_ALL_ACCESS,
		false,
		pid);

	if (null == *processHandle)
	{
		fprintf(stdout, "coudlnt open process with pid %d\r\n", pid);
		return -1;
	}

	else return 0;
}


void * copyBlock(LPHEAPENTRY32 entry, HANDLE processHandle, size_t pid)
/* returns allocated buffer pointer - free after writing to file! */
{
	SIZE_T bytesRead = 0;
	SIZE_T query = 0;
	int readResult = 0;
	char *copyBuffer = null;
	size_t *blockSize = null;
	void *toCopy = null;
	
	copyBuffer = (char *)malloc(( 4 + entry->dwBlockSize ));

	blockSize = (size_t *)copyBuffer;

	*blockSize = entry->dwBlockSize;

	toCopy = copyBuffer + sizeof(size_t);

	readResult = ReadProcessMemory(
		processHandle,
		(void *)(entry->dwAddress),
		(void *)toCopy,
		(size_t)entry->dwBlockSize,
		&bytesRead
		);


	if (0 == readResult)
	{
		if (0 != bytesRead)
		{
			return copyBuffer;
		}
		else
		{
			fprintf(stdout, "error reading process memory %u. bytes read: %d\r\n", GetLastError(), bytesRead);
			free(copyBuffer);
		}

		return null;
	}


	return copyBuffer;
	
}




int main(size_t argc, char** argv)
{
	HANDLE processSnap = null;
	HANDLE processToRead = null;
	unsigned int pid = null;
	HEAPLIST32 heapListObj;
	HEAPENTRY32 heapObj;
	void  *copiedMem = null;
	char outFile[32];
	FILE *dump = null;


	if (argc != 2)
	{
		fprintf(stdout, "usage: headDump <PID>");
		return -1;
	}

	memset(&heapListObj, null, sizeof(HEAPLIST32));
	memset(&heapObj, null, sizeof(HEAPENTRY32));


	pid = atoi(argv[1]);

	switch (errno)
	{
	case ERANGE:
			return -1;
	case EINVAL:
			return -1;
	}


	processSnap = CreateToolhelp32Snapshot(
		TH32CS_SNAPALL,
		pid
		);

	if (INVALID_HANDLE_VALUE == processSnap)
	{
		fprintf(stdout, "failed to open snapshot process");
		return -1;
	}

	
	if (0 != openGivenProcess(pid, &processToRead))
	{
		fprintf(stdout, "failed to open process for reading");
		return -1;
	}


	heapListObj.dwSize = sizeof(HEAPLIST32);

	if (Heap32ListFirst(processSnap, &heapListObj))
	{

		do
		{
			memset(&heapObj, null, sizeof(HEAPENTRY32));

			heapObj.dwSize = sizeof(HEAPENTRY32);

			snprintf(outFile, 32, "%u.dat", heapListObj.th32HeapID);
			
			
			if (fopen_s(&dump, outFile, "wb") != 0)
			{
				fprintf(stdout, "couldn't create file for heapId: %u\r\n", heapListObj.th32HeapID);
				return -1;
			}
			
			
			if (Heap32First(&heapObj, pid, heapListObj.th32HeapID))
			{
				do
				{
					copiedMem = copyBlock(&heapObj, processToRead, pid);
					if (null == copiedMem)
					{
						continue;
					}
					
					fwrite(copiedMem, 1, heapObj.dwBlockSize + 4, dump);

					free(copiedMem);

					heapObj.dwSize = sizeof(HEAPENTRY32);
					
				} while (Heap32Next(&heapObj));
			}

			heapListObj.dwSize = sizeof(HEAPLIST32);
			fclose(dump);
		} while (Heap32ListNext(processSnap, &heapListObj));
	}

	return 0;

}
