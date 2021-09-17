import socket

HOST="localhost"
BUFFER_SIZE=1024
PORT=8001

payload="GET / HTTP/1.0\r\n\Host: www.google.com\r\n\r\n"

def connect(addr):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(addr)
        s.sendall(payload.encode())
        s.shutdown(socket.SHUT_WR)
        full_data=s.recv(BUFFER_SIZE)
        print(full_data)
    except Exception as e:
        print(e)

    finally:
        s.close()

def main():
    connect((HOST,PORT))

if __name__=='__main__':
    main()
