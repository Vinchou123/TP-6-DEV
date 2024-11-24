import asyncio

CLIENTS = {}

async def handle_client(reader, writer):
    addr = writer.get_extra_info('peername')
    print(f"Nouvelle connexion de {addr[0]}:{addr[1]}")

    pseudo = (await reader.readline()).decode().strip()
    
    if pseudo in CLIENTS:
        CLIENTS[pseudo]["connected"] = True
        CLIENTS[pseudo]["writer"] = writer 
        print(f"{addr[0]} s'est reconnecté avec le pseudo '{pseudo}'.")
        broadcast(f"Annonce : {pseudo} est de retour !", pseudo)
    else:
        CLIENTS[pseudo] = {
            "addr": addr,
            "writer": writer,
            "connected": True,
        }
        print(f"{addr[0]} s'est connecté avec le pseudo '{pseudo}'.")
        broadcast(f"Annonce : {pseudo} a rejoint la chatroom.", pseudo)

    try:
        while True:
            data = await reader.readline()
            if not data:
                break
            message = data.decode().strip()
            print(f"Message de {pseudo} ({addr[0]}): {message}")
            broadcast(f"[{addr[0]}] {pseudo} a dit : {message}", pseudo)
    except asyncio.CancelledError:
        pass
    finally:
        print(f"Déconnexion de {addr[0]} ({pseudo})")
        CLIENTS[pseudo]["connected"] = False
        broadcast(f"Annonce : {pseudo} a quitté la chatroom.", pseudo)
        writer.close()
        await writer.wait_closed()

def broadcast(message, sender_pseudo=None):
    """
    Envoie un message à tous les clients connectés sauf à l'expéditeur (si défini).
    """
    for pseudo, info in CLIENTS.items():
        if info["connected"] and pseudo != sender_pseudo:
            try:
                info["writer"].write(f"{message}\n".encode())
            except Exception as e:
                print(f"Erreur lors de l'envoi à {pseudo}: {e}")

async def main():
    server_ip = "10.2.2.2"
    server_port = 8888
    server = await asyncio.start_server(handle_client, server_ip, server_port)
    addr = server.sockets[0].getsockname()
    print(f"Serving on {addr}")

    async with server:
        await server.serve_forever()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nServeur arrêté.")
