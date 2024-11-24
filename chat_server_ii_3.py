import asyncio

async def handle_client(reader, writer):
    
    client_address = writer.get_extra_info('peername')
    print(f"Nouvelle connexion de {client_address}")

    try:
        while True:
            data = await reader.read(1024)
            if not data:
                print(f"Connexion terminée avec {client_address}")
                break

            message = data.decode()
            print(f"Message received from {client_address[0]}:{client_address[1]} : {message}")

            response = f"Message reçu : {message}"
            writer.write(response.encode())
            await writer.drain()

    except asyncio.CancelledError:
        print(f"Connexion annulée avec {client_address}")
    except Exception as e:
        print(f"Erreur avec {client_address}: {e}")
    finally:
        writer.close()
        await writer.wait_closed()
        print(f"Connexion fermée avec {client_address}")

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
