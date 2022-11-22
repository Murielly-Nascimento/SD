import socket  
from model import Mensagem
import client_api as api
from _thread import *
import threading
import json
import subscribe as sub

# Configuração do Socket
serverSocket = socket.socket()


# Tópicos MQTT	
cadProduto = "produtos/cadProduto"
removeProduto = "produtos/removeProduto"
cadCliente = "clientes/cadCliente"

def API(conn, data):

	try:
		mensagem = json.loads(data, object_hook=Mensagem.mensagemDecoder)
	except:
		print("Erro ao decodificar mensagem recebida do cliente")
	else:
		opcao = mensagem.funcao

		if opcao == "autenticarCliente":
			CID = mensagem.id
			dadosCliente = mensagem.dados
			topico, msg = api.autenticarCliente(CID,dadosCliente)

		elif opcao == "criarPedido": 
			CID = mensagem.id
			PID = mensagem.dados
			topico, msg = api.criarPedido(CID, PID)

		elif opcao == "modificarPedido":
			CID = mensagem.id
			dadosPedido = mensagem.dados
			
			topico, msg = api.modificarPedido(CID, dadosPedido)
			
		elif opcao == "listarPedido":
			CID = mensagem.id
			OID = mensagem.dados

			topico, msg = api.listarPedido(CID, OID)

		elif opcao == "listarPedidos": 
			CID = mensagem.id
			topico, msg = api.listarPedidos(CID)

		elif opcao == "apagarPedido": 
			CID = mensagem.id
			OID = mensagem.dados
			topico, msg = api.apagarPedido(CID,OID)


		print("Envie do topico " + topico + " a mensagem " + msg + "\n")
		conn.send(msg.encode())
		

lock = threading.Lock()

def threaded(c, adress):
	while True:
		data = c.recv(1024)
		if not data:
			print(f"Conexão do endereço: {adress[1]} encerrada.")
			lock.release()
			break
		print(data.decode())
		API(c, data.decode())
	c.close() 

def main():

	host = "127.0.0.1"            
	port = int(input("Digite o número da porta: "))
	serverSocket.bind((host, port))

	print("\n<< Portal do Cliente >>\n")
	print("Servidor conectado ao host: " + host + " na porta: " + str(port))

	serverSocket.listen(5)

	clientMQTT = sub.connectMQTT()
	sub.subscribe(clientMQTT,cadCliente)
	sub.subscribe(clientMQTT,cadProduto)
	sub.subscribe(clientMQTT,removeProduto)
	clientMQTT.loop_start()
	
	while True:
		conn, adress = serverSocket.accept()
		lock.acquire()
		print("Connection from: " + str(adress))
		start_new_thread(threaded, (conn,adress))
	clientMQTT.loop_stop()
	serverSocket.close()

if __name__ == '__main__': 
    main() 