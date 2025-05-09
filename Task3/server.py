import socket
import time
import threading
from config import SERVER_HOST, TCP_PORT

create_lock = threading.Lock()  #For safer threading (To avoid the race conditions)
Max_Player = 4
Min_Player = 2
Players = {}
Player_Existance = 0
time_limit = 30  #Seconds


def accept_client(conn, add):
    try:
        conn.sendall("Welcome to the Game, Enter Join <username>\r\n".encode())
        while True:
            data = conn.recv(1024).decode().strip()
            parts = data.split()
            if len(parts) == 2 and parts[0].lower() == "join":
                username = parts[1]
                # with create_lock:
                if username not in Players and len(Players) < Max_Player:
                    Players[username] = conn
                    number_players = len(Players)
                    conn.sendall(f"Player with username {username} Added Successfully!\r\n".encode())
                    start_time = time.time()
                    if Max_Player > len(Players) > Min_Player:
                        conn.sendall(f"Waiting Time of {time_limit} to Start the Game.......\r\n".encode())
                        while time.time() - start_time <= time_limit:
                            if len(Players) > number_players:
                                number_players = len(Players)
                                start_time = time.time()
                                conn.sendall(f"New Player With username {list(Players.keys())[-1]} Has Joined The Game!\r\n".encode())
                                conn.sendall(f"Waiting Time of {time_limit} to Start the Game.......\r\n".encode())
                                continue
                    if len(Players) == 1:
                        conn.sendall(f"Minimum Players to Play the game is {Min_Player}\r\n".encode())
                        continue
                    conn.sendall("StartingGame\r\n".encode())
                else:
                    if username in Players:
                        conn.sendall("This username already taken!\r\n".encode())
                    else:
                        conn.sendall("Max Number of Players Reached!\r\n".encode())
                        return
            else:
                conn.sendall("Invalid format. Use: JOIN <username>\r\n".encode())
    except Exception as e:
        print(f"Closing the server due to an error: {e}")
        conn.close()


def tcp_connection():
    connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connection.bind((SERVER_HOST, TCP_PORT))
    connection.listen()
    print(f"Server started at {SERVER_HOST} and at TCP Port -> {TCP_PORT}")

    while True:
        conn, addr = connection.accept()
        threading.Thread(target=accept_client, args=(conn, addr)).start()


tcp_connection()
