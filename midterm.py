def packet_error_probability(packet_length_b, bit_error_probability):
    b = packet_length_b
    p = bit_error_probability
    prob = 1 - (1 - p) ** b
    return prob

def two_wrong_bits(packet_length_b, bit_error_probability):
    b = packet_length_b
    p = bit_error_probability
    p_0 = (1 - p) ** b
    p_1 = b * p * (1-p) ** (b-1)
    p_2 = 1 - p_1 - p_0
    return p_2

def connection_setup_delay(num_switches, cable_length_km, light_speed_kmps, data_rate_bps, request_length_b, response_length_b, processing_time_s):
    n      = num_switches
    k      = cable_length_km
    c      = light_speed_kmps
    r      = data_rate_bps
    m_req  = request_length_b
    m_resp = response_length_b
    p      = processing_time_s
    prop_delay = n * k / c
    trans_delay_req = n * m_req / r
    trans_delay_resp = n * m_resp / r
    process_delay = 2 * n * p + 2 * p
    total_delay = 2 * prop_delay + trans_delay_req + trans_delay_resp + process_delay
    return total_delay

def backoff(num_collisions):
    k = min(num_collisions, 10)
    return (2 ** k) - 1

def collision_probability(num_slots):
    return (1 / num_slots)

import math

def min_packet_length(cable_length_km, light_speed_kmps, data_rate_bps):
    k = cable_length_km
    c = light_speed_kmps
    r = data_rate_bps
    delay = k / c
    L = 2 * delay * r
    return math.ceil(L)

string = ""

from itertools import combinations

# Define your set
my_set = {'v', 'w', 'x', 'y', 'z'}

# Find all 3-combinations
combinations_3 = list(combinations(my_set, 3))

# Print the 3-combinations
for combo in combinations_3:
    string += f"{set(combo)}" + "\n"

print(string.replace("'", ""))