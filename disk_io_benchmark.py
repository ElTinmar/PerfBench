import os
import subprocess
import re

# File name for benchmarking
FILE_NAME = "disk_benchmark_file.dd"
BLOCK_SIZES = [4 * 1024, 64 * 1024, 512 * 1024, 1 * 1024 * 1024]  # Varying buffer sizes
FILE_SIZE = 1 * 1024**3

def run_dd_benchmark(input_file, output_file, block_size, file_size):
    """
    Run a `dd` command to benchmark sequential read or write
    """
    counts = file_size // block_size
    command = [
        'dd',
        f'if={input_file}',
        f'of={output_file}',
        f'bs={block_size}',  # Block size
        f'count={counts}',  # Number of blocks to read/write
        'oflag=dsync'  # Ensure data is synced to disk
    ]
            
    # Execute the dd command and measure throughput
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    
    if process.returncode != 0:
        print(f"Error running dd command: {stderr.decode()}")
        return None, None

    output = stderr.decode()

    # Use regex to find throughput in bytes/sec, MB/s, GB/s, etc.
    match = re.search(r'(\d+(?:[\.,]\d+)?)\s*(bytes|KB|MB|GB)/s', output)
    if match:
        value_str = match.group(1)  # Numeric value as string
        
        # Replace comma with a dot to ensure we parse it correctly
        value_str = value_str.replace(',', '.')
        
        value = float(value_str)  # Convert the string to a float
        unit = match.group(2).lower()  # Unit (e.g., MB or GB)
        
        # Convert to MB/s
        if unit == 'bytes':
            throughput = value / (1024 * 1024)  # Convert bytes to MB
        elif unit == 'kb':
            throughput = value / 1024  # Convert KB to MB
        elif unit == 'gb':
            throughput = value * 1024  # Convert GB to MB
        else:  # MB/s
            throughput = value
    else:
        throughput = 0
        
    return throughput

def display_table(block_sizes, write_throughputs, read_throughputs):
    """Display throughput results in a table format."""
    print(f"{'Block Size':<15}{'Write Throughput (MB/s)':<25}{'Read Throughput (MB/s)'}")
    print("="*60)
    
    for i, block_size in enumerate(block_sizes):
        print(f"{block_size:<15}{write_throughputs[i]:<25.2f}{read_throughputs[i]:.2f}")

def run_benchmarks():
    
    # Sequential Write Benchmark
    write_throughputs = []
    for block_size in BLOCK_SIZES:
        write_throughputs.append(run_dd_benchmark("/dev/urandom", FILE_NAME, block_size, FILE_SIZE))  

    # Sequential Read Benchmark
    read_throughputs = []
    for block_size in BLOCK_SIZES:
        read_throughputs.append(run_dd_benchmark(FILE_NAME, "/dev/null", block_size, FILE_SIZE))

    # display results
    display_table(BLOCK_SIZES, write_throughputs, read_throughputs)

    # Clean up the file after benchmarking
    if os.path.exists(FILE_NAME):
        os.remove(FILE_NAME)
        
    print("Benchmark complete and file cleaned up.")

if __name__ == "__main__":
    run_benchmarks()
