import admin_api as api
from dto import Mensagem,ProdutoDTO,ClienteDTO
import socket
import time

def main():
	# Configurações do Socket
	s = socket.socket()                        
	host = "127.0.0.1"                 
	port = 12345                                
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

		# Cadastro
		topico, msg = api.inserirCliente(CID, cliente)
		msg = f"Topico: {topico} e Mensagem: {msg}"
		c.send(msg.encode())
		time.sleep(1)

		# Modificação
		topico, msg = api.modificarCliente(CID, cliente)
		msg = f"Topico: {topico} e Mensagem: {msg}"
		c.send(msg.encode())
		time.sleep(1)

		# Recuperacao
		topico, msg = api.recuperarCliente(CID)
		msg = f"Topico: {topico} e Mensagem: {msg}"
		c.send(msg.encode())
		time.sleep(1)

		# Apagar
		topico, msg = api.apagarCliente(CID)
		msg = f"Topico: {topico} e Mensagem: {msg}"
		c.send(msg.encode())
		time.sleep(1)

		# Manipulação de Produtos
		PID = "Peter Pan"
		produto = ProdutoDTO("Peter Pan","O garoto que nunca cresceu")

		# Cadastro
		topico, msg = api.inserirProduto(PID, produto)
		msg = f"Topico: {topico} e Mensagem: {msg}"
		c.send(msg.encode())
		time.sleep(1)

		# Modificação
		topico, msg = api.modificarProduto(PID, produto)
		msg = f"Topico: {topico} e Mensagem: {msg}"
		c.send(msg.encode())
		time.sleep(1)

		# Recuperacao
		topico, msg = api.recuperarProduto(PID)
		msg = f"Topico: {topico} e Mensagem: {msg}"
		c.send(msg.encode())
		time.sleep(1)

		# Apagar
		topico, msg = api.apagarProduto(PID)
		msg = f"Topico: {topico} e Mensagem: {msg}"
		c.send(msg.encode())
		time.sleep(1)

		c.close()  
		s.close()
		break
	
if __name__ == '__main__': 
	main()