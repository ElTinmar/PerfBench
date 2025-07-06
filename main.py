from perf_bench import cpu_linear_algebra, single_threaded_memory_bandwidth, disk_io_benchmark

if __name__ == "__main__":

    print('Running CPU benchmark')
    print(60*"=" + "\n")
    cpu_linear_algebra()

    print('Running Disk IO benchmark')
    print(60*"=" + "\n")
    disk_io_benchmark()

    print('Running memory benchmark')
    print(60*"=" + "\n")
    single_threaded_memory_bandwidth()