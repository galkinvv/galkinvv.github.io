#!/usr/bin/env python3
# Copyright (C) 2017-2020 Vasily Galkin (galkinvv.github.io)
# This file may be used and redistributed accoring to GPLv3 license.

#1MB woking 1070 before mem init: \xfb\xac\xd0\xba\xff\xff\xff\xff\xfc\xac\xd0\xba\xff\xff\xff\xff (0badac??, ?? are rotating).
import sys, os, mmap, random, datetime, time
random.seed(12111)
passed = []
def run_test():
    if len(sys.argv) < 2: raise Exception("Usage: " + sys.argv[0] + " C8000000 [mb_to_test]")
    offset = int(sys.argv[1], 16)
    if len(sys.argv) >= 3:
        bytes_to_test = int(1024 * 1024 * float(sys.argv[2]))
    else:
        bytes_to_test = 1024 * 1024 * 32 // 8 
    physmem = os.open("/dev/" + os.environ.get("MEM","mem"), os.O_RDWR)
    #physmem = os.open("/dev/fb0", os.O_RDWR)
    phys_arr = mmap.mmap(physmem, bytes_to_test, offset=offset)
    #with open("/tmp/in", "rb") as binin: phys_arr[:]=binin.read() and sys.exit(0)
    #with open("/tmp/out", "wb") as binout: binout.write(phys_arr) and sys.exit(0)
    def bin8(byte):
        return "0b{:08b}".format(byte)
    def verify_no_errors_with_data(data, test_name):
        if len(phys_arr) > len(data):
            data += b'\x00' * (len(phys_arr) - len(data))
        #print("Starting test " + test_name)
        phys_arr[:]=data
        data_possibly_modified = phys_arr[:]
        #time.sleep(0.5)
        #os.system("setfont")
        bad_addresses = {}
        all_errors = []
        bad_bits = [0]*8
        for i in range(0x0000, len(data)):
            xored_error = data[i] ^ data_possibly_modified[i]
            if xored_error: #and xored_error == 0b01000000:
                if not bad_addresses:
                    print("first error detected at " + hex(i))
                    print("\\x" + "\\x".join("{:02x}".format(n) for n in data_possibly_modified[i:i+32]))
                #addr_file.write("{:08x}".format(i)+"\n")
                if xored_error not in bad_addresses:
                    bad_addresses[xored_error] = [0, []]
                bad_addresses[xored_error][0] += 1
                all_addresses = bad_addresses[xored_error][1]
                if 1:
                    for b in range(8):
                        if xored_error & (1<<b): bad_bits[b] += 1
                if 1:    
                    if len(all_addresses) < 0x4000:
                        all_addresses.append(i)
                    if len(all_errors) < 0x8000:
                        all_errors.append(i)
        if not bad_addresses:
            passed.append(test_name)
            return
        def totals():
            print("Total bytes tested: 4*" + str(len(data)//4))
            total_errors =  sum((v[0] for k, v in bad_addresses.items()))
            print(test_name + " total errors count: ", total_errors, " - every ", len(data)/total_errors, " OK: ", len(data) - total_errors)
            max_bit = max(bad_bits)
            others_avg_bit = (sum(bad_bits) - max_bit)/(len(bad_bits)-1)
            print("Bit error numbers:", ", ".join(map(str,bad_bits)), " max-avg=", max_bit - others_avg_bit)
            print("different errors patterns count: ", len(bad_addresses))
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
        k1, v1 = patterns_by_count[min(2, len(patterns_by_count))-1]
        print("")
        pat_to_print = {bin8(k1):v[1][:20], bin8(k):v1[1][:20], "noerr_big+":all_errors[:20], "total":all_errors[:20]}
        for pk,pv in pat_to_print.items():
            if not pv: continue 
            prev = pv[0]
            print("First address for "+pk+":", hex(prev))
            #continue
            print("Address diffs:")
            for a in pv[1:]:
                diff = a - prev
                if "big+" in pk:
                    if diff < 0x20:
                        prev = a
                        continue
                    print(hex(prev + 1), end = ":")
                print(hex(diff), end = "\t")
                prev = a
                if columns % 8 == 7:
                    print("")
                columns += 1
            print("\n")
        totals()
        raise Exception("ERRORS found in test " + test_name)
    dif_rands = 2048
    """
    verify_no_errors_with_data(
	#b'b'\x45\xff\x77\x48\x65\xff\x25\xce\x65\xff\x15\x66\x47\xff\x57\x6d\x45\xff\xff\x13\x07\xff\xf5\x45\x65\xff\x15\xb6\x47\xff\xd7\xae''
	b'\x9b\x8e\xb1\x02\xcf\x7a\xaf\x4e\xce\xfe\xff\x8e\xfe\x3b\xc2\xdd\x02\x9f\x0e\x2c\x58\xb6\xd7\x04\x7a\x54\xa2\x14\x48\x70\xe5\x4e'
        *(len(phys_arr)//32), "Polaris0x600Hynix")
    #"""
    #verify_no_errors_with_data(b'\xFF'*len(phys_arr), "ONEs")
    #verify_no_errors_with_data(b'\x00'*len(phys_arr), "ZERO")
    #verify_no_errors_with_data(b'\xCC'*len(phys_arr), "xCC")
    #verify_no_errors_with_data(b'\x55'*len(phys_arr), "x55")
    #verify_no_errors_with_data(b'\x31'*len(phys_arr), "x31")
    #verify_no_errors_with_data(b'\xaa'*len(phys_arr), "xaa")
    #verify_no_errors_with_data(b'\x12\x34\x56\x78\x9A\xBC\xDE\xF0\x46\xa3\xe5\x13\xad'*(len(phys_arr)//13), "special")
    #verify_no_errors_with_data(b'\x55\xaa\x55'*(len(phys_arr)//3), "aa55")
    amd_problem=0x200
    amd_total=0x8000
    amd_pat=b'\xee'*amd_problem + bytes(random.getrandbits(8) for i in range(0x100)) + b'\xaa'*(amd_total - 0x100 - amd_problem)
    #verify_no_errors_with_data(amd_pat * (len(phys_arr)//len(amd_pat)), "amd-mem")
    verify_no_errors_with_data(bytes(random.getrandbits(8) for i in range(len(phys_arr))), "rand")
    #verify_no_errors_with_data(bytes(random.getrandbits(8) for i in range(len(phys_arr))), "rand")
try:
    for i in range(1):
        run_test()
finally:
    os.system("setfont")
    print("Before errors, following passed:", passed)
    os.system("setfont")
