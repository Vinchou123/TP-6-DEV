import asyncio

CLIENTS = {}

async def broadcast_message(sender_addr, message):
    for addr, client in CLIENTS.items():
        if addr != sender_addr:
            writer = client["w"]
            try:
                formatted_message = f"{sender_addr[0]}:{sender_addr[1]} a dit : {message}"
                writer.write(formatted_message.encode())
                await writer.drain()
            except Exception as e:
                print(f"Erreur lors de l'envoi à {addr}: {e}")


async def handle_client(reader, writer):

    addr = writer.get_extra_info('peername')
    print(f"Nouvelle connexion de {addr}")

    if addr not in CLIENTS:
        CLIENTS[addr] = {"r": reader, "w": writer}
    
    try:
        while True:
            data = await reader.read(1024)
            if not data:
                print(f"Déconnexion de {addr}")
                break

            message = data.decode()
            print(f"Message received from {addr[0]}:{addr[1]} : {message}")

            await broadcast_message(addr, message)
    
    except asyncio.CancelledError:
        print(f"Connexion annulée avec {addr}")
    except Exception as e:
        print(f"Erreur avec {addr}: {e}")
    finally:
        writer.close()
        await writer.wait_closed()
        if addr in CLIENTS:
            del CLIENTS[addr]
        print(f"Connexion fermée avec {addr}")

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
