#!/usr/bin/env python3
import os, sys
for x in range(8, 0x78): 
    print("Dumping " + hex(x) + " on " + sys.argv[1])
    os.system("i2cdump -y "+ sys.argv[1] + " " + hex(x))
