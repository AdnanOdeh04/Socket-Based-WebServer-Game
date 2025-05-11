from config import HOST, PORT
import socket
from urllib.parse import parse_qs, unquote

# Handle one client connection
def handle_client(client_socket, client_address):
    print(f'Connected to {client_address[0]}:{client_address[1]}')

    try:
        # Read the request from the browser
        request = client_socket.recv(4096).decode()
        if not request:
            print("No data received.")
            return

        # Split the request into headers and body
        headers_end = request.find("\r\n\r\n")
        header_lines = request[:headers_end].splitlines()
        body = request[headers_end + 4:]

        # Get method (GET or POST) and requested path
        request_line = header_lines[0]
        method, path, _ = request_line.split()

        # Handle POST (form submission)
        if method.upper() == "POST":
            form_data = parse_qs(body)
            filename = form_data.get("filename", [""])[0]
            filetype = form_data.get("filetype", [""])[0]
            print(filename)

            if filetype and filename:
                # Show image
                if filetype == "image":
                    try:
                        filename = filename.replace("/img/", "")
                        print(filename)
                        with open(f"./templates/img/{filename}", "rb") as f:
                            content = f.read()
                        # Send image back to browser
                        response_headers = (
                            "HTTP/1.1 200 OK\r\n"
                            "Content-Type: image/png\r\n"
                            f"Content-Length: {len(content)}\r\n"
                            "\r\n"
                        ).encode()
                        client_socket.sendall(response_headers + content)
                        return
                    except FileNotFoundError:
                        # If not found, redirect to Google
                        redirect_url = f"https://www.google.com/search?q={filename.replace(' ', '+')}&tbm=vid"
                        response_headers = (
                            "HTTP/1.1 303 See Other\r\n"
                            f"Location: {redirect_url}\r\n"
                            "Content-Length: 0\r\n"
                            "Connection: Close\r\n"
                            "\r\n"
                        ).encode()
                        client_socket.sendall(response_headers)
                        return

                # Show video
                elif filetype == "video":
                    try:
                        with open(f"./templates/videos/{filename}", "rb") as f:
                            content = f.read()
                        response_headers = (
                            "HTTP/1.1 200 OK\r\n"
                            "Content-Type: video/mp4\r\n"
                            f"Content-Length: {len(content)}\r\n"
                            "\r\n"
                        ).encode()
                        client_socket.sendall(response_headers + content)
                        return
                    except FileNotFoundError:
                        # If not found, redirect to Google
                        redirect_url = f"https://www.google.com/search?q={filename.replace(' ', '+')}&tbm=vid"
                        response_headers = (
                            "HTTP/1.1 303 See Other\r\n"
                            f"Location: {redirect_url}\r\n"
                            "Content-Length: 0\r\n"
                            "Connection: Close\r\n"
                            "\r\n"
                        ).encode()
                        client_socket.sendall(response_headers)
                        return
                else:
                    response_body = "<h1>Unknown file type.</h1>"
            else:
                response_body = "<h1>Missing file name or type.</h1>"

            # If something’s wrong with the form
            response = (
                "HTTP/1.1 400 Bad Request\r\n"
                "Content-Type: text/html\r\n"
                f"Content-Length: {len(response_body)}\r\n"
                "\r\n"
                f"{response_body}"
            )
            client_socket.sendall(response.encode())
            return

        # Handle GET request (normal browser page)
        if method.upper() == "GET":
            path = path.rstrip("?")

            # Match path to file
            if path in ["/", "/en", "/index.html", "/main_en.html"]:
                file_path = "./templates/main_en.html"
            elif path in ["/ar", "/main_ar.html"]:
                file_path = "./templates/main_ar.html"
            elif path == "/mySite_STDID_en.html":
                file_path = "./templates/mySite_1220175_en.html"
            elif path == "/mySite_STDID_ar.html":
                file_path = "./templates/mySite_1220175_ar.html"
            elif path == "/css/main_en.css":
                file_path = "./css/main_en.css"
            elif path == "/css/main_ar.css":
                file_path = "./css/main_ar.css"
            elif path == "/css/supporting":
                file_path = "./css/supporting.css"
            else:
                file_path = path

            # Serve CSS file
            if file_path.endswith(".css"):
                try:
                    with open(f"./templates{path}", "r") as f:
                        content = f.read()
                    response = (
                        "HTTP/1.1 200 OK\r\n"
                        "Content-Type: text/css\r\n"
                        f"Content-Length: {len(content.encode())}\r\n"
                        "\r\n"
                        f"{content}"
                    )
                    client_socket.sendall(response.encode())
                except FileNotFoundError:
                    # CSS not found
                    response_body = "<h1>CSS file not found.</h1>"
                    response = (
                        "HTTP/1.1 404 Not Found\r\n"
                        "Content-Type: text/css\r\n"
                        f"Content-Length: {len(response_body.encode())}\r\n"
                        "\r\n"
                        f"{response_body}"
                    )
                    client_socket.sendall(response.encode())
                return

            # Serve image
            if file_path.endswith(".png"):
                try:
                    file_path = file_path.replace("/img/", "")
                    file_path = unquote(file_path)
                    print(file_path)
                    with open(f"./templates/img/{file_path}", "rb") as f:
                        content = f.read()
                    response_headers = (
                        "HTTP/1.1 200 OK\r\n"
                        "Content-Type: image/png\r\n"
                        f"Content-Length: {len(content)}\r\n"
                        "\r\n"
                    ).encode()
                    client_socket.sendall(response_headers + content)
                    return
                except FileNotFoundError:
                    # Image not found
                    response_body = "<h1>img not found.</h1>"
                    response = (
                        "HTTP/1.1 404 Not Found\r\n"
                        "Content-Type: image/png\r\n"
                        f"Content-Length: {len(response_body.encode())}\r\n"
                        "\r\n"
                        f"{response_body}"
                    )
                    client_socket.sendall(response.encode())
                    return

            # Serve HTML file
            try:
                with open(file_path, "r") as f:
                    content = f.read()
                response = (
                    "HTTP/1.1 200 OK\r\n"
                    "Content-Type: text/html\r\n"
                    f"Content-Length: {len(content.encode())}\r\n"
                    "\r\n"
                    f"{content}"
                )
                client_socket.sendall(response.encode())
            except FileNotFoundError:
                # HTML not found
                response_body = f"""
                    <html>
                    <head><title>Error 404</title></head>
                    <body>
                        <h1 style="color:red;">The file is not found</h1>
                        <p>Client IP: {client_address[0]}</p>
                        <p>Client Port: {client_address[1]}</p>
                    </body>
                    </html>
                """
                response = (
                    "HTTP/1.1 404 Not Found\r\n"
                    "Content-Type: text/html\r\n"
                    f"Content-Length: {len(response_body.encode())}\r\n"
                    "\r\n"
                    f"{response_body}"
                )
                client_socket.sendall(response.encode())

    except Exception as e:
        print("Error:", e)

    # Always close the connection at the end
    finally:
        client_socket.close()

# Start the server and keep it running
def run_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, PORT))
    server_socket.listen(5)
    print(f"Server is running at {HOST}:{PORT}")
    while True:
        client_socket, client_address = server_socket.accept()
        handle_client(client_socket, client_address)

# Run it!
run_server()
