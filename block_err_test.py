#!/usr/bin/env -Spython3 -u
# sctipt to analyze unreadable sectors appetrn on NVME. Pass /dev/nvme?n1 as a parameter
import sys, os, time

block_size = 512 * 8 #maximal bloxk size that speeds up detection
class XorShift64PrngIter:
    MOD = 2 ** 64
    def __init__(self, initial_state = 1):
        "Pass 0 as initial_state to get time-based initialization"
        while not initial_state or not (initial_state % self.MOD):
            import time
            initial_state = time.time_ns()
        self.state = initial_state % self.MOD

    def __iter__(self): return self

    def __next__(self):
        self.state ^= self.state >> 12
        self.state ^= (self.state << 25) % self.MOD
        self.state ^= self.state >> 27
        return (self.state * 2685821657736338717) % self.MOD

def test_read(f, block_idx):
    if (block_idx * block_size) % (64*1024*1024) == 0:
        print(f"testing {hex(block_idx)}*{block_size} byte...")
    read_size = block_size # should be multiple of block size for os.O_DIRECT
    start = time.time()
    try:
        result = os.pread(f, read_size, block_idx*block_size)
        if len(result) == read_size:
            return True
        else:
            print(f"{hex(block_idx)}*{block_size} byte read [{len(result)}]={result}")
            return False
    except OSError as e:
        print(f"{hex(block_idx)}*{block_size} byte IO Error {e} after {time.time() - start} seconds")
        return False
    except Exception as e:
        print(f"{hex(block_idx)}*{block_size} interrupted {e} after {time.time() - start} seconds")
        return False

def test_mode(mode, f, blocks, step, max_err, steps_sequence):
    print(f"Test {mode}")
    ok_count = 0
    err_count = 0
    for i in steps_sequence:
        current = test_read(f, (i * step) % blocks)
        if current:
            ok_count += 1
        else:
            err_count += 1
        if not current or i % 128 == 0:
            print(f"{ok_count=} {err_count=}")
        if max_err and err_count >= max_err:
            break

f = os.open(sys.argv[1], flags=os.O_RDONLY|os.O_DIRECT)
blocks = os.lseek(f, 0, 2) // block_size
print(f"size in {block_size}:{hex(blocks)}")

test_mode("pseudo_random", f, blocks, 1, 128, XorShift64PrngIter())
huge_step = 1024*1024
test_mode("overall_huge_step", f, blocks, huge_step, 0, range(0, blocks, huge_step))
mid_step = 1024
test_mode("mid_step", f, blocks, mid_step, 128, range(0, blocks, mid_step))
test_mode("start", f, blocks, 1, 128, range(0, blocks, 1))

