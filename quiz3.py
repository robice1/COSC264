def connection_setup_delay(cable_length_km, light_speed_kmps, message_length_b, data_rate_bps, processing_time_s):
    d = cable_length_km
    c = light_speed_kmps
    m = message_length_b
    r = data_rate_bps
    p = processing_time_s
    t_prop = d / c
    t_transmission = m / r
    t_processing = p

    t_setup = t_prop + t_transmission + t_processing
    return t_setup * 4

def message_delay(conn_setup_time_s, cable_length_km, light_speed_kmps, message_length_b, data_rate_bps):
    ts = conn_setup_time_s
    d = cable_length_km
    c = light_speed_kmps
    m = message_length_b
    r = data_rate_bps
    delay = ts + 2* d/c + m /r
    return delay
    
    
import math

def total_number_bits(max_user_data_per_packet_b, overhead_per_packet_b, message_length_b):
    s = max_user_data_per_packet_b
    o = overhead_per_packet_b
    m = message_length_b
    n_packets = math.ceil(m / s)
    total_overhead = n_packets * o
    total_bits = m + total_overhead
    return total_bits

def packet_transfer_time(link_length_km, light_speed_kmps, processing_delay_s, data_rate_bps, max_user_data_per_packet_b, overhead_per_packet_b):
    d = link_length_km
    c = light_speed_kmps
    p = processing_delay_s
    r = data_rate_bps
    s = max_user_data_per_packet_b
    o = overhead_per_packet_b
    packet_size = s + o
    
    total_time = 2 * ((s + o) / r + d / c + p)
    return total_time

def total_transfer_time(link_length_km, light_speed_kmps, processing_delay_s, data_rate_bps, max_user_data_per_packet_b, overhead_per_packet_b, message_length_b):
    d = link_length_km
    c = light_speed_kmps
    p = processing_delay_s
    r = data_rate_bps
    s = max_user_data_per_packet_b
    o = overhead_per_packet_b
    m = message_length_b
    n_packets = m / s
    t_prop = d / c
    t_trans = (s + o) / r
    t_total = 2 * t_prop + 2 * p + (n_packets + 1) * t_trans
    return t_total


print(total_transfer_time(10000, 200000, 0.001, 1000000, 1000, 100, 1000000000))