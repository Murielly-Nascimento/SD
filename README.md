# SD

O trabalho é divido nas aplicações voltadas para cliente e administrador, cada um com arquivos de testes. 
Note que o test_adminServer e assim por diante, são usados como testes automatizados das API's.

## Modelagem dos Dados

Para conversão dos objetos e organização do código, o arquivo model.py informa
as classes usadas pelos clientes e administradores.

```python
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
class Cliente:
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
class Produto:
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
class Pedido:
	quantidade: int
	custo: float
	produto: Produto
	cliente: Cliente
	OID: int

	def __init__(self, quantidade, produto: Produto, cliente:Cliente):
		self.quantidade = quantidade
		self.custo = produto.preco * quantidade
		self.produto = produto
		self.OID = 1
	
	def toJSON(self):
		return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

```


## Aplicação Administrador

### Portal Administrador

Começamos por inicializar o portal do Administrador. Ele permite que até 5 conexões sejam feitas (o número pode ser alterado)
E que múltiplos portais sejam abertos. Para isso, o programa pede ao usuário que insira o número da porta.
Assim a todo portal é executado em uma porta diferente. Note que este mesmo número deverá ser usado pelos
administradores que desejam se conectar a um portal.

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

Para comunicação ente o portal Administrador e Cliente usei o protocolo MQTT as configurações dele são como segue:

```python
	# Configurações MQTT para comunicação com o cliente
	adminMQTT = pub.connectMQTT()
	adminMQTT.loop_start()
```

### Administrador

O administrador, como mencionado anteriormente, deve informar o número do servidor 
(o número da porta que o servidor Administrador está usando). Toda a configuração de sockets e comunicação com o servidor
é feita pelo arquivo admin.py

```python
	host = "127.0.0.1"            
	port = int(input("Digite o número do servidor: ")) 
	adminSocket.connect((host, port))
	opcoesMenu()
	adminSocket.close()
```

As casos de uso do administrador são descritos pelo arquivo admin_funcoes.py 
Os seguintes menus descrevem as funcões usadas.

```python
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
```

Cada função do administrador pede que o usuário preencha determinadas informações.
Com elas inicializamos uma Mensagem que será enviado ao servidor por meio do socket.

```python
def inserirCliente():
	nome = input("Nome do cliente: ")
	email = input("Email do cliente: ")
	senha = input("Senha do cliente: ")

	cliente = Cliente(nome,email,senha)

	msg = Mensagem("inserirCliente",email,cliente)
	msg = str(json.dumps(asdict(msg)))

	return msg
```














