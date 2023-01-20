import socket 
import client_funcoes as f

# Instância o socket
clientSocket = socket.socket()

def opcoesMenu(CID):
	while(True):
		f.menuPrincipal()
		opcao = int(input())

		if opcao > 0 and opcao < 6:
			if opcao == 1:
				msg = f.criarPedido(CID)
				clientSocket.send(msg.encode())

			elif opcao == 2:
				msg = f.modificarPedido(CID)
				clientSocket.send(msg.encode())
			
			elif opcao == 3:
				msg = f.listarPedido(CID)
				clientSocket.send(msg.encode())

			elif opcao == 4: 
				msg = f.listarPedidos(CID)
				clientSocket.send(msg.encode())

			elif opcao == 5: 
				msg = f.apagarPedido(CID)
				clientSocket.send(msg.encode())
		
			data = clientSocket.recv(1024)
			print("\nRecebido do servidor: " + data.decode() + "\n")

		else:
			if opcao == 6:
				clientSocket.send("".encode())
				return
			else:
				print("Opcao inválida! Tente novamente.")

def login():
	msg, CID = f.autentica()
	
	clientSocket.send(msg.encode())
	data = clientSocket.recv(1024)
	print("Receive from server: " + data.decode())

	if data.decode() == "Cliente autenticado":
		opcoesMenu(CID)
	else:
		clientSocket.send("".encode())
		return

def main():
	host = "127.0.0.1"            
	port = int(input("Digite o número da porta: "))
	clientSocket.connect((host, port))
	login()
	clientSocket.close()

if __name__ == '__main__': 
    main()
