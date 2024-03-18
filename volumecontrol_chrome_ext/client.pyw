import socket_comm
import socket
import sys
import time

if __name__ == "__main__":
    port = 5051
    server = socket.gethostbyname(socket.gethostname())
    addr = (server,port)
    client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    client.connect(addr)

    message = sys.argv[1]    

    socket_comm.send(client,message)
    socket_comm.send(client,"close")