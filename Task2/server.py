import socket
from config import HOST, PORT
import os
from urllib.parse import parse_qs

def run_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(2)
    
    print(f"Server listening on {HOST}:{PORT}")
    
    while True:
        conn, add = server_socket.accept()

        data = conn.recv(4096)
        request_text = data.decode('utf-8')

        header, body = request_text.split('\r\n\r\n', 1)
        
        if "POST" in header:
            form_data = parse_qs(body)
            file_type = form_data.get('type', [None])[0]
            file_name = form_data.get('filename', [None])[0]
            
            print(f"Received file type: {file_type}")
            print(f"Received file name: {file_name}")
            
            response = "HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n"
            response += "<html><body><h1>Form data received</h1></body></html>"
            conn.send(response.encode('utf-8'))

        conn.close()

run_server()
