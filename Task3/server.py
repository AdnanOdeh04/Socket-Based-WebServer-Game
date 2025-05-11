import socket
import time
import threading
from config import SERVER_HOST, TCP_PORT, UDP_PORT
import random

create_lock = threading.Lock()  #For safer threading (To avoid the race conditions)
Max_Player = 4
Min_Player = 2
Players = {}
Player_Existance = 0
time_limit = 30  #Seconds
game_duration = 60
max_number = 100
round_limit = 10
game_over = False

def game_setup(tcp_conn, tcp_add):
    winner = 0
    winner_name = ""
    udp_connection = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_connection.bind((SERVER_HOST, UDP_PORT))
    secret_guess = random.randint(1, 100)
    start_Game = time.time()
    global game_over
    game_over = False
    while not game_over:
        if time.time() - start_Game > 60:
            for i in Players:
                udp_connection.sendto("Time's up! No one guessed correctly.".encode(), Players[i])
                udp_connection.sendto("finish".encode(), Players[i])
            break

        data, add = udp_connection.recvfrom(1024)
        number_guessed = data.decode().strip()
        if not number_guessed.isdigit():
            udp_connection.sendto("Invalid input".encode(), add)
            continue
        guess = int(number_guessed)
        if guess == secret_guess:
            udp_connection.sendto("Correct!".encode(), add)
            for i in Players:
                if Players[i] == add:
                    winner_name = i
                    break
            try:
                for connection in Players:
                    Players[connection].sendall("winner\r\n".encode())
                    Players[connection].sendall("We Have a correct Guess!\r\n".encode())
                    Players[connection].sendall(f"Game finished! {winner_name} is the winner!\r\n".encode())
                    Players[connection].sendall("finish\r\n".encode())
                    game_over = True
                break
            except Exception as e:
                print(e)
        elif guess < secret_guess:
            udp_connection.sendto("Higher!".encode(), add)

        else:
            udp_connection.sendto("Lower!".encode(), add)



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
                    print(f"username: {username}, {conn}")
                    number_players = len(Players)
                    conn.sendall(f"Player with username {list(Players.keys())[0]} Added Successfully!\r\n".encode())
                    start_time = time.time()
                    if Max_Player >= len(Players) >= Min_Player:
                        conn.sendall(f"Waiting Time of {time_limit} to Start the Game.......\r\n".encode())
                        while time.time() - start_time <= time_limit:
                            if len(Players) > number_players:
                                number_players = len(Players)
                                start_time = time.time()
                                conn.sendall(
                                    f"New Player With username {list(Players.keys())[len(list(Players.keys()))-1]} Has Joined The Game!\r\n".encode())
                                conn.sendall(f"Waiting Time of {time_limit} to Start the Game.......\r\n".encode())
                                continue
                    if len(Players) == 1:
                        conn.sendall(f"Minimum Players to Play the game is {Min_Player}\r\n".encode())
                        while len(Players) == 1:
                            continue
                        number_players = len(Players)
                        conn.sendall(f"Player with username {list(Players.keys())[len(list(Players.keys()))-1]} Added Successfully!\r\n".encode())
                        start_time = time.time()
                        if Max_Player >= len(Players) >= Min_Player:
                            conn.sendall(f"Waiting Time of {time_limit} to Start the Game.......\r\n".encode())
                            while time.time() - start_time <= time_limit:
                                if len(Players) > number_players:
                                    number_players = len(Players)
                                    start_time = time.time()
                                    print(Players.keys())
                                    conn.sendall(
                                        f"New Player With username {list(Players.keys())[len(list(Players.keys()))-1]} Has Joined The Game!\r\n".encode())
                                    conn.sendall(f"Waiting Time of {time_limit} to Start the Game.......\r\n".encode())
                                    continue
                    conn.sendall("StartingGame\r\n".encode())
                    game_setup(conn, add)
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