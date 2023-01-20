import client_api as api
from dto import ProdutoDTO,ClienteDTO,Mensagem
from varname import nameof
from dataclasses import asdict
import socket
import time
import json

def main():
	# Configurações do Socket
	s = socket.socket()                        
	host = "127.0.0.1"                 
	port = 12346                                
	s.bind((host, port))                        
	s.listen(5)                                 

	print("Servidor conectado ao host: " + host + " na porta: " + str(port))
	print("Aguardando conexões...")

	while True:
		c, addr = s.accept()                     
		print('Got connection from', addr)

		# Testando manipulação de cliente
		CID = "maria@gmail.com"
		cliente = ClienteDTO("Maria",CID,"123456")

		# Autenticar
		topico, msg = api.autenticarCliente(CID, cliente)
		msg = f"Topico: {topico} e Mensagem: {msg}"
		c.send(msg.encode())
		time.sleep(1)

		# Manipulação de Pedidos
		PID = "Alice"
		produto = ProdutoDTO("Alice","Alice no Pais das Maravilhas")

		# Inserir 
		topico, msg = api.criarPedido(CID, PID)
		msg = f"Topico: {topico} e Mensagem: {msg}"
		c.send(msg.encode())
		time.sleep(1)

		# Modificação
		OID = 1 
		produto = "Alice"
		quantidade = 5
		dados = {nameof(OID):OID, nameof(produto):produto, nameof(quantidade):quantidade}
		
		# Exemplo de desserialização usada
		aux = Mensagem("modificarPedido",CID,dados)
		aux = str(json.dumps(asdict(aux)))
		mensagem = json.loads(aux, object_hook=Mensagem.mensagemDecoder)

		topico, msg = api.modificarPedido(CID, mensagem.dados)
		msg = f"Topico: {topico} e Mensagem: {msg}"
		c.send(msg.encode())
		time.sleep(1)

		# Listar Pedido
		topico, msg = api.listarPedido(CID,OID)
		msg = f"Topico: {topico} e Mensagem: {msg}"
		c.send(msg.encode())
		time.sleep(1)

		# Listar Pedidos
		topico, msg = api.listarPedidos(CID)
		msg = f"Topico: {topico} e Mensagem: {msg}"
		c.send(msg.encode())
		time.sleep(1)
		
		# Apagar Pedidos
		topico, msg = api.apagarPedido(CID,OID)
		msg = f"Topico: {topico} e Mensagem: {msg}"
		c.send(msg.encode())
		time.sleep(1)

		c.close()  
		s.close()
		break
	
if __name__ == '__main__': 
	main()