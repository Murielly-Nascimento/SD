# SD

## Divisão

O trabalho é divido nas aplicações voltadas para cliente e administrador, cada um com arquivos de testes. 
Note que o test_adminServer e assim por diante, são usados como testes automatizados das API's.

### Administrador

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



















