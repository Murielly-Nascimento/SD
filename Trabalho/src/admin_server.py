import socket, select 
from model import Mensagem
import admin_api
from _thread import *
import threading
import json
import publish as pub

def API(conn, data, adminMQTT):

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

			pub.publish(adminMQTT,topico,msg)
			
		elif opcao == "modificarCliente":
			CID = mensagem.id
			dadosCliente = mensagem.dados

			topico, msg = admin_api.modificarCliente(CID, dadosCliente)

		elif opcao == "apagarCliente": 
			CID = mensagem.id
			topico, msg = admin_api.apagarCliente(CID)

			pub.publish(adminMQTT,topico,CID)

		elif opcao == "recuperarProduto": 
			PID = mensagem.id
			topico, msg = admin_api.recuperarProduto(PID)
			
		elif opcao == "inserirProduto": 
			PID = mensagem.id
			dadosProduto = mensagem.dados
			topico, msg = admin_api.inserirProduto(PID, dadosProduto)

			pub.publish(adminMQTT,topico,msg)

		elif opcao == "modificarProduto": 
			PID = mensagem.id
			dadosProduto = mensagem.dados
			topico, msg = admin_api.modificarProduto(PID, dadosProduto)

			pub.publish(adminMQTT,topico,msg)

		elif opcao == "apagarProduto": 
			PID = mensagem.id
			topico, msg = admin_api.apagarProduto(PID)

			pub.publish(adminMQTT,topico,PID)

		print("Enviado do topico " + topico + " a mensagem " + msg + "\n")
		conn.send(msg.encode())
		

def threaded(c, adress, adminMQTT):
	while True:
		data = c.recv(1024)
		if not data:
			print(f"Conexão do endereço: {adress[1]} encerrada.\n")
			break
		print(data.decode())
		API(c, data.decode(), adminMQTT)
	c.close() 

def main():
	try:
		# Configuração do Socket
		serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		host = "127.0.0.1"            
		port = int(input("Digite o número da porta: ")) 
		print("Lembre-se que esse número será usado ao administradores se conectarem")
		serverSocket.bind((host, port))
	except socket.error as e:
		print(str(e))

	print("\n<< Portal Administrador >>\n")
	print("Servidor conectado ao host: " + host + " na porta: " + str(port))

	serverSocket.listen(5)
	
	# Configurações MQTT para comunicação com o cliente
	adminMQTT = pub.connectMQTT()
	adminMQTT.loop_start()

	while True:
		conn, adress = serverSocket.accept()
		print("Connection from: " + str(adress))
		start_new_thread(threaded, (conn,adress, adminMQTT))
	serverSocket.close()

if __name__ == '__main__': 
	main()