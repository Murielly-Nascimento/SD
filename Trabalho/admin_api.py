from functools import lru_cache
from model import Cliente, Produto
from dto import ClienteDTO, ProdutoDTO
from dataclasses import asdict
from typing import Any
import json
import lmdb

# BD

Ki = 1024
Mi = 1024*Ki
Gi = 1024*Mi

clienteBD = lmdb.Environment("cliente.lmdb", map_size=Gi, subdir=True, readonly=False, metasync=True, sync=True,
                           map_async=False, mode=493, create=True, readahead=True, writemap=True, meminit=True,
                           max_readers=126, max_dbs=2, max_spare_txns=1, lock=True)

produtoBD = lmdb.Environment("produto.lmdb", map_size=Gi, subdir=True, readonly=False, metasync=True, sync=True,
                           map_async=False, mode=493, create=True, readahead=True, writemap=True, meminit=True,
                           max_readers=126, max_dbs=2, max_spare_txns=1, lock=True)

# Clients
		
def recuperarCliente(CID):
	topico = "clientes/getCliente"
	msg = ""

	with clienteBD.begin() as txn:
		raw_bytes = txn.get(CID.encode())
		if raw_bytes!= None:
			dados = Cliente.from_buffer_copy(raw_bytes)
		else:
			dados = None

	if dados == None:
		msg = "Cliente não encontrado"
	else: 
		cliente = ClienteDTO(dados.nome.decode(), dados.email.decode(), dados.senha.decode())
		msg = str(json.dumps(asdict(cliente)))

	return topico, msg

def inserirCliente(CID, dados: Any):
	topico = "clientes/cadCliente"
	msg = ""

	aux, confirmacao = recuperarCliente(CID)

	if confirmacao != "Cliente não encontrado":
		msg = "Cliente já cadastrado."
	
	else:
		nome = dados.nome
		email = dados.email
		senha = dados.senha

		dadosCliente = Cliente(nome = nome.encode(), email = email.encode(), senha = senha.encode())
		
		with clienteBD.begin(write=True) as txn:
			txn.put(dadosCliente.email, bytes(dadosCliente))

		msg = "Cliente cadastrado com sucesso!"

	return topico, msg

def modificarCliente(CID, dados: Any):
	topico = "clientes/putCliente"
	msg = ""

	aux, confirmacao = recuperarCliente(CID)

	if confirmacao == "Cliente não encontrado":
		msg = confirmacao	

	else:
		nome = dados.nome
		email = dados.email
		senha = dados.senha

		dadosCliente = Cliente(nome = nome.encode(), email = email.encode(), senha = senha.encode())
		
		with clienteBD.begin(write=True) as txn:
			txn.put(dadosCliente.email, bytes(dadosCliente))

		msg = "Nome e senha do cliente alterados com sucesso!"
	
	return topico, msg

def apagarCliente(CID):
	topico = "clientes/removeCliente"
	msg = ""

	aux, confirmacao = recuperarCliente(CID)

	if confirmacao == "Cliente não encontrado":
		msg = confirmacao	
	else:
		with clienteBD.begin(write=True) as txn:
			txn.delete(CID.encode())
		msg = f"Cliente {CID} removido"

	return topico, msg


# Products

def recuperarProduto(PID):
	topico = "produtos/getProduto"
	msg = ""

	with produtoBD.begin() as txn:
		raw_bytes = txn.get(PID.encode())
		if raw_bytes != None:
			dados = Produto.from_buffer_copy(raw_bytes)
		else:
			dados = None

	if dados == None:
		msg = "Produto não encontrado"
	else:
		produto = ProdutoDTO(dados.titulo.decode(), dados.descricao.decode(), dados.quantidade, dados.preco)
		msg = str(json.dumps(asdict(produto)))

	return topico, msg 

def inserirProduto(PID, dados: Any):
	topico = "produtos/cadProduto"
	msg = ""

	aux, confirmacao = recuperarProduto(PID)

	if confirmacao != "Produto não encontrado":
		msg = "Produto já cadastrado"	

	else:	
		titulo = dados.titulo
		descricao = dados.descricao
		quantidade = dados.quantidade
		preco = dados.preco

		dadosProduto = Produto(titulo = titulo.encode(), descricao = descricao.encode(), quantidade = quantidade, preco = preco)
		
		with produtoBD.begin(write=True) as txn:
			txn.put(dadosProduto.titulo, bytes(dadosProduto))

		msg = "Produto cadastrado com sucesso!"

	return topico, msg

def modificarProduto(PID, dados: Any):
	topico = "produtos/putProduto"
	msg = ""

	aux, confirmacao = recuperarProduto(PID)

	if confirmacao == "Produto não encontrado":
		msg = confirmacao	

	else:
		titulo = dados.titulo
		descricao = dados.descricao
		quantidade = dados.quantidade
		preco = dados.preco

		dadosProduto = Produto(titulo = titulo.encode(), descricao = descricao.encode(), quantidade = quantidade, preco = preco)
		
		with produtoBD.begin(write=True) as txn:
			txn.put(dadosProduto.titulo, bytes(dadosProduto))

		msg = "Produto atualizado com sucesso!"
	
	return topico, msg

def apagarProduto(PID):
	topico = "produtos/removeProduto"
	msg = ""

	aux, confirmacao = recuperarProduto(PID)

	if confirmacao == "Produto não encontrado":
		msg = confirmacao	
	else: 
		with produtoBD.begin(write=True) as txn:
			txn.delete(PID.encode())
		msg = f"Produto {PID} removido"

	return topico, msg