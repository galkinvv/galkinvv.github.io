#!/usr/bin/env python3
import sys, os, mmap, random, datetime, time, ctypes, os.path
if len(sys.argv) != 2: raise Exception("Usage: " + sys.argv[0] + " /sys/bus/pci/devices/0000:03:00.0/resource5")
mem = os.open(sys.argv[1], os.O_RDWR)
arr = mmap.mmap(mem, os.path.getsize(sys.argv[1]))
sys.stdout.buffer.write(arr[:])

