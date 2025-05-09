import socket
from config import SERVER_HOST, TCP_PORT


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
            while True:
                new_data = client_socket.recv(1024).decode()
                if not new_data:
                    print("Server closed the connection.")
                    return
                if "startinggame" in new_data.lower():
                    print("Starting Game.........\n")
                    break
                print(new_data)
            break
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
