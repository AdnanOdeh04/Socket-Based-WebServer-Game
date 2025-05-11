import os
import socket
from time import sleep
from config import SERVER_HOST, TCP_PORT, UDP_PORT
import threading

# Total number of rounds (guesses allowed)
rounds_num = 6

# Variable to store the user's guess
guess = ""

# Function to get user input (guess) with timeout
def get_input():
    global guess
    guess = ""
    guess = input("Enter your guess: ")

# Thread function to listen for messages from the server (TCP)
def tcp_listener(sock):
    while True:
        try:
            msg = sock.recv(1024).decode().strip()
            if not msg:
                break
            # If the server says "finish", show it and exit the game
            if "finish" in msg.lower():
                print(msg)
                sock.close()
                exit(0)
        except:
            break

# Function to connect to the server and play the game
def tcp_client_connection():
    # Create TCP socket and connect to the server
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((SERVER_HOST, TCP_PORT))

    while True:
        # Receive message from server (welcome, status, etc.)
        data = client_socket.recv(4096).decode()
        if not data:
            print("Server closed the connection.")
            break

        print(data)

        # If player was successfully added
        if "added" in data.lower():
            print("Successfully joined the game!")
            try:
                # Wait for the game to start
                while True:
                    new_data = client_socket.recv(1024).decode()
                    if not new_data:
                        print("Server closed the connection.")
                        return
                    if "startinggame" in new_data.lower():
                        print("Starting Game.........\n")
                        break
                    print(new_data)

                # Create UDP socket to send guesses
                udp_client_conn = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

                # Countdown before game starts
                print("3...")
                sleep(1)
                print("2...")
                sleep(1)
                print("1...")

                # Start a thread to keep listening for server TCP messages
                listener_thread = threading.Thread(target=tcp_listener, args=(client_socket,))
                listener_thread.start()

                # Game loop for 6 rounds
                for i in range(6):
                    # Start input thread so the user has 10 seconds to guess
                    input_thread = threading.Thread(target=get_input)
                    input_thread.start()
                    input_thread.join(timeout=10)

                    if guess == "":
                        print("No Guesses Added!")
                        continue

                    # Send guess to the server using UDP
                    udp_client_conn.sendto(guess.encode(), (SERVER_HOST, UDP_PORT))

                    try:
                        # Get the server's response over UDP
                        data, add = udp_client_conn.recvfrom(4096)
                        message = data.decode()

                        # Show response to the player
                        if "correct" in message.lower():
                            print(message)
                        elif "higher" in message.lower() or "lower" in message.lower():
                            print(message)
                        else:
                            print("UDP:", message)

                    except socket.timeout:
                        print("No response from server.")
                exit(0)  # Exit after all rounds
            except ConnectionResetError:
                print("Server closed the connection.")

        # If username already taken
        elif "taken" in data.lower():
            print("Username already taken. Try again.")
            user_input = input("Enter Join <Username>: ")
            client_socket.sendall((user_input + "\r\n").encode())

        # If the server is waiting for a username
        elif "join" in data.lower():
            user_input = input("Enter Join <Username>: ")
            client_socket.sendall((user_input + "\r\n").encode())

        # If the server is full
        elif "max" in data.lower():
            print("Max Number of Players Reached!")
            break

    # Close connection when game ends
    client_socket.close()

# Start the client program
tcp_client_connection()
