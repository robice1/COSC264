import socket
import sys
import struct

messages = {}

def start_server(port):
    if not 1024 <= port <= 64000:
        print("Error: Port number should be between 1024 and 64000")
        sys.exit(1)
    
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        server_socket.bind(('0.0.0.0', port))
    except socket.error as e:
        print(f"Bind failed with error: {e}")
        sys.exit(1)
    
    try:
        server_socket.listen()
    except socket.error as e:
        print(f"Listen failed with error: {e}")
        server_socket.close()
        sys.exit(1)
    print(f"Listening on port {port}")
    while True:
        try:
            client_socket, address = server_socket.accept()
            print(f"Connection established with {address}")
            handle_message_request(client_socket)
        except Exception as e:
            print(f"Connection Error: {e}")
        finally:
            client_socket.close()

def handle_message_request(client_socket):
    header_data = client_socket.recv(7)
    if len(header_data) != 7:
        print("Error: Invalid MessageRequest length for header")
        return
    magic_no, msg_id, name_len, receiver_len, message_len = struct.unpack('!HBBBH', header_data)
    if magic_no != 0xAE73 or msg_id not in [1, 2] or name_len < 1:
        print("Error: Invalid MessageRequest header")
        return
    if (msg_id == 1 and (receiver_len != 0 or message_len != 0)) or (msg_id == 2 and (receiver_len < 1 or message_len < 1)):
        print("Error: Invalid MessageRequest for ID type")
        return
    data_len = name_len + receiver_len + message_len
    message_content_data = client_socket.recv(data_len)
    if len(message_content_data) != data_len:
        print("Error: Invalid MessageRequest length for content")
        return
    name = message_content_data[:name_len].decode()
    if msg_id == 1: # read
        send_message_response(client_socket, name)
    elif msg_id == 2: # create
        receiver_name = message_content_data[name_len:name_len + receiver_len].decode()
        message_content = message_content_data[name_len + receiver_len:].decode()
        store_message(name, receiver_name, message_content)

def store_message(sender_name, receiver_name, message_content):
    if receiver_name not in messages:
        messages[receiver_name] = []
    messages[receiver_name].append((sender_name, message_content))
    print(f"Stored message: To {receiver_name}, {message_content}, From {sender_name}")

def send_message_response(client_socket, name):
    msgs = messages.get(name, [])
    num_items = len(msgs)
    more_msgs = 1 if num_items > 255 else 0
    num_items = min(255, num_items)
    header = struct.pack("!HBBI", 0xAE73, 3, num_items, more_msgs)
    client_socket.sendall(header)
    for i in range(num_items):
        sender, content = msgs[i]
        sender_len = len(sender)
        content_len = len(content)
        msg_header = struct.pack('!BH', sender_len, content_len)
        try:
            client_socket.sendall(msg_header + sender.encode() + content.encode())
        except socket.error:
            print("Error sending msg")
            client_socket.close()
    messages[name] = messages[name][num_items:]

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: server.py <port>")
        sys.exit(1)
    port = int(sys.argv[1])
    start_server(port)