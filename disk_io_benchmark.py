import os
import time
import random
import string
import subprocess
import matplotlib.pyplot as plt

# File name for benchmarking
FILE_NAME = "disk_benchmark_file.txt"

# Time duration for each benchmark run (in seconds)
BENCHMARK_DURATION = 5  # 1 minute

# Generate a random string for writing
def generate_random_data(size):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=size))

# Function to flush the OS cache (Linux/Unix based systems)
def flush_cache():
    subprocess.run(['sync'])  # This ensures all data is written to disk
    # Optionally, you can clear pagecache, dentries, and inodes on Linux
    subprocess.run(['echo', '3', '>', '/proc/sys/vm/drop_caches'])

# Sequential write benchmark (run for 1 minute and report throughput)
def benchmark_sequential_write(file_name, buffer_size):
    data = generate_random_data(buffer_size)
    start_time = time.perf_counter()
    times = []
    throughputs = []
    
    with open(file_name, 'wb') as f:
        while time.perf_counter() - start_time < BENCHMARK_DURATION:
            before_time = time.perf_counter()
            f.write(data.encode('utf-8'))  # Write buffer to file
            elapsed_time = time.perf_counter() - before_time
            
            throughput = buffer_size / elapsed_time / (1024 * 1024)  # MB/s
            times.append(times[-1] + elapsed_time)
            throughputs.append(throughput)
    
    print(f"Sequential Write (Final) - Final Throughput: {throughput:.2f} MB/s")
    
    # Return throughput over time
    return times, throughputs

# Sequential read benchmark (run for 1 minute and report throughput)
def benchmark_sequential_read(file_name, buffer_size):
    start_time = time.perf_counter()
    times = []
    throughputs = []
    
    with open(file_name, 'rb') as f:
        while time.perf_counter() - start_time < BENCHMARK_DURATION:
            before_time = time.perf_counter()
            f.read(buffer_size)  # Read the data in chunks
            elapsed_time = time.perf_counter() - before_time
            
            throughput = buffer_size / elapsed_time / (1024 * 1024)  # MB/s
            times.append(times[-1] + elapsed_time)
            throughputs.append(throughput)
    
    print(f"Sequential Read (Final) - Final Throughput: {throughput:.2f} MB/s")
    
    # Return throughput over time
    return times, throughputs

# Random write benchmark (run for 1 minute and report throughput)
def benchmark_random_write(file_name, file_size, buffer_size):
    data = generate_random_data(buffer_size)
    start_time = time.perf_counter()
    times = []
    throughputs = []
    
    with open(file_name, 'r+b') as f:
        while time.perf_counter() - start_time < BENCHMARK_DURATION:
            position = random.randint(0, file_size - buffer_size)

            before_time = time.perf_counter()
            f.seek(position)
            f.write(data.encode('utf-8'))  # Write buffer at random position
            elapsed_time = time.perf_counter() - before_time
                        
            throughput = buffer_size / elapsed_time / (1024 * 1024)  # MB/s
            times.append(times[-1] + elapsed_time)
            throughputs.append(throughput)
    
    print(f"Random Write (Final) - Final Throughput: {throughput:.2f} MB/s")
    
    # Return throughput over time
    return times, throughputs

# Random read benchmark (run for 1 minute and report throughput)
def benchmark_random_read(file_name, file_size, buffer_size):
    start_time = time.perf_counter()
    times = []
    throughputs = []
    
    with open(file_name, 'rb') as f:
        while time.perf_counter() - start_time < BENCHMARK_DURATION:
            position = random.randint(0, file_size - buffer_size)

            before_time = time.perf_counter()
            f.seek(position)
            f.read(buffer_size)  # Read data from random position
            elapsed_time = time.perf_counter() - before_time
            
            throughput = buffer_size / elapsed_time / (1024 * 1024)  # MB/s
            times.append(times[-1] + elapsed_time)
            throughputs.append(throughput)

    print(f"Random Read (Final) - Final Throughput: {throughput:.2f} MB/s")
    
    # Return throughput over time
    return times, throughputs

# Function to run all benchmarks with increasing buffer sizes and save plot as PNG
def run_disk_io_benchmarks(file_size, buffer_sizes):
    print("Running disk I/O benchmark...")

    # Create a figure with multiple subplots (one for each benchmark type)
    fig, axes = plt.subplots(len(buffer_sizes), 4, figsize=(15, 12), sharex=True, sharey=True)
    
    for i, buffer_size in enumerate(buffer_sizes):
        print(f"Running benchmarks for buffer size: {buffer_size} bytes")
        
        # Sequential write test
        seq_write_times, seq_write_throughputs = benchmark_sequential_write(FILE_NAME, buffer_size)
        axes[i, 0].plot(seq_write_times, seq_write_throughputs, label=f'Seq Write {buffer_size}B')
        axes[i, 0].set_title(f'Seq Write - {buffer_size}B')
        flush_cache()

        # Sequential read test
        seq_read_times, seq_read_throughputs = benchmark_sequential_read(FILE_NAME, buffer_size)
        axes[i, 1].plot(seq_read_times, seq_read_throughputs, label=f'Seq Read {buffer_size}B')
        axes[i, 1].set_title(f'Seq Read - {buffer_size}B')
        flush_cache()
        
        # Random write test
        rand_write_times, rand_write_throughputs = benchmark_random_write(FILE_NAME, file_size, buffer_size)
        axes[i, 2].plot(rand_write_times, rand_write_throughputs, label=f'Rand Write {buffer_size}B')
        axes[i, 2].set_title(f'Rand Write - {buffer_size}B')
        flush_cache()

        # Random read test
        rand_read_times, rand_read_throughputs = benchmark_random_read(FILE_NAME, file_size, buffer_size)
        axes[i, 3].plot(rand_read_times, rand_read_throughputs, label=f'Rand Read {buffer_size}B')
        axes[i, 3].set_title(f'Rand Read - {buffer_size}B')
        flush_cache()

    # Clean up the file after benchmarking
    if os.path.exists(FILE_NAME):
        os.remove(FILE_NAME)
    
    print("Benchmark complete. Cleaning up and saving plot.")
    # Set common axis labels
    for ax in axes.flat:
        ax.set(xlabel='Time (s)', ylabel='Throughput (MB/s)')
        ax.grid(True)
    
    # Adjust layout
    plt.tight_layout()

    # Save plot as PNG
    plt.savefig('disk_io_benchmark.png')
    plt.close()
    print("Plot saved as 'disk_io_benchmark.png'.")

# Estimate the file size based on the buffer size and duration
FILE_SIZE = 512 * 1024 * 1024  # 512 MB file size
BUFFER_SIZES = [4 * 1024, 64 * 1024, 512 * 1024, 1 * 1024 * 1024, 4 * 1024 * 1024]  # Varying buffer sizes

# Run the benchmark
if __name__ == "__main__":
    run_disk_io_benchmarks(FILE_SIZE, BUFFER_SIZES)
