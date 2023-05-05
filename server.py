# 1. Implementasi pembuatan TCP socket dan mengaitkannya ke alamat dan port tertentu
# (poin: 20)
# 2. Program web server dapat menerima dan memparsing HTTP request yang dikirimkan
# oleh browser(poin: 20)
# 3. Web server dapat mencari dan mengambil file(dari file system) yang diminta oleh
# client(poin: 15)
# 4. Web server dapat membuat HTTP response message yang terdiri dari header dan
# konten file yang diminta(poin: 20)
# 5. Web server dapat mengirimkan response message yang sudah dibuat ke browser
# (client) dan dapat ditampilkan dengan benar di sisi client(poin: 15)
# 6. Jika file yang diminta oleh client tidak tersedia, web server dapat mengirimkan pesan
# "404 Not Found" dan dapat ditampilkan dengan benar di sisi client. (poin: 10)

# 1301213294
# 1301210233

from socket import *
import sys

# membuat socket server
serverSocket = socket(AF_INET, SOCK_STREAM)
serverPort = 6789
serverSocket.bind(('', serverPort))
serverSocket.listen(1)

while True:
    # Establish the connection
    print('Ready to serve...')
    connectionSocket, addr = serverSocket.accept()
    try:
        message = connectionSocket.recv(1024).decode()
        filename = message.split()[1]
        f = open(filename[1:])
        outputdata = f.read()
        # Send one HTTP header line into socket
        connectionSocket.send("HTTP/1.1 OK\r\n\r\n".encode())
        # Send the content of the requested file to the client
        for i in range(0, len(outputdata)):
            connectionSocket.send(outputdata[i].encode())
        connectionSocket.send("\r\n".encode())
        connectionSocket.close()
    except IOError:
        # Send response message for file not found
        connectionSocket.send("HTTP/1.1 404 Not Found\r\n\r\n".encode())
        # Close client socket
        connectionSocket.close()

serverSocket.close()
sys.exit()
