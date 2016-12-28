#!/usr/bin/env python3
import sys, os, mmap, random
random.seed(12111)
try:
    if len(sys.argv) < 2: raise Exception("Usage: " + sys.argv[0] + " C8000000")
    offset = int(sys.argv[1], 16)
    physmem = os.open("/dev/mem", os.O_RDWR)
    phys_arr = mmap.mmap(physmem, 1024*1024*96, offset=offset)
    passed = []
    def verify_no_errors_with_data(data, test_name):
        for itertion in range(10):
            phys_arr[:]=data
            data_possibly_modified = phys_arr[:]
            bad_addresses = {}
            for i in range(len(data)):
                xored_error = data[i] ^ data_possibly_modified[i]
                if xored_error:
                    if not bad_addresses:
                        print("first error detected")
                    if xored_error not in bad_addresses:
                        bad_addresses[xored_error] = [0, []]
                    bad_addresses[xored_error][0] += 1
                    all_addresses = bad_addresses[xored_error][1]
                    if len(all_addresses) < 4096:
                        all_addresses.append(i)
            if not bad_addresses:
                passed.append(test_name)
                return
            else:
                print(test_name + " total errors count: ", sum((v[0] for k, v in bad_addresses.items())))
                print("different errors patterns count: ", len(bad_addresses))
                print("patterns sorted by error count:")
                columns = 0
                patterns_by_count = sorted(bad_addresses.items(), key=lambda v:-v[1][0])
                for k, v in patterns_by_count:
                    print(bin(k), v[0], end = "\t")
                    if columns % 4 == 0:
                        print("")
                    columns += 1
                columns = 0
                k, v = patterns_by_count[0]
                print("")
                prev = v[1][0]
                print("First address for "+bin(k)+":", hex(prev))
                print("Address diffs:")
                for a in v[1][1:]:
                    print(hex(a - prev), end = "\t")
                    prev = a
                    if columns % 8 == 7:
                        print("")
                    columns += 1
            raise Exception("ERRORS found")
    #verify_no_errors_with_data(b'\xFF'*len(phys_arr), "ONEs")
    #verify_no_errors_with_data(b'\x00'*len(phys_arr), "ZERO")
    verify_no_errors_with_data(bytes(random.getrandbits(8) for i in range(len(phys_arr))), "rand")
finally:
    print("Before errors, foolowing passed:", passed)
    os.system("setfont")
#os.lseek(physmem,offset, os.SEEK_SET)
#sys.stdout.buffer.write(phys_arr[:])
