import socket
from config import HOST, PORT


def create_socket_connection():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(("localhost", PORT))
    
    
    while True:
        data = input()
        
        client_socket.sendall(data.encode())
    
    client_socket.close()
    
create_socket_connection()