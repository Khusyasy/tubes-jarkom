# 1301213294 | 1301210233

from socket import *
import sys

# membuat socket server
serverSocket = socket(AF_INET, SOCK_STREAM)
serverPort = 6789
serverSocket.bind(('', serverPort))
serverSocket.listen(1)

while True:
    print('Ready to serve...')
    # membuat koneksi baru dari client
    connectionSocket, addr = serverSocket.accept()
    try:
        message = connectionSocket.recv(1024).decode()
        request = message.split()

        # mengecek apakah request method GET
        if len(request) < 2 or request[0] != "GET":
            raise IOError

        # mengambil nama file dan mencoba membuka file
        filename = request[1][1:]
        with open(filename) as f:
            outputdata = f.read()

        # HTTP response header jika file ditemukan
        connectionSocket.send("HTTP/1.1 200 OK\r\n".encode())
        connectionSocket.send("Content-Type: text/html\r\n".encode())
        connectionSocket.send(
            "Content-Length: {}\r\n".format(len(outputdata)).encode())
        connectionSocket.send("\r\n".encode())

        # mengirim konten file ke client
        for i in range(0, len(outputdata)):
            connectionSocket.send(outputdata[i].encode())

        # menutup socket client
        connectionSocket.close()
    except IOError:
        # HTTP header untuk file not found atau request method bukan GET
        connectionSocket.send("HTTP/1.1 404 Not Found\r\n".encode())
        connectionSocket.send("Content-Type: text/html\r\n".encode())
        connectionSocket.send("\r\n".encode())
        connectionSocket.send(
            "<html><head></head><body><h1>404 Not Found</h1></body></html>".encode())

        # menutup socket client
        connectionSocket.close()

serverSocket.close()
sys.exit()
