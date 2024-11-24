import asyncio
import random
import hashlib
from datetime import datetime

CLIENTS = {}
COLORS = ["\033[91m", "\033[92m", "\033[93m", "\033[94m", "\033[95m", "\033[96m"]

def generate_unique_id(ip, port, pseudo):
    return hashlib.sha256(f"{ip}:{port}:{pseudo}".encode()).hexdigest()

async def broadcast_message(sender_addr, message, include_sender=False):
    for addr, client in CLIENTS.items():
        if not include_sender and addr == sender_addr:
            continue
        writer = client["w"]
        try:
            writer.write(message.encode())
            await writer.drain()
        except Exception as e:
            print(f"Erreur lors de l'envoi à {addr}: {e}")

async def handle_client(reader, writer):
    addr = writer.get_extra_info('peername')
    print(f"Nouvelle connexion de {addr}")

    color = random.choice(COLORS)

    try:
        data = await reader.read(1024)
        if not data:
            print(f"Connexion annulée par {addr} (aucun pseudo envoyé).")
            writer.close()
            await writer.wait_closed()
            return

        message = data.decode().strip()
        if message.startswith("Hello|"):
            pseudo = message.split("|", 1)[1].strip()
            if not pseudo:
                pseudo = "Anonyme"
        else:
            print(f"Format de message inattendu de {addr}: {message}")
            writer.close()
            await writer.wait_closed()
            return

        user_id = generate_unique_id(addr[0], addr[1], pseudo)

        if user_id in CLIENTS:
            if CLIENTS[user_id]["connected"]:
                print(f"{addr} s'est reconnecté avec le pseudo '{pseudo}'.")
                writer.write(f"Welcome back {pseudo}!\n".encode())
                await writer.drain()
                reconnect_announcement = f"Annonce : {pseudo} est de retour !\n"
                await broadcast_message(sender_addr=None, message=reconnect_announcement)
            else:
                print(f"{addr} s'est connecté avec le pseudo '{pseudo}'.")
                join_announcement = f"Annonce : {pseudo} a rejoint la chatroom.\n"
                await broadcast_message(sender_addr=None, message=join_announcement)
        else:
            print(f"{addr} s'est connecté avec le pseudo '{pseudo}'.")
            join_announcement = f"Annonce : {pseudo} a rejoint la chatroom.\n"
            await broadcast_message(sender_addr=None, message=join_announcement)

        CLIENTS[user_id] = {
            "r": reader,
            "w": writer,
            "pseudo": pseudo,
            "color": color,
            "connected": True
        }

        while True:
            data = await reader.read(1024)
            if not data:
                break

            msg = data.decode().strip()
            print(f"Message de {pseudo} ({addr}): {msg}")

            timestamp = datetime.now().strftime("[%H:%M]")
            redistrib_message = f"{timestamp} {color}{pseudo}\033[0m a dit : {msg}\n"
            await broadcast_message(sender_addr=addr, message=redistrib_message)

    except asyncio.CancelledError:
        print(f"Connexion annulée avec {addr}")
    except Exception as e:
        print(f"Erreur avec {addr}: {e}")
    finally:
        pseudo = CLIENTS.get(user_id, {}).get("pseudo", "Inconnu")
        CLIENTS[user_id]["connected"] = False
        print(f"Déconnexion de {addr} ({pseudo})")

        leave_announcement = f"Annonce : {pseudo} a quitté la chatroom.\n"
        await broadcast_message(sender_addr=None, message=leave_announcement)

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

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nServeur arrêté manuellement.")
