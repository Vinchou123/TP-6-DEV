import socket

def main():
    server_address = ('10.2.2.2', 8888)
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        client_socket.connect(server_address)
        print(f"Connecté au serveur {server_address}")

        message = "Hello"
        client_socket.sendall(message.encode())

        data = client_socket.recv(1024)
        print(f"Réponse du serveur: {data.decode()}")

    finally:
        print("Fermeture de la connexion")
        client_socket.close()

if __name__ == '__main__':
    main()
