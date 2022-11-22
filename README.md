# SD

O trabalho é divido nas aplicações voltadas para cliente e administrador, cada um com arquivos de testes. 
Note que o test_adminServer e assim por diante, são usados como testes automatizados das API's.

## Modelagem dos Dados

As aplicações Cliente e Administrador usam os modelos de dados descritos no arquivo model.py. Note que o contexto de uma livraria é simulado pelo programa.

A classe Cliente, consiste no nome, e-mail e senha do usuário. Sendo que o ID do cliente é o seu e-mail. Quanto ao produto, os atributos são o Título do livro, a descrição ou sinopse do livro, a quantidade dele no estoque e o seu preço. O seu ID é o título do livro. Cada Pedido é composto pela quantidade do Produto (Livro) que será pedido, o custo que é o preço do livro multiplicado pela quantidade solicitada, o Cliente que solicitou o pedido e o Produto propriamente dito.

A classe Mensagem é usada para a comunicação entre os usuários e os portais. Assim, temos a função que foi chamada, exemplo cadastrarCliente, o ID, seja o do Produto, Pedido ou Cliente, e os dados da mensagem, que podem ou não ser usados, geralmente são objetos das demais classes.


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

## Portais Cliente e Administrador

A comunicação entre portal e cliente é feita por meio de sockets. E entre os Portais pelo protocolo MQTT.

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













