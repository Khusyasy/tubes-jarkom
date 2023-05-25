from socket import *
import sys

# Mengecek jumlah argumen yang diberikan
if len(sys.argv) < 4:
    print("Usage: python client.py server_host server_port filename")
    sys.exit()

# Membaca argumen dari baris perintah
serverHost = sys.argv[1]
serverPort = int(sys.argv[2])
filename = sys.argv[3]

# Membuat socket client
clientSocket = socket(AF_INET, SOCK_STREAM)

try:
    # Melakukan koneksi ke server
    clientSocket.connect((serverHost, serverPort))

    # Membuat HTTP request
    request = f"GET /{filename} HTTP/1.1\r\n"
    request += f"Host: {serverHost}\r\n\r\n"

    # Mengirimkan HTTP request ke server
    clientSocket.send(request.encode())

    # Menerima respons dari server
    chunk = []
    while True:
        data = clientSocket.recv(1024)
        chunk.append(data.decode())
        if not data:
            break
    response = "".join(chunk)

    # Mencetak HTTP response
    print(response)

except ConnectionRefusedError:
    print("Error: Connection Refused.")

finally:
    # Menutup socket client
    clientSocket.close()
