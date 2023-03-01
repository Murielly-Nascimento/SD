#!/usr/bin/python                  # This is server.py file

import socket                      # Import socket module

s = socket.socket()                # Create a socket object
host = "127.0.0.1"
port = 12345                       # Reserve a port for your service.
s.bind((host, port)) 		   # Bind to the port

s.listen(5)                        # Now wait for client connections.
print(f"Listening on {host}:{port}")
while True:
   c, addr = s.accept()            # Accept client connection
   print('Got connection from', addr)
   c.send('Thank you'.encode())
   c.close()
