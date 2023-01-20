from dto import ClienteDTO, Mensagem, ProdutoDTO
from dataclasses import asdict
import json

# Menus

def menuPrincipal():
	print("\n<< Administrador da Livraria Lovelace >>")
	print("1 - Manipular Clientes")
	print("2 - Manipular Produtos")
	print("3 - Sair")
	print("Digite uma opcao: ",end="") 

def menuCliente():
	print("\n<< Cliente >>")
	print("1 - Recuperar Cliente")
	print("2 - Inserir Cliente")
	print("3 - Modificar Cliente")
	print("4 - Apagar Cliente")
	print("5 - Sair")
	print("Digite uma opcao: ",end="") 

def menuProduto():
	print("\n<< Produto >>")
	print("6 - Recuperar Produto")
	print("7 - Inserir Produto")
	print("8 - Modificar Produto")
	print("9 - Apagar Produto")
	print("10 - Sair")
	print("Digite uma opcao: ",end="") 


# Clientes

def inserirCliente():
	nome = input("Nome do cliente: ")
	email = input("Email do cliente: ")
	senha = input("Senha do cliente: ")

	cliente = ClienteDTO(nome,email,senha)

	msg = Mensagem("inserirCliente",email,cliente)
	msg = str(json.dumps(asdict(msg)))

	return msg

def modificarCliente():
	email = input("Digite o email do cliente: ")
	nome = input("Digite o novo nome do cliente: ")
	senha = input("Digite a nova senha do cliente: ")

	cliente = ClienteDTO(nome,email,senha)

	msg = Mensagem("modificarCliente",email,cliente)
	msg = str(json.dumps(asdict(msg)))

	return msg

def recuperarCliente():
	email = input("Digite o email do cliente: ")
	msg = Mensagem("recuperarCliente",email)
	msg = str(json.dumps(asdict(msg)))

	return msg

def apagarCliente():
	email = input("Digite o email do cliente: ")
	msg = Mensagem("apagarCliente",email)
	msg = str(json.dumps(asdict(msg)))
	
	return msg

# Produtos

def inserirProduto():
	try:
		titulo = input("Digite o titulo do livro: ")
		descricao = input("Digite a sinopse do livro: ")
		quantidade = int(input("Digite a quantidade do livro: "))
		preco = float(input("Digite o preço do livro: "))

		produto = ProdutoDTO(titulo,descricao,quantidade,preco)
	except:
		print("\nQuantidade deve ser um número e preco deve ser um valor racional.")
		print("Os valores padrão: 1 e R$ 50,00 serão atribuídos ao produto")
		produto = ProdutoDTO(titulo,descricao)

	msg = Mensagem("inserirProduto",titulo,produto)
	msg = str(json.dumps(asdict(msg)))

	return msg

def modificarProduto():
	try:
		titulo = input("Digite o titulo do livro: ")
		descricao = input("Digite a nova sinopse do livro: ")
		quantidade = int(input("Digite a nova quantidade do livro: "))
		preco = float(input("Digite o novo preço do livro: "))
		produto = ProdutoDTO(titulo,descricao, quantidade, preco)
	except:
		print("\nQuantidade deve ser um número e preco deve ser um valor racional.")
		print("Os valores padrão: 1 e R$ 50,00 serão atribuídos ao produto")
		produto = ProdutoDTO(titulo,descricao)

	produto = ProdutoDTO(titulo,descricao,quantidade,preco)

	msg = Mensagem("modificarProduto",titulo,produto)
	msg = str(json.dumps(asdict(msg)))

	return msg

def recuperarProduto():
	titulo = input("Digite o titulo do livro: ")
	msg = Mensagem("recuperarProduto",titulo)
	msg = str(json.dumps(asdict(msg)))

	return msg

def apagarProduto():
	titulo = input("Digite o titulo do livro: ")
	msg = Mensagem("apagarProduto",titulo)
	msg = str(json.dumps(asdict(msg)))
	
	return msg