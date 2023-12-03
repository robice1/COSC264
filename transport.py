def dev_rtt(sample_rtts):
    alpha = 0.125
    beta = 0.25
    est_rtt = sample_rtts[0]
    dev_rtt = 0
    for sample_rtt in sample_rtts:
        est_rtt = (1 - alpha) * est_rtt + alpha * sample_rtt
        dev_rtt = (1 - beta) * dev_rtt + beta * abs(sample_rtt - est_rtt)
    return dev_rtt

def timeout_interval(sample_rtts):
    alpha = 0.125
    beta = 0.25
    est_rtt = sample_rtts[0]
    dev_rtt = 0
    for sample_rtt in sample_rtts:
        est_rtt = (1 - alpha) * est_rtt + alpha * sample_rtt
        dev_rtt = (1 - beta) * dev_rtt + beta * abs(sample_rtt - est_rtt)
    timeout = est_rtt + 4 * dev_rtt
    return timeout

def num_rtt(initial, threshold):
    cwnd = initial
    num_round_trips = 0
    while cwnd <= threshold:
        cwnd *= 2
        num_round_trips += 1
    return num_round_trips

print(num_rtt(2, 16))