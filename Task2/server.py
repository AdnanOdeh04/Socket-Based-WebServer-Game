#Aboud Fialah       ID: 1220216      Section: 2 
#Alaa Faraj         ID: 1220217      Section: 2
#Adnan Odeh         ID: 1220218      Section:

import socket
from config import HOST, PORT

def run_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)       #this line create TCP socket
    server_socket.bind((HOST,PORT))     #bind -> sets the PORT number, and the HOST IP address 
    server_socket.listen(2)             #listen -> put the socket on listening mode, 1 -> referes to the maximum number of incoming connection requests

