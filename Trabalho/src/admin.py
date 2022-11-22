import socket 
import admin_funcoes as f
import random
import publish as pub
from paho.mqtt import client as mqtt_client

# Instância o socket
adminSocket = socket.socket()

def opcoesProduto():
	while(True):
		f.menuProduto()
		opcao = int(input())
		topico = ""

		if opcao > 5 and opcao < 10:
			if opcao == 6:
				msg = f.recuperarProduto()
				adminSocket.send(msg.encode())

			elif opcao == 7:
				msg = f.inserirProduto()
				adminSocket.send(msg.encode())
			
			elif opcao == 8:
				msg = f.modificarProduto()
				adminSocket.send(msg.encode())

			elif opcao == 9: 
				msg = f.apagarProduto()
				adminSocket.send(msg.encode())
		
			data = adminSocket.recv(1024)
			print("Receive from server: " + data.decode())
		else:
			if opcao == 10:
				return
			else:
				print("Opcao inválida. Tente novamente!")


def opcoesCliente():
	while(True):
		f.menuCliente()
		opcao = int(input())
		topico = ""

		if opcao > 0 and opcao < 5:
			if opcao == 1:
				msg = f.recuperarCliente()
				adminSocket.send(msg.encode())

			elif opcao == 2:
				msg = f.inserirCliente()
				adminSocket.send(msg.encode())
			
			elif opcao == 3:
				msg = f.modificarCliente()
				adminSocket.send(msg.encode())

			elif opcao == 4: 
				msg = f.apagarCliente()
				adminSocket.send(msg.encode())
		
			data = adminSocket.recv(1024)
			print("Receive from server: " + data.decode())
		else:
			if opcao == 5:
				return
			else:
				print("Opcao inválida! Tente novamente.")


def opcoesMenu():
	while(True):
		f.menuPrincipal()
		opcao = int(input())

		if opcao == 1:
			opcoesCliente()
		
		elif opcao == 2:
			opcoesProduto()

		elif opcao == 3:
			adminSocket.send("".encode())
			return
		
		else:
			print("Opção inválida! Tente novamente.")

def main():
	host = "127.0.0.1"            
	port = int(input("Digite o número do servidor: ")) 
	adminSocket.connect((host, port))
	opcoesMenu()
	adminSocket.close()

if __name__ == '__main__': 
	main()
