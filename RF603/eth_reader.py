import socket
import struct
 
UDP_PORT = 603  # the receiving port on the pc
 
sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
sock.bind(("", UDP_PORT))
 
while True:
    data, addr = sock.recvfrom(1024)
    print("received message:", data) 