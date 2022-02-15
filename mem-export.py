#!/usr/bin/env -S python3 -u
import sys, os, mmap, random, datetime, time, ctypes, os.path
if len(sys.argv) != 2: raise Exception("Usage: " + sys.argv[0] + " /sys/bus/pci/devices/0000:03:00.0/resource5")
for x in range(3,4):
    os.system(f"setpci -s 00:0{x}:00.0 COMMAND=0x02")
mem = os.open(sys.argv[1], os.O_RDWR)
byte_len = os.path.getsize(sys.argv[1])
arr = mmap.mmap(mem, byte_len)
for idx in range(byte_len//4):
    u32 = ctypes.c_uint32.from_buffer(arr, idx*4)
    sys.stdout.buffer.write(u32)

