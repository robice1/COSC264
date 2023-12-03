"""client.py is a command line application that operates as a TCP client

Author: Robert Ivill, 46012819
"""

import sys
import socket

def build_message(request_type, username, receiver, message):
    fixed_header = (0xAE73).to_bytes(2, 'big')
    if request_type == "read":
        fixed_header += (1).to_bytes(1, 'big') #ID
        fixed_header += len(username).to_bytes(1, 'big') #NameLen
        fixed_header += (0).to_bytes(1, 'big') #ReceiverLen
        fixed_header += (0).to_bytes(1, 'big') #MessageLen
        data = username.encode()
    else: # request_type == 'create'
        fixed_header += (2).to_bytes(1, 'big') #ID
        fixed_header += len(username).to_bytes(1, 'big') #NameLen
        fixed_header += len(receiver).to_bytes(1, 'big')  #ReceiverLen
        fixed_header += len(message).to_bytes(2, 'big')  #MessageLen
        data = username.encode() + receiver.encode() + message.encode()
    request_data = fixed_header + data
    return request_data

def process_response(sock):
    try:
        fixed_header = sock.recv(5)
        if not fixed_header:
            print("Connection closed by the server.")
            sock.close()
            return
    except socket.timeout:
        print("Socket timed out while trying to receive data.")
        sock.close()
        return
    except Exception as e:
        print(f"Process Response Error: {e}")
    magic_no = int.from_bytes(fixed_header[:2], byteorder = 'big')
    print(magic_no == 0xAE73)
    id_val = fixed_header[2]
    print(id_val)
    num_items = fixed_header[3]
    print(num_items)
    messages = fixed_header[4]
    print(messages)
    if magic_no != 0xAE73 or id_val >= 3:
        print("Error: Invalid data")
        return
    for x in range(num_items):
        message_header = sock.recv(3)
        if len(message_header) < 3:
            print("Error: incomplete message header")
            return
        sender_len, message_len = message_header[0], int.from_bytes(message_header[1:], 'big')
        if sender_len < 1 or message_len < 1:
            print("Error: Invalid sender or message length")
            return
        sender_name_data = sock.recv(sender_len)
        message_data = sock.recv(message_len)
        sender_name = sender_name_data.decode()
        message = message_data.decode()
        print(f'Message from {sender_name}: {message}')


def get_receiver():
    while True:
        receiver = input("Enter receiver's name: ")
        if 1 <= len(receiver.encode()) < 255:
            return receiver
        print("Error: Receiver name must be between 1 and 255 bytes. Try again")

def get_message():
    while True:
        message = input("Enter your message: ")
        if 1 <= len(message.encode()) < 65535:
            return message
        print("Error: Message must be between 1 and 65535 bytes. Try again")

def main():
    if len(sys.argv) != 5:
        print("Must be of the form: client.py <IP/Hostname> <Port> <Username> <RequestType>")
        sys.exit(1)
    host, port_str, username, request_type = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]
    try:
        ip = socket.getaddrinfo(host, None)[0][4][0]
    except:
        print("Error: Invalid Hostname or IP")
        sys.exit(1)
    try:
        port = int(port_str)
        if not (1024 <= port <= 64000):
            raise ValueError
    except ValueError:
        print("Error: Invalid port number")
        sys.exit(1)
    if not (1 <= len(username) <= 255):
        print("Error: Username must be between 1 and 255 characters inclusive")
        sys.exit(1)
    if request_type not in ['read', 'create']:
        print("Error: Invalid request type.")
        sys.exit(1)
    receiver = None
    message = None
    if request_type == 'create':
        receiver = get_receiver()
        message = get_message()
    request_data = build_message(request_type, username, receiver, message)
    print(request_data)
    clnt_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        clnt_socket.connect((ip, port))
        clnt_socket.settimeout(1)
        clnt_socket.sendall(request_data)
        if request_type == 'read':
            process_response(clnt_socket)
    except socket.timeout:
        print("Network operation timed out")
        sys.exit(1)
    except Exception as e:
        print(f"Error client.main(): {e}")
    finally:
        clnt_socket.close()

if __name__ == '__main__':
    main()