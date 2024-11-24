import asyncio
from datetime import datetime

CLIENTS = {}

async def broadcast_message(message, exclude_addr=None):
    """
    Diffuse un message à tous les clients, sauf éventuellement à un client spécifique.
    """
    for addr, client in CLIENTS.items():
        if addr == exclude_addr or client["connected"] is False:
            continue
        try:
            client["writer"].write(message.encode())
            await client["writer"].drain()
        except Exception as e:
            print(f"Erreur lors de l'envoi du message à {addr}: {e}")

async def handle_client(reader, writer):
    """
    Gère un nouveau client : connexion, messages et déconnexion.
    """
    addr = writer.get_extra_info('peername')[0]
    print(f"Nouvelle connexion de {addr}")

    if addr in CLIENTS and not CLIENTS[addr]["connected"]:
        pseudo = CLIENTS[addr]["pseudo"]
        CLIENTS[addr]["connected"] = True
        CLIENTS[addr]["reader"] = reader
        CLIENTS[addr]["writer"] = writer
        writer.write(f"Welcome back, {pseudo}!\n".encode())
        print(f"{addr} s'est reconnecté avec le pseudo '{pseudo}'.")
        await broadcast_message(f"Annonce : {pseudo} est de retour !\n", exclude_addr=None)
    else:
        writer.write(b"Entrez votre pseudo : ")
        pseudo = (await reader.read(1024)).decode().strip()
        if not pseudo:
            writer.close()
            await writer.wait_closed()
            return
        CLIENTS[addr] = {
            "pseudo": pseudo,
            "reader": reader,
            "writer": writer,
            "connected": True
        }
        print(f"{addr} s'est connecté avec le pseudo '{pseudo}'.")
        await broadcast_message(f"Annonce : {pseudo} a rejoint la chatroom.\n", exclude_addr=None)

    try:
        while True:
            data = await reader.read(1024)
            if not data:
                break
            message = data.decode().strip()
            timestamp = datetime.now().strftime("[%H:%M]")
            full_message = f"{timestamp} {pseudo} a dit : {message}\n"
            await broadcast_message(full_message, exclude_addr=addr)
    except Exception as e:
        print(f"Erreur avec {addr}: {e}")
    finally:
        if addr in CLIENTS:
            CLIENTS[addr]["connected"] = False
            print(f"Déconnexion de {addr} ({pseudo})")
            await broadcast_message(f"Annonce : {pseudo} a quitté la chatroom.\n", exclude_addr=None)
        writer.close()
        await writer.wait_closed()

async def main():
    server = await asyncio.start_server(handle_client, "10.2.2.2", 8888)
    addr = server.sockets[0].getsockname()
    print(f"Serving on {addr}")

    async with server:
        await server.serve_forever()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nServeur arrêté.")
