from dataclasses import dataclass
from collections import namedtuple
from typing import Any
import json

# Classes DTO

@dataclass
class Mensagem:
	funcao: str
	id: str
	dados: 'Any'

	def __init__(self, funcao, id, dados=""):
		self.funcao = funcao
		self.id = id
		self.dados = dados

	def mensagemDecoder(obj):
		return namedtuple('Mensagem', obj.keys())(*obj.values())

@dataclass
class ClienteDTO:
	nome: str
	email: str
	senha:str

	def __init__(self, nome, email, senha):
		self.nome = nome
		self.email = email
		self.senha = senha

	def clienteDecoder(obj):
		return namedtuple('Cliente', obj.keys())(*obj.values())

@dataclass
class ProdutoDTO:
	titulo: str
	descricao: str
	quantidade: int
	preco: float

	def __init__(self, titulo, descricao, quantidade=1, preco=50):
		self.titulo = titulo
		self.descricao = descricao
		self.quantidade = quantidade
		self.preco = preco
	
	def encode(self):
		return self.__dict__
	
	def produtoDecoder(obj):
		return namedtuple('Produto', obj.keys())(*obj.values())


@dataclass
class PedidoDTO:
	OID: str
	quantidade: int
	custo: float
	PID: str
	CID: str

	def __init__(self, OID, quantidade, custo, PID, CID):
		self.OID = OID
		self.quantidade = quantidade
		self.custo = custo
		self.PID = PID
		self.CID = CID
		
	
	def toJSON(self):
		return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)
