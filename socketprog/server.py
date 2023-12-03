"""server.py allows client.py to send and read messages to and from other
clients. The client and the server will communicate through
stream / TCP sockets, exchanging both control and actual message data.

Author: Robert Ivill, 46012819
"""
import socket
import sys

messages = {}

def start_server(port):
    srv_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        srv_socket.bind(('0.0.0.0', port))
    except socket.error as e:
        print(f'Bind failed with error code {e}')
        sys.exit(1)
    srv_socket.listen()
    print(f'Server listening on port {port}')
   
    while True:
        clnt_socket = None
        try:
            clnt_socket, address = srv_socket.accept()
            clnt_socket.settimeout(1)
            print(f'Connection established with {address}')
            handle_message_request(clnt_socket)
        except socket.timeout:
            print("Network operation timed out.")
        except Exception as e:
            print(f"Error start server: {e}")
        finally:
            if clnt_socket:
                clnt_socket.close()

def unpack_fixed_header(fixed_header):
    if len(fixed_header) < 5:
        raise ValueError("Insufficient data for the fixed header")
    magic_no = int.from_bytes(fixed_header[:2], byteorder = 'big')
    print("unpack")
    print(magic_no)
    id_val = fixed_header[2]
    print(id_val)
    name_len = fixed_header[3]
    print(name_len)
    receiver_len = fixed_header[4]
    print(receiver_len)
    return magic_no, id_val, name_len, receiver_len

def handle_message_request(clnt_socket):
    print(clnt_socket.recv(5))
    try:
        try:
            fixed_header = clnt_socket.recv(5)
        except Exception as e:
            print(f"Error reading fixed header: {e}")
            return
        print(fixed_header + " fixed header srv")
        magic_no, id_val, name_len, receiver_len = unpack_fixed_header(fixed_header)
       
        if magic_no != 0xAE73:
            raise ValueError("Invalid Magic Number")
        if id_val not in [1, 2]:
            raise ValueError("Invalid ID")
        if name_len < 1:
            raise ValueError("Invalid Name Length")
        if id_val == 1:
            message_len = 0
        else:
            message_len_data = clnt_socket.recv(2)
            message_len = int.from_bytes(message_len_data, byteorder = 'big')
        data_len = name_len + receiver_len + message_len
        data = clnt_socket.recv(data_len)
        if len(data) != data_len:
            raise ValueError("Expected data length does not equal actual data length")
        name = data[:name_len].decode()
        receiver = data[name_len: (name_len + receiver_len)].decode()
        message = data[receiver_len : (receiver_len + message_len)].decode()
        if id_val == 1:
            messages_for_name = messages.get(name, [])
            for message in messages_for_name:
                clnt_socket.sendall(message.encode())
        elif id_val == 2:
            if receiver not in messages:
                messages[receiver] = []
            messages[receiver].append(f"Message from {name}: {message}")
            clnt_socket.sendall("Message stored successfully.".encode())
    
    except ValueError as e:
        print(f'Handle Message Request Error: {e}')
        error_response = f"Error: {e}".encode()
        clnt_socket.sendall(error_response)
        clnt_socket.close()


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: server.py <port>")
        sys.exit(1)
    port = int(sys.argv[1])
    start_server(port)