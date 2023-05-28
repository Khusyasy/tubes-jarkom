# 1301213294 | 1301210233


from socket import *
import sys
import urllib.parse


def parse_http(message):
    # Memparsing HTTP request
    startline, message = message.split("\r\n", 1)
    startline = startline.split()
    header_text, body = message.split("\r\n\r\n", 1)
    header_text = header_text.split("\r\n")
    headers = {}
    for header in header_text:
        key, value = header.split(":", 1)
        headers[key] = value.strip()
    return (startline, headers, body)


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
        # Menerima HTTP request dari client
        chunk = []
        while True:
            data = connectionSocket.recv(1024)
            chunk.append(data.decode())
            if not data or len(data) < 1024:
                break
        message = "".join(chunk)

        req_startline, req_headers, req_body = parse_http(message)

        if req_startline[0] == "GET":
            # Jika request method GET
            # Mengambil nama file yang diminta oleh client
            filename = urllib.parse.unquote(req_startline[1][1:])

            # Membuka file yang diminta oleh client
            with open(filename, "rb") as f:
                outputdata = f.read()

            # HTTP response header jika file ditemukan
            response_header = "HTTP/1.1 200 OK\r\n"
            response_header += f"Content-Length: {len(outputdata)}\r\n\r\n"

            # Mengirim HTTP response message ke client
            connectionSocket.send(response_header.encode())
            connectionSocket.send(outputdata)
        elif req_startline[0] == "POST":
            # Jika request method POST

            # buat chrome aja
            if (req_body.strip() == ""):
                chunk = []
                while True:
                    data = connectionSocket.recv(1024)
                    chunk.append(data.decode())
                    if not data or len(data) < 1024:
                        break
                req_body = "".join(chunk)

            # Parsing form data
            # Membaca boundary dari HTTP request header
            boundary = req_headers["Content-Type"].split("=")[1]

            # Membaca form data dari HTTP request body
            req_body = req_body.split(f"--{boundary}\r\n", 1)[1]
            req_body = req_body.split(f"\r\n--{boundary}--\r\n")[0]
            filename = req_body.split('filename="')[1].split('"')[0]
            filecontent = req_body.split("\r\n\r\n", 1)[1]

            # Menyimpan file yang dikirim oleh client
            try:
                with open(filename, "wb") as f:
                    f.write(filecontent.encode())
            except:
                pass

            # HTTP response header
            response_header = "HTTP/1.1 303 See Other\r\n"
            response_header += f"Location: {urllib.parse.quote(filename)}\r\n\r\n"

            # Mengirim HTTP response message ke client
            connectionSocket.send(response_header.encode())

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
