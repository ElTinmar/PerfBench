from benchmarks import cpu_linear_algebra, memory_bandwidth, disk_io_benchmark

if __name__ == "__main__":
    cpu_linear_algebra.main()
    disk_io_benchmark.main()
    memory_bandwidth.main()