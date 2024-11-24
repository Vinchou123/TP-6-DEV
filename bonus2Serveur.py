import asyncio
import random
from datetime import datetime

CLIENTS = {}
COLORS = ["\033[91m", "\033[92m", "\033[93m", "\033[94m", "\033[95m", "\033[96m"]

async def broadcast_message(sender_addr, message, include_sender=False):
    for addr, client in CLIENTS.items():
        if not include_sender and addr == sender_addr:
            continue
        writer = client["writer"]
        try:
            writer.write(message.encode())
            await writer.drain()
        except Exception as e:
            print(f"Erreur lors de l'envoi à {addr}: {e}")

async def handle_client(reader, writer):
    addr = writer.get_extra_info('peername')[0]
    print(f"Nouvelle connexion de {addr}")

    if addr in CLIENTS:
        pseudo = CLIENTS[addr]["pseudo"]
        writer.write(f"Welcome back, {pseudo}!\n".encode())
        await writer.drain()
        print(f"{addr} se reconnecte avec le pseudo '{pseudo}'.")
    else:
        writer.write(b"Entrez votre pseudo : ")
        data = await reader.read(1024)
        pseudo = data.decode().strip()
        if not pseudo:
            writer.close()
            await writer.wait_closed()
            return

        color = random.choice(COLORS)
        CLIENTS[addr] = {
            "reader": reader,
            "writer": writer,
            "pseudo": pseudo,
            "color": color
        }
        print(f"{addr} s'est connecté avec le pseudo '{pseudo}'.")

        join_message = f"Annonce : {pseudo} a rejoint la chatroom.\n"
        await broadcast_message(sender_addr=None, message=join_message)

    try:
        while True:
            data = await reader.read(1024)
            if not data:
                break
            msg = data.decode().strip()
            timestamp = datetime.now().strftime("[%H:%M]")
            redistrib_message = f"{timestamp} {CLIENTS[addr]['color']}{pseudo}\033[0m a dit : {msg}\n"
            await broadcast_message(sender_addr=addr, message=redistrib_message)

    except Exception as e:
        print(f"Erreur avec {addr}: {e}")
    finally:
        pseudo = CLIENTS[addr]["pseudo"]
        print(f"Déconnexion de {addr} ({pseudo})")
        del CLIENTS[addr]

        leave_message = f"Annonce : {pseudo} a quitté la chatroom.\n"
        await broadcast_message(sender_addr=None, message=leave_message)

        writer.close()
        await writer.wait_closed()

async def main():
    server_host = "10.2.2.2"
    server_port = 8888

    server = await asyncio.start_server(handle_client, server_host, server_port)
    addr = server.sockets[0].getsockname()
    print(f"Serving on {addr}")

    async with server:
        await server.serve_forever()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nServeur arrêté manuellement.")
