import socket,time,sys
from multiprocessing import Process

HOST="localhost"
BUFFER_SIZE=1024
PORT=8001
extern_host='www.google.com'
extern_port=80

def get_remote_ip(host):
    print(f'Getting IP for {host}')
    try:
        remote_ip = socket.gethostbyname( host )
    except socket.gaierror:
        print ('Hostname could not be resolved. Exiting')
        sys.exit()

    print (f'Ip address of {host} is {remote_ip}')
    return remote_ip

def handle_request(addr,conn,proxy_end):
    send_full_data=conn.recv(BUFFER_SIZE)
    print(f"Sending received data {send_full_data} to Google")
    proxy_end.sendall(send_full_data)

    proxy_end.shutdown(socket.SHUT_WR)

    data=proxy_end.recv(BUFFER_SIZE)
    print(f"Sending received data to client")

    conn.send(data)



def main():


    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as proxy_start:
        print("Starting proxy server")
        proxy_start.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
        proxy_start.bind((HOST,PORT))
        proxy_start.listen(5)

        while True:
            conn,addr=proxy_start.accept()
            print("Connected by ",addr)
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as proxy_end:
                print("Connecting to Google")
                remote_ip=get_remote_ip(extern_host)
                proxy_end.connect((remote_ip,extern_port))

                p=Process(target=handle_request,args=(addr,conn,proxy_end))
                p.daemon=True
                p.start()
                print("Starting process ", p)

        conn.close()

if __name__=='__main__':
    main()
