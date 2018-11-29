import time
import sys
import socket
import threading

host, port =  "127.0.0.1", 25001
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((host, port))
sock.send(b'1')
print(sock.recv(1024).decode())

def recvThreadFunc():
    while True:
        try:
            otherword = sock.recv(1024)
            if otherword:
                print(otherword.decode())
            else:
                pass
        except ConnectionAbortedError:
            print('Server closed this connection!')
            break
 
        except ConnectionResetError:
            print('Server is closed!')
            break


t = threading.Thread(target=recvThreadFunc)
t.setDaemon(True)
t.start()
t.join()