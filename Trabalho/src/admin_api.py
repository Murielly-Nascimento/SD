from functools import lru_cache
from model import Cliente, Produto
from dataclasses import asdict
from typing import Any
import random
import json
# BD

bd_clientes = {}
bd_produtos = {}
bd_pedidos = {}

# Cache

# Clients
		
def recuperarCliente(CID):
	topico = "clientes/getCliente"
	msg = ""

	if CID not in bd_clientes:
		msg = "Cliente não encontrado"
	else: 
		msg = str(json.dumps(asdict(bd_clientes[CID])))

	return topico, msg

def inserirCliente(CID, dados: Any):
	topico = "clientes/cadCliente"
	msg = ""

	if CID in bd_clientes:
		msg =  "Cliente já cadastrado"	
	else:
		dadosCliente = Cliente(dados.nome, dados.email, dados.senha)
		bd_clientes[CID] = dadosCliente
		msg = str(json.dumps(asdict(bd_clientes[CID])))

	return topico, msg

def modificarCliente(CID, dados: Any):
	topico = "clientes/putCliente"
	msg = ""

	if CID not in bd_clientes:
		msg = "Cliente não cadastrado"	
	else:
		dadosCliente = Cliente(dados.nome, dados.email, dados.senha)
		bd_clientes[CID] = dadosCliente
		msg =  "Cliente atualizado com sucesso"
	
	return topico, msg

def apagarCliente(CID):
	topico = "clientes/removeCliente"
	msg = ""

	if CID not in bd_clientes:
		msg = "Cliente não cadastrado"	
	else:
		bd_clientes.pop(CID)
		msg = f"Cliente {CID} removido"

	return topico, msg


# Products

def recuperarProduto(PID):
	topico = "produtos/getProduto"
	msg = ""
	if PID not in bd_produtos:
		msg = "Produto não encontrado"
	else:
		msg = str(json.dumps(asdict(bd_produtos[PID])))

	return topico, msg 

def inserirProduto(PID, dados: Any):
	topico = "produtos/cadProduto"
	msg = ""
	if PID in bd_produtos:
		msg = "Produto já cadastrado"
	else:	
		dadosProduto = Produto(dados.titulo, dados.descricao, dados.quantidade, dados.preco)
		bd_produtos[PID] = dadosProduto
		msg =  str(json.dumps(asdict(bd_produtos[PID])))

	return topico, msg

def modificarProduto(PID, dados: Any):
	topico = "produtos/putProduto"
	msg = ""
	if PID not in bd_produtos:
		msg = "Produto não cadastrado"	
	else:
		dadosProduto = Produto(dados.titulo, dados.descricao, dados.quantidade, dados.preco)
		bd_produtos[PID] = dadosProduto
		msg = str(json.dumps(asdict(bd_produtos[PID])))
	
	return topico, msg

def apagarProduto(PID):
	topico = "produtos/removeProduto"
	msg = ""
	if PID not in bd_produtos:
		msg = "Produto não cadastrado"	
	else: 
		bd_produtos.pop(PID)
		msg = "Produto removido"

	return topico, msg