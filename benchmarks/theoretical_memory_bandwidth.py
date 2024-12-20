mem_freq_hz = 2666*1e6
num_channels = 2
bus_width_bits = 64
theoretical_mem_bandwidth = mem_freq_hz * bus_width_bits//8 * num_channels 
print(f'{theoretical_mem_bandwidth * 1e-9} GiB/s')