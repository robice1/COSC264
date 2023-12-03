import math

def number_fragments(message_size_bytes, overhead_per_packet_bytes, maximum_n_packet_size_bytes):
    s = message_size_bytes
    o = overhead_per_packet_bytes
    m = maximum_n_packet_size_bytes
    num_frags = math.ceil((s) / (m - o))
    return num_frags

def last_fragment_size(message_size_bytes, overhead_per_packet_bytes, maximum_n_packet_size_bytes):
    s = message_size_bytes
    o = overhead_per_packet_bytes
    m = maximum_n_packet_size_bytes
    last_fragment_size = (s + o) % (m - o) if s % (m - o) != 0 else m
    return last_fragment_size

print(last_fragment_size(10000, 20, 1500))
print(number_fragments(10000, 20, 1500))