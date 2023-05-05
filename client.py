from socket import *
import sys

if len(sys.argv) < 4:
    print('client.py server_host server_port filename')
    sys.exit()

serverName = sys.argv[1]
serverPort = int(sys.argv[2])
filename = sys.argv[3]
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName, serverPort))
clientSocket.send(f'GET /{filename} HTTP/1.1'.encode())
response = clientSocket.recv(1024)
while (response):
    print(response.decode())
    response = clientSocket.recv(1024)
clientSocket.close()
sys.exit()
