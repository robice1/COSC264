def transmission_delay(packet_length_bytes, rate_mbps):
    r = rate_mbps
    l = packet_length_bytes
    delay = (8 * l / r) / 1000000
    return delay

def total_time(cable_length_km, packet_length_b):
    d = cable_length_km
    l = packet_length_b
    transmission_time = l / 10000000000
    propagation_time = d / 200000
    total_time = transmission_time + propagation_time
    milliseconds = total_time * 1000
    return milliseconds

def queueing_delay(rate_bps, num_packets, packet_length_b):
    r = rate_bps
    n = num_packets
    l = packet_length_b
    delay = n * l / r
    return delay

def average_trials(p_loss):
    trials = 1 / (1-p_loss)
    return trials

def per_from_ber(bit_error_probability, packet_len_b):
    p = bit_error_probability
    l = packet_len_b
    error_probability = 1 - (1 - p) ** l
    return error_probability

def avg_trials_from_ber(bit_error_probability, packet_length_b):
    p = bit_error_probability
    l = packet_length_b
    average_trials = 1 / (1 - p) ** l
    return average_trials

print(f"{avg_trials_from_ber(0.001, 2000):.3f}")
