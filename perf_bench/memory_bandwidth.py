import numpy as np
import time
from typing import Tuple
import threading

# Function to measure RAM-to-RAM memory copy bandwidth
def single_threaded_memory_bandwidth(
        array_shape: Tuple = (4096, 4096), # make sure this is bigger than L3 cache
        num_iterations: int = 1000,
        warmup_iterations: int = 100
    ) -> Tuple[float, float]:
    
    size_in_bytes = np.prod(array_shape, dtype=np.float32) * 4  # Assuming float32 (4 bytes per element)
    array_src = np.random.rand(*array_shape).astype(np.float32)
    array_dst = np.empty_like(array_src)
    
    # Warm-up phase
    for _ in range(warmup_iterations):
        np.copyto(array_dst, array_src)
    
    # Timed runs
    times = []
    for _ in range(num_iterations):
        start = time.perf_counter()
        np.copyto(array_dst, array_src)
        end = time.perf_counter()
        times.append(end - start)
    
    avg_time = sum(times) / len(times)
    bandwidth = size_in_bytes / avg_time / (1024**3)  # Convert to GB/s
    
    print(f"--- Single-threaded RAM-to-RAM Copy---")
    print(f"Array size       : {array_shape[0]}×{array_shape[1]} (≈{size_in_bytes/1024**2:.1f} MiB)")
    print(f"Average Copy Time: {avg_time:.6f} seconds")
    print(f"Effective Bandwidth: {bandwidth:.2f} GB/s")

    return avg_time, bandwidth

def multithreaded_memory_bandwidth(
        array_shape: Tuple[int, int] = (4096, 4096),
        num_iterations: int = 1000,
        warmup_iterations: int = 100,
        num_threads: int = 4
    ) -> Tuple[float, float]:
    """
    Splits a large float32 array copy across `num_threads` threads to
    approximate multi-channel DRAM bandwidth.
    Returns (avg_time_s, bandwidth_GBps).
    """
    # Total bytes to copy per iteration
    size_in_bytes = np.prod(array_shape) * 4  # float32 → 4 bytes
    # Create source and destination
    src = np.random.rand(*array_shape).astype(np.float32)
    dst = np.empty_like(src)

    # Worker that copies one slice repeatedly
    def worker(start_idx: int, end_idx: int, iterations: int):
        for _ in range(iterations):
            # each thread copies its own contiguous chunk
            np.copyto(dst.ravel()[start_idx:end_idx],
                      src.ravel()[start_idx:end_idx])

    # Precompute slice boundaries
    count = array_shape[0] * array_shape[1]
    chunk = count // num_threads
    slices = [
        (i * chunk, (i + 1) * chunk if i < num_threads - 1 else count)
        for i in range(num_threads)
    ]

    # Warm‑up
    threads = []
    for start, end in slices:
        t = threading.Thread(target=worker, args=(start, end, warmup_iterations))
        threads.append(t)
        t.start()
    for t in threads:
        t.join()

    # Timed runs
    times = []
    for _ in range(num_iterations):
        threads = []
        t0 = time.perf_counter()
        for start, end in slices:
            t = threading.Thread(target=worker, args=(start, end, 1))
            threads.append(t)
            t.start()
        for t in threads:
            t.join()
        t1 = time.perf_counter()
        times.append(t1 - t0)

    avg_time = sum(times) / len(times)
    bandwidth = size_in_bytes / avg_time / (1024 ** 3)  # GB/s

    print(f"--- Multithreaded ({num_threads} threads) RAM-to-RAM Copy ---")
    print(f"Array size       : {array_shape[0]}×{array_shape[1]} (≈{size_in_bytes/1024**2:.1f} MiB)")
    print(f"Average Copy Time: {avg_time:.6f} s")
    print(f"Effective Bandwidth: {bandwidth:.2f} GB/s")
    return avg_time, bandwidth

if __name__ == "__main__":
    single_threaded_memory_bandwidth()
    multithreaded_memory_bandwidth(num_threads=8)
