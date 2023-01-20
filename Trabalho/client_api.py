from functools import lru_cache
from model import Pedido
from dto import ProdutoDTO, PedidoDTO
from dataclasses import asdict
from typing import Any
import random
import json
import lmdb
import textwrap

from admin_api import recuperarCliente, recuperarProduto, modificarProduto, apagarProduto

# BD
Ki = 1024
Mi = 1024*Ki
Gi = 1024*Mi

pedidoBD = lmdb.Environment("pedido.lmdb", map_size=Gi, subdir=True, readonly=False, metasync=True, sync=True,
                           map_async=False, mode=493, create=True, readahead=True, writemap=True, meminit=True,
                           max_readers=126, max_dbs=2, max_spare_txns=1, lock=True)


# Clients

def autenticarCliente(CID, dados: Any):
	topico = "clientes/authCliente"
	msg = ""

	aux, confirmacao = recuperarCliente(CID)

	if confirmacao == "Cliente não encontrado":
		msg = confirmacao

	else:
		cliente = json.loads(confirmacao) 
		if cliente["senha"] != dados.senha:  
			msg = "Senha incorreta!"

		else:
			msg = "Cliente autenticado"
	
	return topico, msg


# Pedidos

def criarPedido(CID, PID):
	topico = "pedidos/cadPedido"
	msg = ""

	aux, confirmacao = recuperarProduto(PID)
	if confirmacao == "Produto não encontrado":
		msg = "Este título não está no catálogo."

	else:
		obj = json.loads(confirmacao)
		prod = ProdutoDTO(obj["titulo"], obj["descricao"], (int(obj["quantidade"])-1), float(obj["preco"]))
		if prod.quantidade <= 0: 
			apagarProduto(PID)
		else:	
			modificarProduto(PID, prod)

		OID = str(random.randint(0, 1000))
		pedido = Pedido(OID = OID.encode(), quantidade = 1,custo = prod.preco, PID = prod.titulo.encode(), CID = CID.encode())

		with pedidoBD.begin(write=True) as txn:
			txn.put(pedido.OID, bytes(pedido))

		msg = f"Pedido cadastrado com sucesso. O OID é {OID}"
	
	return topico, msg

def listarPedidos(CID):
	topico = "pedidos/listPedido"
	msg = ""
	json_object = ""

	with pedidoBD.begin() as txn:
		list = [ key for key, _ in txn.cursor() ]

	for item in list:
		with pedidoBD.begin() as txn:
			raw_bytes = txn.get(item)
			aux = Pedido.from_buffer_copy(raw_bytes)
			pedido = json.dumps(asdict(toDTO(aux)))
			json_object = json_object + pedido + "\n" 

	msg = json_object
	
	return topico, msg

def toDTO(dados: Pedido):
	pedidoDTO = PedidoDTO(OID = dados.OID.decode(), quantidade = dados.quantidade, custo = dados.custo, PID = dados.PID.decode(), CID = dados.CID.decode())
	return pedidoDTO

def listarPedido(OID):
	topico = "pedidos/getPedido"
	msg = ""
	json_object = ""

	with pedidoBD.begin() as txn:
		raw_bytes = txn.get(OID.encode())
		if raw_bytes!= None:
			dados = Pedido.from_buffer_copy(raw_bytes)
		else:
			dados = None
	
	if dados == None:
		msg = "Pedido não encontrado"
	else:
		pedido = toDTO(dados)
		msg = str(json.dumps(asdict(pedido)))
	
	return topico, msg

def apagarPedido(OID):
	topico = "pedidos/removePedido"
	msg = ""

	aux, confirmacao = listarPedido(OID)
	
	if confirmacao == "Pedido não encontrado":
		msg = confirmacao
	else:
		# Resetar o estoque do produto que estava no pedido
		dados = json.loads(confirmacao)
		aux, produto = recuperarProduto(dados["PID"])
		obj = json.loads(produto)
		
		prod = ProdutoDTO(obj["titulo"], obj["descricao"], (int(obj["quantidade"]) + dados["quantidade"]), float(obj["preco"]))
		modificarProduto(prod.titulo, prod)

		
		with pedidoBD.begin(write=True) as txn:
			txn.delete(OID.encode())

		msg = "Pedido cancelado com sucesso"

	return topico, msg

def modificarPedido(CID, dados: Any):
	topico = "pedidos/putPedido"
	msg = ""

	OID = dados.OID

	aux, confirmacao = listarPedido(OID)
	obj = json.loads(confirmacao)

	aux, produtoAntigo = recuperarProduto(obj["PID"])
	obj = json.loads(produtoAntigo)

	aux, produtoNovo = recuperarProduto(dados.produto)
	obj2 = json.loads(produtoNovo)

	if confirmacao == "Pedido não encontrado":
		msg = confirmacao
	elif obj2 == "Produto não encontrado":
		msg = obj2
	elif obj2["quantidade"] < dados.quantidade:
		msg = "Estoque insuficiente"
	else:
		# Resetar o estoque do produto que estava no pedido
		prod = ProdutoDTO(obj["titulo"], obj["descricao"], (int(obj["quantidade"]) + dados.quantidade), float(obj["preco"]))
		modificarProduto(prod.titulo, prod)

		# Atualizo o pedido
		custo = dados.quantidade * prod.preco
		pedido = Pedido(OID = OID.encode(), quantidade = dados.quantidade,custo = custo, PID = prod.titulo.encode(), CID = CID.encode())

		if int(obj2["quantidade"]) <= 0: 
			apagarProduto(obj2["titulo"])
		else:	
			modificarProduto(obj2["titulo"], prod)

		msg = "Pedido atualizado com sucesso"

	return topico, msg