# SD

O trabalho é divido nas aplicações voltadas para cliente e administrador, cada um com arquivos de testes. 

  * [Modelagem dos Dados](#modelagem-dos-dados)
  * [Portais Cliente e Administrador](#portais-cliente-e-administrador)
  * [APIs](#apis)
  * [Banco de dados LMDB](#banco-de-dados-lmdb)
  * [Administrador e Cliente](#administrador-e-cliente)
  * [Funcionalidades do Administrador e Cliente](#funcionalidades-do-administrador-e-cliente)
  * [Testes Automatizados](#testes-automatizados)

## Modelagem dos Dados

As aplicações Cliente e Administrador usam os modelos de dados descritos no arquivo model.py. Note que o contexto de uma livraria é simulado pelo programa.

A classe Cliente, consiste no nome, e-mail e senha do usuário. Sendo que o ID do cliente é o seu e-mail. Quanto ao produto, os atributos são o Título do livro, a descrição ou sinopse do livro, a quantidade dele no estoque e o seu preço. O seu ID é o título do livro. Cada Pedido é composto pela quantidade do Produto (Livro) que será pedido, o custo que é o preço do livro multiplicado pela quantidade solicitada, o Cliente que solicitou o pedido e o Produto propriamente dito.

A classe Mensagem é usada para a comunicação entre os usuários e os portais. Assim, temos a função que foi chamada, exemplo cadastrarCliente, o ID, seja o do Produto, Pedido ou Cliente, e os dados da mensagem, que podem ou não ser usados, geralmente são objetos das demais classes.

O padrão DTO foi implementado para melhor organização do projeto. Logo as classes para transferências de dados são definidas no arquivo dto.py.


```python
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

```

As classes para transações no banco de dados ficam no arquivo model.py

```python
# Classes BD

class Ident(Array):
	_length_ = 36
	_type_ = c_char

class Cliente(Structure):
	_fields_ = [
		('nome', Ident),
		('email', Ident),
		('senha', Ident)
	]

	def __repr__(self):
		return f"{self.__class__.__name__}({', '.join(['='.join([key, str(val)]) for key, val in self.as_dict.items()])})"


class Produto(Structure):
	_fields_ = [
		('titulo', Ident),
		('descricao', Ident),
		('quantidade', c_int),
		('preco', c_double)
	]

	def __repr__(self):
		return f"{self.__class__.__name__}({', '.join(['='.join([key, str(val)]) for key, val in self.as_dict.items()])})"

class Pedido(Structure):
	_fields_ =[
		('OID', Ident),
		('quantidade', c_int),
		('custo', c_double),
		('PID', Ident),
		('CID', Ident)
	]

	def __repr__(self):
		return f"{self.__class__.__name__}({', '.join(['='.join([key, str(val)]) for key, val in self.as_dict.items()])})"

class AsDictMixin:
    @property
    def as_dict(self):
        d = {}
        for (key, _) in self._fields_:
            if isinstance(getattr(self, key), AsDictMixin):
                d[key] = getattr(self, key).as_dict
            elif isinstance(getattr(self, key), bytes):
                d[key] = getattr(self, key).decode()
            else:
                d[key] = getattr(self, key)
        return d
```

## Portais Cliente e Administrador

A comunicação entre portal e cliente é feita por meio de sockets.

Os arquivos admin_server.py e cliente_server.py contém toda a configuração dos sockets para envio e recebimento de Mensagens.

Não há restrições para os portais. A cada execução do código admin_server.py é solicitado um número de porta diferente para que não haja conflitos. Quanto as conexões aceitas por cada portal deixei definido um limite de 5, esse número pode ser alterado.

```python
	try:
		# Configuração do Socket
		serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		host = "127.0.0.1"            
		port = int(input("Digite o número da porta: ")) 
		print("Lembre-se que esse número será usado ao administradores se conectarem")
		serverSocket.bind((host, port))
	except socket.error as e:
		print(str(e))
		return
		
	print("\n<< Portal Administrador >>\n")
	print("Servidor conectado ao host: " + host + " na porta: " + str(port))

	serverSocket.listen(5)
```

A função API nesses arquivos deserializa a Mensagem enviada pelo cliente e determina qual operação da API será acionada. O retorno de cada uma dessas funções é repassado para o cliente.

```python
def API(conn, data, adminMQTT):

	try:
		mensagem = json.loads(data, object_hook=Mensagem.mensagemDecoder)
	except:
		print("Erro ao decodificar mensagem recebida do administrador")
	else:
		opcao = mensagem.funcao

		if opcao == "recuperarCliente":
			CID = mensagem.id
			topico, msg = admin_api.recuperarCliente(CID)
		
		print("Enviado do topico " + topico + " a mensagem " + msg + "\n")
		conn.send(msg.encode())
```
## APIs

As APIs do cliente e do administrador são definidas no arquivo admin_api.py e cliente_api.py. E cada função define um tópico e uma mensagem a ser retornada.

```python
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
```

## Banco de Dados LMDB

A implementação do banco de dados foi feita usando o LMDB e sua implemtação fica nos arquivos admin_api.py e client_api.py

```python
clienteBD = lmdb.Environment("cliente.lmdb", map_size=Gi, subdir=True, readonly=False, metasync=True, sync=True,
                           map_async=False, mode=493, create=True, readahead=True, writemap=True, meminit=True,
                           max_readers=126, max_dbs=2, max_spare_txns=1, lock=True)
			   
			   
produtoBD = lmdb.Environment("produto.lmdb", map_size=Gi, subdir=True, readonly=False, metasync=True, sync=True,
                           map_async=False, mode=493, create=True, readahead=True, writemap=True, meminit=True,
                           max_readers=126, max_dbs=2, max_spare_txns=1, lock=True)
			   
pedidoBD = lmdb.Environment("pedido.lmdb", map_size=Gi, subdir=True, readonly=False, metasync=True, sync=True,
                           map_async=False, mode=493, create=True, readahead=True, writemap=True, meminit=True,
                           max_readers=126, max_dbs=2, max_spare_txns=1, lock=True)
```

## Administrador e Cliente

As funcionalidades dos usuários de ambas as aplicações (Cliente e Administrador) são definidas nos arquivos cliente.py e admin.py. A configuração dos sockets para envio e recebimento de informação também é feita nesses arquivos. E em ambos os casos é solicitado o número da porta em que o servidor está rodando.

```python
	host = "127.0.0.1"            
	port = int(input("Digite o número da porta: "))
	clientSocket.connect((host, port))
	login()
	clientSocket.close()
```

## Funcionalidades do Administrador e Cliente

As funcionalidades dos administradores e cliente são definidas nos arquivos admin_funcoes.py e cliente_funcoes.py. Em ambos os casos Menus interativos foram definidos para organização do código.

```python
def menuPrincipal():
	print("\n<< Administrador da Livraria Lovelace >>")
	print("1 - Manipular Clientes")
	print("2 - Manipular Produtos")
	print("3 - Sair")
	print("Digite uma opcao: ",end="") 
	
def menuPrincipal():
	print("\n<< Cliente >>")
	print("1 - Inserir Pedido")
	print("2 - Modificar Pedido")
	print("3 - Enumerar Pedido")
	print("4 - Enumerar Pedidos")
	print("5 - Cancelar Pedido")
	print("6 - Sair")
	print("Digite uma opcao: ",end="") 
```

Cada função solicita que o usuário preencha uma sequência de informações que serão convertidas em um objeto Mensagem que posteriormente será enviado para o servidor.

```python
def autentica():
	print("\n<< Bem vindo a Livraria Lovelace >>\n")
	nome = input("Digite seu nome: ")
	email = input("Digite seu email: ")
	senha = input("Digite sua senha: ")

	cliente = Cliente(nome,email,senha)
	msg = Mensagem("autenticarCliente",email,cliente)
	msg = str(json.dumps(asdict(msg)))

	return msg, email
```

## Testes Automatizados

Os testes automatizados de ambas as aplicações Cliente e Administrador são definidos nos arquivos com prefixo test. Para cada caso a um file para o servidor e o cliente que devem ser executadas. Todas as operações da API são testadas e os códigos de erro ou sucesso são enviados do Servidor para o Cliente.

## Compilação

Inicializar o sevidor do administrador
```
python admin_server.py
```

Inicializar o Administrador
```
python admin.py
```

Inicializar o servidor do cliente
```
python client_server.py
```

Inicializar o cliente
```
python client.py
```

OBS: Recomendável inicializar o servidor cliente e administrador ao mesmo tempo para garantir a conexão MQTT entre ambos.




