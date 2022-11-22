import random
from paho.mqtt import client as mqtt_client

# Configuracoes MQTT
broker = 'broker.emqx.io'
port = 1883

adminId = f'python-mqtt-{random.randint(0, 1000)}'
username = 'emqx'
password = 'public'

def connectMQTT():
	def on_connect(client, userdata, flags, rc):
		if rc == 0:
			print("Conectado ao MQTT Broker")
		else:
			print("Falha de conexão, codigo de erro:  %d\n", rc)
            
	client = mqtt_client.Client(adminId)
	client.username_pw_set(username, password)
	client.on_connect = on_connect
	client.connect(broker, port)
	return client


def publish(client, topico, msg):
	result = client.publish(topico, msg)
	status = result[0]
	if status == 0:
		print(f"\nPublicado no topico: `{topico}` a mensagem: `{msg}` \n")
	else:
		print(f"Falha ao enviar mensagem para o topico: {topico}\n")
