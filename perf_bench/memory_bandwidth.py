import numpy as np
import time
from typing import Tuple

# Function to measure RAM-to-RAM memory copy bandwidth
def memory_bandwidth(
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
    print(f"Average Copy Time: {avg_time:.6f} seconds")
    print(f"Effective Bandwidth: {bandwidth:.2f} GB/s")
    return avg_time, bandwidth

if __name__ == "__main__":
    memory_bandwidth()
