from config import HOST, PORT
import socket
from urllib.parse import parse_qs
from urllib.parse import unquote

def handle_client(client_socket, client_address):
    print(f'Got connection from {client_address[0]}:{client_address[1]}')
    try:
        request = client_socket.recv(4096).decode()
        if not request:
            print("Empty request.")
            return

        headers_end = request.find("\r\n\r\n")
        header_lines = request[:headers_end].splitlines()
        body = request[headers_end + 4:]

        request_line = header_lines[0]
        method, path, _ = request_line.split()

        if method.upper() == "POST":
            form_data = parse_qs(body)# 1220808 122175 1220216
            filename = form_data.get("filename", [""])[0]
            filetype = form_data.get("filetype", [""])[0]
            print(filename)
            if filetype and filename:
                if filetype == "image":
                    try:
                        filename = filename.replace("/img/", "")
                        print(filename)
                        with open(f"./templates/img/{filename}", "rb") as f:
                            content = f.read()
                        response_headers = (
                            "HTTP/1.1 200 OK\r\n"
                            "Content-Type: image/png\r\n"
                            f"Content-Length: {len(content)}\r\n"
                            "\r\n"
                        ).encode()
                        print(request)
                        client_socket.sendall(response_headers + content)
                        return
                    except FileNotFoundError:
                        redirect_url = f"https://www.google.com/search?q={filename.replace(' ', '+')}&tbm=vid"
                        response_headers = (
                            "HTTP/1.1 303 See Other\r\n"
                            f"Location: {redirect_url}\r\n"
                            "Content-Length: 0\r\n"
                            "Connection: Close\r\n"
                            "\r\n"
                        ).encode()
                        client_socket.sendall(response_headers)
                        print(request)
                        return
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
                        print(request)
                        client_socket.sendall(response_headers + content)
                        return
                    except FileNotFoundError:
                        redirect_url = f"https://www.google.com/search?q={filename.replace(' ', '+')}&tbm=vid"
                        response_headers = (
                            "HTTP/1.1 303 See Other\r\n"
                            f"Location: {redirect_url}\r\n"
                            "Content-Length: 0\r\n"
                            "Connection: Close\r\n"
                            "\r\n"
                        ).encode()
                        client_socket.sendall(response_headers)
                        print(request)
                        return
                else:
                    response_body = "<h1>Unsupported file type requested.</h1>"
            else:
                response_body = "<h1>Missing filename or filetype.</h1>"

            response = (
                "HTTP/1.1 400 Bad Request\r\n"
                "Content-Type: text/html\r\n"
                f"Content-Length: {len(response_body)}\r\n"
                "\r\n"
                f"{response_body}"
            )
            client_socket.sendall(response.encode())
            return
        if method.upper() == "GET":
            path = path.rstrip("?")
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
            if file_path:

                if file_path.endswith(".css"):#1220808
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
                        print(request)
                        client_socket.sendall(response.encode())
                    except FileNotFoundError:
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
                if file_path.endswith(".png"):#1220808
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
                        print(request)
                        client_socket.sendall(response_headers + content)
                        return
                    except FileNotFoundError:
                        response_body = "<h1>img not found.</h1>"
                    response = (
                        "HTTP/1.1 404 Not Found\r\n"
                        "Content-Type: image/png\r\n"
                        f"Content-Length: {len(content)}\r\n"
                        "\r\n"
                        f"{response_body}"
                    )
                    client_socket.sendall(response.encode())
                    return
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
                    print(request)
                    client_socket.sendall(response.encode())
                except FileNotFoundError:
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
                    print(request)
                    client_socket.sendall(response.encode())
            else:
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
                print(request)
                client_socket.sendall(response.encode())

    except Exception as e:
        print("Error:", e)
    finally:
        client_socket.close()

def run_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, PORT))
    server_socket.listen(5)
    print(f"Server listening on {HOST}:{PORT}")
    while True:
        client_socket, client_address = server_socket.accept()
        handle_client(client_socket, client_address)


run_server()
