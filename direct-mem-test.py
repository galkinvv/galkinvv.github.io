#!/usr/bin/env python3
import sys, os, mmap, random
random.seed(12111)
try:
    offset = int(sys.argv[1], 16)
    physmem = os.open("/dev/mem", os.O_RDWR)
    phys_arr = mmap.mmap(physmem, 4096*4096, offset=offset)
    data = os.urandom(len(phys_arr))
    phys_arr[:]=data
    data_possibly_modified = phys_arr[:]
    bad_addresses = []
    for i in range(len(data)):
        xored_error = data[i] ^ data_possibly_modified[i]
        if xored_error:
            bad_addresses.append(str(hex(i)) + " " + bin(xored_error))
            if len(bad_addresses) >= 256: break
    if not bad_addresses:
        print("No errors")
    else:
        columns = 0
        for kv in bad_addresses:
            print(kv, end = "\t")
            columns += 1
            if (columns >= 4):
                print("")
                columns = 0
finally:
    print("")
    os.system("setfont")
#os.lseek(physmem,offset, os.SEEK_SET)
#sys.stdout.buffer.write(phys_arr[:])
