#!/usr/local/bin/python3

import socket                   # Import socket module

s = socket.socket()             # Create a socket 
host = "127.0.0.1"              # Get local host name
port = 12345                    # Port for your service

s.connect((host, port))
data = s.recv(1024)             # Receive data
print(data.decode())
s.close()                       # Close the socket

