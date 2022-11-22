from functools import lru_cache
from model import Cliente, Produto, Pedido
from dataclasses import asdict
from typing import Any
import random
import json
# BD

bd_clientes = {}
bd_produtos = {}
bd_pedidos = {}

# Valores de exemplo
clienteTeste = Cliente("Elena","elena@gmail.com","123456")
produtoTeste = Produto("Alice","Alice no Pais das Maravilhas")
pedidoTeste = Pedido(1,produtoTeste,clienteTeste)

bd_clientes[clienteTeste.email] = clienteTeste
bd_produtos[produtoTeste.titulo] = produtoTeste

aux = {}
aux[1] = pedidoTeste
bd_pedidos[clienteTeste.email] = aux

# Cache

# Clients

def autenticarCliente(CID, dados: Any):
	topico = "clientes/authCliente"
	msg = ""

	if CID not in bd_clientes:
		msg = "Cliente não encontrado!"

	elif bd_clientes[CID].senha != dados.senha:  
		msg = "Senha incorreta!"
	
	else:
		msg = "Cliente autenticado"
	
	return topico, msg

def salvarCliente(dados):
	dados = json.loads(dados, object_hook=Cliente.clienteDecoder)
	dadosCliente = Cliente(dados.nome, dados.email, dados.senha)
	bd_clientes[dados.email] = dadosCliente

def removerCliente(CID):
	bd_clientes.pop(CID)

# Produtos

def salvarProduto(dados):
	dados = json.loads(dados, object_hook=Produto.produtoDecoder)
	dadosProduto = Produto(dados.titulo, dados.descricao, dados.quantidade, dados.preco)
	bd_produtos[dados.titulo] = dadosProduto

def removerProduto(CID):
	bd_clientes.pop(CID)

def atualizarProduto(dados):
	dados = json.loads(dados, object_hook=Produto.produtoDecoder)
	dadosProduto = Produto(dados.titulo, dados.descricao, dados.quantidade, dados.preco)
	bd_produtos[dados.titulo] = dadosProduto

# Pedidos

def criarPedido(CID, PID):
	topico = "pedidos/cadPedido"
	msg = ""
	if PID not in bd_produtos:
		msg = "Este título não está no catálogo."
	else:
		produto = bd_produtos[PID]
		cliente = bd_clientes[CID]
		pedido = Pedido(1,produto,cliente)

		bd_produtos[PID].quantidade = bd_produtos[PID].quantidade - 1
		OID = random.randint(0, 1000)
		aux = {}
		pedido.OID = OID
		aux[OID] = pedido

		if CID not in bd_pedidos:	
			bd_pedidos[CID] = aux
		else:
			bd_pedidos[CID].update(aux)

		msg = f"Pedido cadastrado com sucesso. O OID é {OID}"
	
	return topico, msg

def modificarPedido(CID, dados: Any):
	topico = "pedidos/putPedido"
	msg = ""

	OID = dados.OID
	PID = dados.produto
	qtdEmEstoque = bd_produtos[PID].quantidade

	if CID not in bd_pedidos:
		msg = "Este cliente não possui pedidos em andamento."
	elif OID not in bd_pedidos[CID]:
		msg = "Pedido não cadastrado"
	elif PID not in bd_produtos:
		msg = "Título não cadastrado"
	elif qtdEmEstoque < dados.quantidade:
		msg = "Estoque insuficiente"
	else:
		# Resetar o estoque do produto que estava no pedido
		antigoPID = bd_pedidos[CID][OID].produto.titulo
		bd_produtos[antigoPID].quantidade =  bd_produtos[antigoPID].quantidade + bd_pedidos[CID][OID].produto.quantidade

		# Atualizo o pedido
		bd_pedidos[CID][OID].produto = bd_produtos[PID]
		bd_pedidos[CID][OID].quantidade = dados.quantidade
		bd_pedidos[CID][OID].custo = bd_produtos[PID].preco * dados.quantidade

		# Caso esse seja o ultimo pedido feito deste produto antes que ele acabe
		# if qtdEmEstoque == dados.quantidade:
		#	bd_produtos.pop(PID)

		msg = "Pedido atualizado com sucesso"

	return topico, msg

def listarPedido(CID, OID):
	topico = "pedidos/getPedido"
	msg = ""

	if CID not in bd_pedidos:
		msg = "Este cliente não possui pedidos em andamento."
	elif OID not in bd_pedidos[CID]:
		msg = "Pedido não cadastrado"
	else:
		pedido = bd_pedidos[CID][OID]
		msg = str(pedido.toJSON())

	return topico, msg

def listarPedidos(CID):
	topico = "pedidos/listPedido"
	msg = ""

	if CID not in bd_pedidos:
		msg = "Este cliente não possui pedidos em andamento."
	else:
		pedidos = bd_pedidos[CID]
		dados = ""
		for pedido in pedidos:
			dados = dados + Pedido.toJSON(bd_pedidos[CID][pedido])
		msg = dados

	return topico, msg

def apagarPedido(CID, OID):
	topico = "pedidos/removePedido"
	msg = ""

	if CID not in bd_pedidos:
		msg = "Este cliente não possui pedidos em andamento."
	elif OID not in bd_pedidos[CID]:
		msg = "Pedido não cadastrado"
	else:
		# Resetar o estoque do produto que estava no pedido
		PID = bd_pedidos[CID][OID].produto.titulo
		bd_produtos[PID].quantidade =  bd_produtos[PID].quantidade + bd_pedidos[CID][OID].produto.quantidade

		# Atualizo o pedido
		bd_pedidos[CID].pop(OID)

		msg = "Pedido cancelado com sucesso"

	return topico, msg