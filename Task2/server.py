#Aboud Fialah       ID: 1220216      Section: 2 
#Alaa Faraj         ID: 1220217      Section: 2
#Adnan Odeh         ID: 1220218      Section:

import socket
from config import HOST, PORT
import os

def run_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(2)
    
    while True:
        conn, add = server_socket.accept()

        data = conn.recv(1024)
        
        with open("request.txt", "w") as file_to_write:
            file_to_write.write(data.decode('utf-8'))
        
        print(f"Data Received -> {data.decode('utf-8')}")
        
        with open("request.txt", "r") as r:
            for line in r:
                if "filename" in line:
                    input_value = line.split("=")
                    
                    if input_value[1].strip() == '':
                        body = "<html><body><h1>Empty Input</h1></body></html>"
                        response_empty = f"""HTTP/1.1 200 OK\r
Content-Type: text/html\r
Content-Length: {len(body.encode('utf-8'))}\r
\r
{body}"""
                        conn.sendall(response_empty.encode('utf-8'))
                        break
                    
                    else:
                        file_path = os.path.join("media", input_value[1].strip())
                        if os.path.isfile(file_path):
                            body_img = f"""<html>
                            <body>
                            <h1>Computer Networks</h1>
                            <img src="/mnt/c/Socket-Based-WebServer-Game/Socket-Based-WebServer-Game/Task2/media/net.jpeg" alt="Hello">
                            </body>
                            </html>"""

                            response_file_exist = f"""HTTP/1.1 200 OK\r
Content-Type: image/jpeg\r
\r
{open("media/net.jpeg", "rb").read()}"""

                            conn.sendall(response_file_exist.encode('utf-8'))
                            
        conn.close()


    
run_server()