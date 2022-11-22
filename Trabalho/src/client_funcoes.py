from model import Cliente, Mensagem, Pedido
from dataclasses import asdict
from varname import nameof
import json

# Menus

def menuPrincipal():
	print("\n<< Cliente >>")
	print("1 - Inserir Pedido")
	print("2 - Modificar Pedido")
	print("3 - Enumerar Pedido")
	print("4 - Enumerar Pedidos")
	print("5 - Cancelar Pedido")
	print("6 - Sair")
	print("Digite uma opcao: ",end="") 

# Cliente
def autentica():
	print("\n<< Bem vindo a Livraria Lovelace >>\n")
	nome = input("Digite seu nome: ")
	email = input("Digite seu email: ")
	senha = input("Digite sua senha: ")

	cliente = Cliente(nome,email,senha)
	msg = Mensagem("autenticarCliente",email,cliente)
	msg = str(json.dumps(asdict(msg)))

	return msg, email

# Pedidos

def criarPedido(CID):
	PID = input("Informe o título do produto: ")
	msg = Mensagem("criarPedido",CID,PID)
	msg = str(json.dumps(asdict(msg)))

	return msg

def modificarPedido(CID):
	OID = int(input("Digite o OID do pedido: ")) 
	produto = input("Digite o título do livro: ")
	quantidade = int(input("Digite a nova quantidade: "))

	dados = {nameof(OID):OID, nameof(produto):produto, nameof(quantidade):quantidade}

	msg = Mensagem("modificarPedido",CID,dados)
	msg = str(json.dumps(asdict(msg)))

	return msg

def listarPedido(CID):
	OID = int(input("Digite o OID do pedido: "))
	msg = Mensagem("listarPedido",CID,OID)
	msg = str(json.dumps(asdict(msg)))

	return msg

def listarPedidos(CID):
	msg = Mensagem("listarPedidos",CID)
	msg = str(json.dumps(asdict(msg)))
	
	return msg

def apagarPedido(CID):
	OID = int(input("Digite o OID do pedido: "))
	msg = Mensagem("apagarPedido",CID,OID)
	msg = str(json.dumps(asdict(msg)))
	
	return msg

