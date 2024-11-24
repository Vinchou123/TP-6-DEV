import asyncio
from aioconsole import ainput

async def send_message(writer):
    while True:
        message = await ainput("\rVous : ")
        if message.strip():
            writer.write(message.encode())
            await writer.drain()

async def receive_message(reader):
    while True:
        data = await reader.read(1024)
        if not data:
            print("\nConnexion fermée par le serveur.")
            raise SystemExit("La connexion au serveur a été perdue.")
        print(f"\r{data.decode()}\n", end="")
        print("\rVous : ", end="", flush=True)

async def main():
    server_host = "10.2.2.2"
    server_port = 8888

    print(f"Connexion au serveur {server_host}:{server_port}...")
    try:
        reader, writer = await asyncio.open_connection(server_host, server_port)

        pseudo = input("Entrez votre pseudo : ").strip()
        if not pseudo:
            print("Il vous faut un pseudo.")
            pseudo = "Anonyme"
        writer.write(f"Hello|{pseudo}".encode())
        await writer.drain()

        print(f"Vous êtes connecté en tant que '{pseudo}'. Tapez votre message !")

        send_task = asyncio.create_task(send_message(writer))
        receive_task = asyncio.create_task(receive_message(reader))

        await asyncio.gather(send_task, receive_task)
    except ConnectionRefusedError:
        print(f"Impossible de se connecter au serveur {server_host}:{server_port}")
    except asyncio.CancelledError:
        print("\nLa connexion au serveur a été perdue.")
    finally:
        print("\nClient arrêté manuellement.")
        try:
            writer.close()
            await writer.wait_closed()
        except NameError:
            pass

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nFermeture de la connexion.")
    except SystemExit:
        print("\nL'application a été fermée en raison de la déconnexion du serveur.")
