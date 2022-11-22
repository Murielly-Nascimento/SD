# SD

O trabalho é divido nas aplicações voltadas para cliente e administrador, cada um com arquivos de testes. 

  * [Modelagem dos Dados](#modelagem-dos-dados)
  * [Portais Cliente e Administrador](#portais-cliente-e-administrador)
  * [APIs](#apis)
  * [Protocolo MQTT](#protocolo-mqtt)
  * [Administrador e Cliente](#administrador-e-cliente)
  * [Funcionalidades do Administrador e Cliente](#funcionalidades-do-administrador-e-cliente)
  * [Testes Automatizados](#testes-automatizados)

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
## APIs

As APIs do cliente e do administrador são definidas no arquivo admin_api.py e cliente_api.py. Ambas usam tabelas hash locais como Banco de Dados. E cada função define um tópico e uma mensagem a ser retornada.

```python
# BD

bd_clientes = {}
bd_produtos = {}
bd_pedidos = {}

# Clients
		
def recuperarCliente(CID):
	topico = "clientes/getCliente"
	msg = ""

	if CID not in bd_clientes:
		msg = "Cliente não encontrado"
	else: 
		msg = str(json.dumps(asdict(bd_clientes[CID])))

	return topico, msg
```

## Protocolo MQTT

O portal Administrador publica nos tópicos Cadastro, Modificação e Remoção de Produtos e Clientes, através do arquivo publish.py. E o portal Cliente se inscreve nesses mesmos tópicos através do arquivo publish.py

```python
def publish(client, topico, msg):
	result = client.publish(topico, msg)
	status = result[0]
	if status == 0:
		print(f"\nPublicado no topico: `{topico}` a mensagem: `{msg}` \n")
	else:
		print(f"Falha ao enviar mensagem para o topico: {topico}\n")

def subscribe(client: mqtt_client, topic):
	def on_message(client, userdata, msg):
		print(f"\nRecebido do topico `{msg.topic}` a mensagem: `{msg.payload.decode()}` \n")

		if msg.topic == "clientes/cadCliente":
			api.salvarCliente(msg.payload.decode())
		elif msg.topic == "clientes/removeCliente":
			api.removerCliente(msg.payload.decode())
		elif msg.topic == "produtos/cadProduto":
			api.salvarProduto(msg.payload.decode())
		elif msg.topic == "produtos/removeProduto":
			api.removerProduto(msg.payload.decode())
		elif msg.topic == "produtos/putProduto":
			api.atualizarProduto(msg.payload.decode())

	client.subscribe(topic)
	client.on_message = on_message
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





