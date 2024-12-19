import numpy as np
import time

# Function to perform matrix multiplication and measure time
def benchmark_matrix_multiplication(matrix_size, num_iterations=10, warmup_iterations=3):
    A = np.random.rand(matrix_size, matrix_size)
    B = np.random.rand(matrix_size, matrix_size)
    
    # Warm-up phase
    for _ in range(warmup_iterations):
        np.dot(A, B)
    
    # Timed runs
    times = []
    for _ in range(num_iterations):
        start = time.perf_counter()
        np.dot(A, B)
        end = time.perf_counter()
        times.append(end - start)
    
    avg_time = sum(times) / len(times)
    gflops = (2 * matrix_size**3) / (avg_time * 1e9)  # GFLOP/s (2 operations per element in multiplication)
    
    print(f"--- Matrix Multiplication (size {matrix_size}x{matrix_size}) ---")
    print(f"Average Time: {avg_time:.6f} seconds")
    print(f"Performance: {gflops:.2f} GFLOP/s")
    return avg_time, gflops

# Function to benchmark matrix inversion
def benchmark_matrix_inversion(matrix_size, num_iterations=10, warmup_iterations=3):
    A = np.random.rand(matrix_size, matrix_size)
    
    # Warm-up phase
    for _ in range(warmup_iterations):
        np.linalg.inv(A)
    
    # Timed runs
    times = []
    for _ in range(num_iterations):
        start = time.perf_counter()
        np.linalg.inv(A)
        end = time.perf_counter()
        times.append(end - start)
    
    avg_time = sum(times) / len(times)
    gflops = (1 / 3) * matrix_size**3 / (avg_time * 1e9)  # Rough estimate of GFLOP/s for inversion
    
    print(f"--- Matrix Inversion (size {matrix_size}x{matrix_size}) ---")
    print(f"Average Time: {avg_time:.6f} seconds")
    print(f"Performance: {gflops:.2f} GFLOP/s")
    return avg_time, gflops

# Function to benchmark solving linear systems (Ax = b)
def benchmark_linear_system(matrix_size, num_iterations=10, warmup_iterations=3):
    A = np.random.rand(matrix_size, matrix_size)
    b = np.random.rand(matrix_size)
    
    # Warm-up phase
    for _ in range(warmup_iterations):
        np.linalg.solve(A, b)
    
    # Timed runs
    times = []
    for _ in range(num_iterations):
        start = time.perf_counter()
        np.linalg.solve(A, b)
        end = time.perf_counter()
        times.append(end - start)
    
    avg_time = sum(times) / len(times)
    gflops = (2 * matrix_size**3) / (avg_time * 1e9)  # Approximation for solving linear systems
    
    print(f"--- Linear System Solve (size {matrix_size}x{matrix_size}) ---")
    print(f"Average Time: {avg_time:.6f} seconds")
    print(f"Performance: {gflops:.2f} GFLOP/s")
    return avg_time, gflops

# Main function to run all benchmarks
def main():
    matrix_size = 2048  # Example matrix size (1024x1024)
    num_iterations = 100  # Number of timed iterations
    warmup_iterations = 10  # Number of warm-up iterations
    
    # Run benchmarks with warmup iterations
    benchmark_matrix_multiplication(matrix_size, num_iterations, warmup_iterations)
    benchmark_matrix_inversion(matrix_size, num_iterations, warmup_iterations)
    benchmark_linear_system(matrix_size, num_iterations, warmup_iterations)

if __name__ == "__main__":
    main()
