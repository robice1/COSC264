"""
Sender-side simulation of RDT 3.0

"""

# Event constants
# DATA = 0
# ACK = 1
# TIMEOUT = 2

# # State constants - see FSM
# WAIT_DATA0 = 0
# WAIT_ACK0 = 1
# WAIT_DATA1 = 2
# WAIT_ACK1 = 3

# # Status constants
# UNEXPECTED = -1
# DATA_SENT = 0
# ACK_PROCESSED = 1
# RE_SENT = 2

# def rdt_sender(event, state):        
#     """event format: [event_code, seq_num, message]
#         NOTE: seq_num, message are not always present
#        output format: [status, seq_num]
#     """
#     status = -1
#     seq_num = -1
#     event_code = event[0]
#     if event_code == DATA:
#         seq_num = event[1]
#         data = event[2]
#         if state == WAIT_DATA0 and seq_num == 0: #Send DATA0
#             state = WAIT_ACK0
#             seq_num = 0
#             status = DATA_SENT
#         elif state == WAIT_DATA1 and seq_num == 1:
#             state = WAIT_ACK1
#             seq_num = 1
#             status = DATA_SENT
#         else:
#             status, seq_num = UNEXPECTED, UNEXPECTED
#     elif event_code == ACK:
#         seq_num = event[1]
#         if (state == WAIT_ACK0 and seq_num == 0) or (state == WAIT_ACK1 and seq_num == 1):
#             status = ACK_PROCESSED
#             state = WAIT_DATA0 if seq_num == 1 else WAIT_DATA1
#         else:
#             status, seq_num = UNEXPECTED, UNEXPECTED
#     elif event_code == TIMEOUT:
#         if state == WAIT_ACK0 or state == WAIT_DATA1:
#             status = RE_SENT
#             seq_num = 0
#         elif state == WAIT_ACK1 or state == WAIT_DATA0:
#             status = RE_SENT
#             seq_num = 1
#     return state, [status, seq_num]



# def sender_test(event_list):    
#     state = 0
#     action_list = []    
#     for event in event_list:        
#         state, action = rdt_sender(event,state)
#         action_list.append(action)    
#     print(f'{action_list}')


"""
Receiver-side simulation of RDT 3.0

"""

# Status constants
ERROR = -1
ACK = 0

def rdt_receiver(packet):
    """packet: [seq_num, data]
       output: [status, seq_num]
    """
    seq_num, data = packet[0], packet[1]
    if seq_num not in [0, 1]:
        return [ERROR, ERROR]
    else:
        return [ACK, seq_num]

def receiver_test(event_list):    
    action_list = []    
    for event in event_list:        
        action = rdt_receiver(event)
        action_list.append(action)    
    print(f'{action_list}')  

"""
Sender-side simulation of GBN

"""

# Event constants
DATA = 0
ACK = 1
TIMEOUT = 2

# Status constants
ERROR = -1 # unexpected event or window full
DATA_SENT = 0
ACK_PROCESSED = 1
RE_SENT = 2

# Window size
N = 4

def gbn_sender(event, base, next_seq):        
    """event: [event_code, seq_num, data]
       base: seq# of lower window boundary (base)
       output: [status, base, next_seq]
    """
    event_code = event[0]
    if event_code == DATA:
        if next_seq < base + N:
            next_seq += 1
            return [DATA_SENT, base, next_seq]
        else:
            return [ERROR, base, next_seq]
    if event_code == ACK:
        seq_num = event[1]
        if base <= seq_num < next_seq:
            base = seq_num + 1
            return [ACK_PROCESSED, base, next_seq]
        else:
            return [ERROR, base, next_seq]
    if event_code == TIMEOUT:
        return [RE_SENT, base, next_seq]
    return [ERROR, base, next_seq]

def sender_test(event_list):    
    base = 0
    next_seq = 0
    action_list = []    
    
    for event in event_list:        
        action = gbn_sender(event, base, next_seq)
        base = action[1]
        next_seq = action[2]
        action_list.append(action)    
        
    print(f'{action_list}')

"""
Receiver-side simulation of GBN

"""

# Status constants
ERROR = -1
ACK = 0

def gbn_receiver(packet, exp_num):
    """packet: [seq_num, data]
       output: [status, exp_num]
    """
    seq_num = packet[0]
    if seq_num == exp_num:
        status = ACK
        exp_num += 1
    else:
        status = ERROR
    return [status, exp_num]

def receiver_test(packet_list):    
    action_list = []
    exp_num = 1
    for packet in packet_list:        
        action = gbn_receiver(packet, exp_num)
        exp_num = action[1]
        action_list.append(action)    
        
    print(f'{action_list}')  

receiver_test([[1,1]])
receiver_test([[1,1],[2,2]])
receiver_test([[1,1],[2,2],[3,3]])
receiver_test([[0,1]])


