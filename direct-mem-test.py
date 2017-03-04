#!/usr/bin/env python3
import sys, os, mmap, random, datetime, time
random.seed(12111)
try:
    if len(sys.argv) < 2: raise Exception("Usage: " + sys.argv[0] + " C8000000 [mb_to_test]")
    offset = int(sys.argv[1], 16)
    if len(sys.argv) >= 3:
        bytes_to_test = int(1024 * 1024 * float(sys.argv[2]))
    else:
        bytes_to_test = 1024 * 1024 * 32 // 8 
    physmem = os.open("/dev/mem", os.O_RDWR)
    #physmem = os.open("/dev/fb0", os.O_RDWR)
    phys_arr = mmap.mmap(physmem, bytes_to_test, offset=offset)
    passed = []
    def bin8(byte):
        return "0b{:08b}".format(byte)
    def verify_no_errors_with_data(data, test_name):
        if len(phys_arr) > len(data):
            data += b'\x00' * (len(phys_arr) - len(data))
        print("Starting test " + test_name)
        phys_arr[:]=data
        data_possibly_modified = phys_arr[:]
        time.sleep(0.5)
        os.system("setfont")
        bad_addresses = {}
        all_errors = []
        bad_bits = [0]*8
        with open("/tmp/err"+datetime.datetime.now().isoformat(), "w") as addr_file:
            for i in range(len(data)):
                xored_error = data[i] ^ data_possibly_modified[i]
                if xored_error:
                    if not bad_addresses:
                        print("first error detected at " + hex(i))
                    #addr_file.write("{:08x}".format(i)+"\n")
                    if xored_error not in bad_addresses:
                        bad_addresses[xored_error] = [0, []]
                    bad_addresses[xored_error][0] += 1
                    all_addresses = bad_addresses[xored_error][1]
                    for b in range(8):
                        if xored_error & (1<<b): bad_bits[b] += 1
                    if len(all_addresses) < 0x4000:
                        all_addresses.append(i)
                    if len(all_errors) < 0x4000:
                        all_errors.append(i)
        if not bad_addresses:
            passed.append(test_name)
            return
        def totals():
            print("Total bytes tested: 4*" + str(len(data)//4))
            total_errors =  sum((v[0] for k, v in bad_addresses.items()))
            print(test_name + " total errors count: ", total_errors, " - every ", len(data)/total_errors, " OK: ", len(data) - total_errors)
            print("Bit error numbers:", ", ".join(map(str,bad_bits)))
            print("different errors patterns count: ", len(bad_addresses))
        totals()
        print("patterns sorted by error count:")
        columns = 0
        patterns_by_count = sorted(bad_addresses.items(), key=lambda v:-v[1][0])
        for k, v in patterns_by_count:
            print(bin8(k), v[0], end = "\t")
            if columns % 4 == 0:
                print("")
            columns += 1
        columns = 0
        k, v = patterns_by_count[0]
        print("")
        pat_to_print = {"total":all_errors, bin8(k):v[1]}
        for pk,pv in pat_to_print.items():
            prev = pv[0]
            print("First address for "+pk+":", hex(prev))
            print("Address diffs:")
            for a in pv[1:]:
                print(hex(a - prev), end = "\t")
                prev = a
                if columns % 8 == 7:
                    print("")
                columns += 1
        totals()
        raise Exception("ERRORS found")
    #verify_no_errors_with_data(b'\xFF'*len(phys_arr), "ONEs")
    #verify_no_errors_with_data(b'\x00'*len(phys_arr), "ZERO")
    #verify_no_errors_with_data(b'\x52\x52\x52\xff'*(len(phys_arr)//4), "special")
    verify_no_errors_with_data(b'\x55\xaa\x55'*(len(phys_arr)//3), "aa55")
    #verify_no_errors_with_data(bytes(random.getrandbits(8) for i in range(len(phys_arr))), "rand")
finally:
    print("Before errors, foolowing passed:", passed)
    os.system("setfont")
