import socket 
from dto import Mensagem
import admin_api
from _thread import *
import json


def API(conn, data):

	try:
		mensagem = json.loads(data, object_hook=Mensagem.mensagemDecoder)
	except:
		print("Erro ao decodificar mensagem recebida do administrador")
	else:
		opcao = mensagem.funcao

		if opcao == "recuperarCliente":
			CID = mensagem.id
			topico, msg = admin_api.recuperarCliente(CID)

		elif opcao == "inserirCliente":
			CID = mensagem.id
			dadosCliente = mensagem.dados
			
			topico, msg = admin_api.inserirCliente(CID, dadosCliente)
			
			
		elif opcao == "modificarCliente":
			CID = mensagem.id
			dadosCliente = mensagem.dados

			topico, msg = admin_api.modificarCliente(CID, dadosCliente)

		elif opcao == "apagarCliente": 
			CID = mensagem.id
			topico, msg = admin_api.apagarCliente(CID)


		elif opcao == "recuperarProduto": 
			PID = mensagem.id
			topico, msg = admin_api.recuperarProduto(PID)
			
		elif opcao == "inserirProduto": 
			PID = mensagem.id
			dadosProduto = mensagem.dados
			topico, msg = admin_api.inserirProduto(PID, dadosProduto)
			

		elif opcao == "modificarProduto": 
			PID = mensagem.id
			dadosProduto = mensagem.dados
			topico, msg = admin_api.modificarProduto(PID, dadosProduto)
			

		elif opcao == "apagarProduto": 
			PID = mensagem.id
			topico, msg = admin_api.apagarProduto(PID)

		print("Enviado do topico " + topico + " a mensagem " + msg + "\n")
		conn.send(msg.encode())
		

def threaded(c, adress):
	while True:
		data = c.recv(1024)
		if not data:
			print(f"Conexão do endereço: {adress[1]} encerrada.\n")
			break
		print(data.decode())
		API(c, data.decode())
	c.close() 

def main():
	try:
		# Configuração do Socket
		serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		host = "127.0.0.1"            
		port = int(input("Digite o número da porta: "))
		serverSocket.bind((host, port))
	except socket.error as e:
		print(str(e))
		return

	print("\n<< Portal Administrador >>\n")
	print("Servidor conectado ao host: " + host + " na porta: " + str(port))

	serverSocket.listen(5)

	while True:
		conn, adress = serverSocket.accept()
		print("Connection from: " + str(adress))
		start_new_thread(threaded, (conn,adress))
	serverSocket.close()

if __name__ == '__main__': 
	main()