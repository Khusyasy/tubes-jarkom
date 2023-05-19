# 1301213294 | 1301210233

from socket import *
import sys

# Membuat socket server
serverSocket = socket(AF_INET, SOCK_STREAM)
serverPort = 6789
serverSocket.bind(("", serverPort))
serverSocket.listen(1)

while True:
    # Menunggu koneksi dari client
    print("Ready to serve...")
    # Membuat socket baru untuk koneksi dengan client
    connectionSocket, addr = serverSocket.accept()
    try:
        # Menerima dan memparsing HTTP request dari client
        chunk = []
        while True:
            data = connectionSocket.recv(1024)
            chunk.append(data)
            if not data or len(data) < 1024:
                break
        message = (b''.join(chunk)).decode()
        request_header, request_body = message.split('\r\n\r\n', 1)
        request_header = request_header.split()

        # Mengecek apakah request method
        if len(request_header) < 2:
            raise IOError

        if request_header[0] == "GET":
            # Jika request method GET
            # Mengambil nama file yang diminta oleh client
            filename = request_header[1][1:]

            # Membuka file yang diminta oleh client
            with open(filename, "rb") as f:
                outputdata = f.read()

            # HTTP response header jika file ditemukan
            response_header = "HTTP/1.1 200 OK\r\n"
            response_header += "Content-Type: text/html\r\n"
            response_header += f"Content-Length: {len(outputdata)}\r\n\r\n"

            # Mengirim HTTP response message ke client
            connectionSocket.send(response_header.encode())
            connectionSocket.sendall(outputdata)
        elif request_header[0] == "POST":
            # # Jika request method POST
            # # HTTP response header
            # response_header = "HTTP/1.1 200 OK\r\n"
            # response_header = f"Location: /{filename}\r\n\r\n"

            # # Mengirim HTTP response message ke client
            # connectionSocket.send(response_header.encode())
            pass


    except IOError:
        # Mengirim response "404 Not Found" jika file tidak ditemukan
        response_header = "HTTP/1.1 404 Not Found\r\n"
        response_header += "Content-Type: text/html\r\n\r\n"
        response_message = "<html><head></head><body><h1>404 Not Found</h1></body></html>"
        connectionSocket.send((response_header + response_message).encode())

    # Menutup koneksi dengan client
    connectionSocket.close()

# Menutup socket server dan keluar dari program
serverSocket.close()
sys.exit()
