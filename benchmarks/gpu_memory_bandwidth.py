import numpy as np
import cupy as cp
import time

# Function to measure Host-to-Device (CPU-to-GPU) transfer bandwidth
def measure_host_to_device_bandwidth(array_shape, num_iterations=10, warmup_iterations=3):
    size_in_bytes = np.prod(array_shape) * 4  # Assuming float32 (4 bytes per element)
    host_array = cp.random.random(array_shape).astype(cp.float32).get()  # NumPy array
    device_array = cp.empty(array_shape, dtype=cp.float32)  # GPU array

    # Warm-up phase
    for _ in range(warmup_iterations):
        device_array.set(host_array)
    
    # Timed runs
    times = []
    for _ in range(num_iterations):
        start = time.perf_counter()
        device_array.set(host_array)
        cp.cuda.Stream.null.synchronize()  # Ensure transfer completes
        end = time.perf_counter()
        times.append(end - start)
    
    avg_time = sum(times) / len(times)
    bandwidth = size_in_bytes / avg_time / (1024**3)  # Convert to GB/s
    
    print(f"--- Host-to-Device Transfer ---")
    print(f"Average Host-to-Device Transfer Time: {avg_time:.6f} seconds")
    print(f"Effective Bandwidth: {bandwidth:.2f} GB/s")
    return avg_time, bandwidth

# Function to measure Device-to-Device (GPU memory) transfer bandwidth
def measure_device_to_device_bandwidth(array_shape, num_iterations=10, warmup_iterations=3):
    size_in_bytes = np.prod(array_shape) * 4  # Assuming float32 (4 bytes per element)
    gpu_array_src = cp.random.random(array_shape).astype(cp.float32)
    gpu_array_dst = cp.empty_like(gpu_array_src)

    # Warm-up phase
    for _ in range(warmup_iterations):
        cp.copyto(gpu_array_dst, gpu_array_src)
    
    # Timed runs
    times = []
    for _ in range(num_iterations):
        start = time.perf_counter()
        cp.copyto(gpu_array_dst, gpu_array_src)
        cp.cuda.Stream.null.synchronize()  # Ensure transfer completes
        end = time.perf_counter()
        times.append(end - start)
    
    avg_time = sum(times) / len(times)
    bandwidth = size_in_bytes / avg_time / (1024**3)  # Convert to GB/s
    
    print(f"--- Device-to-Device Transfer ---")
    print(f"Average Device-to-Device Transfer Time: {avg_time:.6f} seconds")
    print(f"Effective Bandwidth: {bandwidth:.2f} GB/s")
    return avg_time, bandwidth

# Main function to run all measurements
def main():
    array_shape = (2048, 2048)  # Example array size (2048x2048)
    num_iterations = 1000  # Number of timed iterations
    warmup_iterations = 100  # Number of warm-up iterations
    
    # Measure Host-to-Device (CPU-to-GPU) transfer bandwidth
    measure_host_to_device_bandwidth(array_shape, num_iterations, warmup_iterations)
    
    # Measure Device-to-Device (GPU memory) transfer bandwidth
    measure_device_to_device_bandwidth(array_shape, num_iterations, warmup_iterations)

if __name__ == "__main__":
    main()
