import math

def number_fdma_channels(b_hz, g_hz, u_hz):
    n = (b_hz - g_hz) / (u_hz + g_hz)
    return math.floor(n)


def number_tdma_users(s_s, g_s, u_s):
    return math.floor((s_s + g_s) / (u_s + g_s))

def p_persistent_csma_collision_probability(p):
    return p / (2 - p)

def p_persistent_csma_access_delay(p):
    return  (1 - p) / p

def aggregate_throughput(n):
    return n * 10
