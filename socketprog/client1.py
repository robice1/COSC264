import socket
import sys
import struct

def main():
    if len(sys.argv) != 5:
        print("Usage: client.py <host> <port> <user_name> <request_type>")
        sys.exit(1)
    
    host = sys.argv[1]
    try:
        port = int(sys.argv[2])
    except ValueError:
        print("Error: port number must be an integer")
        sys.exit(1)
    username = sys.argv[3]
    request_type = sys.argv[4]
    if request_type not in ['create', 'read']:
        print("Error: request type must be 'read' or create'")
        sys.exit(1)
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            client_socket.connect((host, port))
            if request_type == 'read':
                send_read_request(client_socket, username)
                receive_message_response(client_socket)
            else:
                send_create_request(client_socket, username)
    except Exception as e:
        print(f"Client Main Error: {e}")

def send_read_request(client_socket, username):
    name_len = len(username)
    header = struct.pack("!HBBBH", 0xAE73, 1, name_len, 0, 0)
    client_socket.sendall(header + username.encode())
    print("Sent read request")

def send_create_request(client_socket, username):
    name_len = len(username)
    receiver_name = input("Enter recipient's name: ").strip()
    while not (0 < len(receiver_name) < 255):
        print("Receiver name must be between 1 and 255 characters.")
        receiver_name = input("Enter receiver's name: ").strip()
    receiver_len = len(receiver_name)
    message_content = input(f"Enter your message to {receiver_name}: ")
    while not (0 < len(message_content) < 65535):
        print("Message must be between 1 and 65535 characters.")
        message_content = input("Enter your message: ")
    message_len = len(message_content)
    header = struct.pack('!HBBBH', 0xAE73, 2, name_len, receiver_len, message_len)
    client_socket.sendall(header + username.encode() + receiver_name.encode() + message_content.encode())
    print("Sent create request")

def receive_message_response(client_socket):
    header_data = client_socket.recv(8)
    if len(header_data) != 8:
        print("Error: Invalid MessageResponse header length")
        return
    magic_no, msg_id, num_msgs, more_msgs = struct.unpack('!HBBI', header_data)
    if magic_no != 0xAE73 or msg_id != 3:
        print("Error: Invalid MessageResponse header")
        return
    for _ in range(num_msgs):
        msg_header_data = client_socket.recv(3)
        sender_len, content_len = struct.unpack('!BH', msg_header_data)
        sender_data = client_socket.recv(sender_len)
        content_data = client_socket.recv(content_len)
        sender = sender_data.decode()
        content = content_data.decode()
        print(f"Message from {sender}: {content}")
    if more_msgs:
        print("More messages available. Rerun the client to view.")

if __name__ == '__main__':
    main()