#!/usr/bin/env -Spython3 -u
# sctipt to analyze unreadable sectors appetrn on NVME. Pass /dev/nvme?n1 as a parameter
import sys, os, time

block_size = 512 * 8 #maximal bloxk size that speeds up detection
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

def test_mode(mode, f, blocks, step, max_err, round_step):
    print(f"Test {mode}")
    ok_count = 0
    err_count = 0
    for i in range(0, blocks, step):
        current = test_read(f, (i * round_step) % blocks)
        if current:
            ok_count += 1
        else:
            err_count += 1
        if not current or (i / step) % 128 == 0:
            print(f"{ok_count=} {err_count=}")
        if max_err and err_count >= max_err:
            break

f = os.open(sys.argv[1], flags=os.O_RDONLY|os.O_DIRECT)
blocks = os.lseek(f, 0, 2) // block_size
print(f"size in {block_size}:{hex(blocks)}")

test_mode("pseudo_random", f, blocks, 1, 128, 999999000001)
test_mode("overall", f, blocks, 1024*1024, 0, 1)
test_mode("start", f, blocks, 1, 128, 1)

