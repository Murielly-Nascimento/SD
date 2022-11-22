import random
import client_api as api
from paho.mqtt import client as mqtt_client

broker = 'broker.emqx.io'
port = 1883

client_id = f'python-mqtt-{random.randint(0, 100)}'
username = 'emqx'
password = 'public'


def connectMQTT() -> mqtt_client:
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connectado ao MQTT Broker!")
        else:
            print("Falha de conexão, codigo de erro:  %d\n", rc)

    client = mqtt_client.Client(client_id)
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client


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
