def theoretical_memory_bandwidth(
        mem_freq_hz: float,
        num_channels: int = 2,
        bus_width_bits: int = 64
) -> float:
    return mem_freq_hz * bus_width_bits//8 * num_channels 

if __name__ == "__main__":
    bandwidth = theoretical_memory_bandwidth(2666*1e6, 2) 
    print(f'{bandwidth * 1e-9} GiB/s')
