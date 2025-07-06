import numpy as np
import time

# Function to measure RAM-to-RAM memory copy bandwidth
def measure_memory_copy_bandwidth(array_shape, num_iterations=10, warmup_iterations=3):
    size_in_bytes = np.prod(array_shape) * 4  # Assuming float32 (4 bytes per element)
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
    
    print(f"--- RAM-to-RAM Copy ---")
    print(f"Average Copy Time: {avg_time:.6f} seconds")
    print(f"Effective Bandwidth: {bandwidth:.2f} GB/s")
    return avg_time, bandwidth

# Main function to run measurements
def memory_bandwidth():
    array_shape = (2048, 2048)  # Example array size (2048x2048)
    num_iterations = 1000  # Number of timed iterations
    warmup_iterations = 100  # Number of warm-up iterations
    
    # Measure RAM-to-RAM memory copy bandwidth
    measure_memory_copy_bandwidth(array_shape, num_iterations, warmup_iterations)

if __name__ == "__main__":
    memory_bandwidth()
