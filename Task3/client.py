import os
import socket
from time import sleep

from config import SERVER_HOST, TCP_PORT, UDP_PORT
import threading
rounds_num = 6
guess = ""
def get_input():
    global guess
    guess = ""
    guess = input("Enter your guess: ")

def tcp_listener(sock):
    while True:
        try:
            msg = sock.recv(1024).decode().strip()
            if not msg:
                break
            if "finish" in msg.lower():
                print(msg)
                sock.close()
                exit(0)
        except:
            break
def tcp_client_connection():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((SERVER_HOST, TCP_PORT))

    while True:
        data = client_socket.recv(4096).decode()
        if not data:
            print("Server closed the connection.")
            break

        print(data)

        if "added" in data.lower():
            print("Successfully joined the game!")
            try:
                while True:
                    new_data = client_socket.recv(1024).decode()
                    if not new_data:
                        print("Server closed the connection.")
                        return
                    if "startinggame" in new_data.lower():
                        print("Starting Game.........\n")
                        break
                    print(new_data)
                udp_client_conn = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                print("3...")
                sleep(1)
                print("2...")
                sleep(1)
                print("1...")

                listener_thread = threading.Thread(target=tcp_listener, args=(client_socket,))
                listener_thread.start()

                # UDP Game Guessing Loop
                for i in range(6):
                    input_thread = threading.Thread(target=get_input)
                    input_thread.start()
                    input_thread.join(timeout=10)

                    if guess == "":
                        print("No Guesses Added!")
                        continue

                    udp_client_conn.sendto(guess.encode(), (SERVER_HOST, UDP_PORT))

                    try:
                        data, add = udp_client_conn.recvfrom(4096)
                        message = data.decode()

                        if "correct" in message.lower():
                            print(message)
                        elif "higher" in message.lower() or "lower" in message.lower():
                            print(message)
                        else:
                            print("UDP:", message)

                    except socket.timeout:
                        print("No response from server.")
                exit(0)
            except ConnectionResetError:
                print("Server closed the connection.")

        elif "taken" in data.lower():
            print("Username already taken. Try again.")
            user_input = input("Enter Join <Username>: ")
            client_socket.sendall((user_input + "\r\n").encode())
        elif "join" in data.lower():
            user_input = input("Enter Join <Username>: ")
            client_socket.sendall((user_input + "\r\n").encode())
        elif "max" in data.lower():
            print("Max Number of Players Reached!")
            break

    client_socket.close()

tcp_client_connection()