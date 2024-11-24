import asyncio
import random

# Dictionnaire pour gérer les clients
CLIENTS = {}

def generate_random_color():
    # Génère une couleur aléatoire au format hexadécimal
    return "#{:02x}{:02x}{:02x}".format(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

async def broadcast_message(sender_addr, message, include_sender=False):
    # Diffuse le message à tous les clients connectés
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

        # Génération d'une couleur aléatoire pour le client
        color = generate_random_color()

        CLIENTS[addr] = {
            "r": reader,
            "w": writer,
            "pseudo": pseudo,
            "color": color,  # Ajout de la couleur
        }
        print(f"{addr} s'est connecté avec le pseudo '{pseudo}' et la couleur '{color}'.")

        join_announcement = f"Annonce : {pseudo} a rejoint la chatroom.\n"
        await broadcast_message(sender_addr=None, message=join_announcement)

        while True:
            data = await reader.read(1024)
            if not data:
                break

            msg = data.decode().strip()
            print(f"Message de {pseudo} ({addr}): {msg}")

            # Envoie du message avec la couleur du client et l'heure actuelle
            timestamp = asyncio.get_event_loop().time()
            redistrib_message = f"{pseudo}|{CLIENTS[addr]['color']}|{timestamp}|{msg}\n"
            await broadcast_message(sender_addr=addr, message=redistrib_message)

    except asyncio.CancelledError:
        print(f"Connexion annulée avec {addr}")
    except Exception as e:
        print(f"Erreur avec {addr}: {e}")
    finally:
        pseudo = CLIENTS.get(addr, {}).get("pseudo", "Inconnu")
        del CLIENTS[addr]
        print(f"Déconnexion de {addr} ({pseudo})")

        leave_announcement = f"Annonce : {pseudo} a quitté la chatroom.\n"
        await broadcast_message(sender_addr=None, message=leave_announcement)

        writer.close()
        await writer.wait_closed()

async def main():
    global CLIENTS
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
