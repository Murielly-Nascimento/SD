from model import Mensagem,Produto,Cliente
import socket

def main():
	# Configurações do Socket
	adminSocket = socket.socket()
	host = "127.0.0.1"            
	port = 12346
	adminSocket.connect((host, port))

	print("Client conectado ao host: " + host + " na porta: " + str(port))

	while True:
		data = adminSocket.recv(1024)
		if not data:
			break

		print("Receive from server: " + data.decode() + "\n")
	adminSocket.close()

if __name__ == '__main__': 
	main()