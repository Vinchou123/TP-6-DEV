import asyncio
from aioconsole import ainput
from datetime import datetime

async def send_message(writer):
    while True:
        message = await ainput("\rVous : ")
        if message.strip():
            writer.write(message.encode())
            await writer.drain()
            print(f"\rVous avez dit : {message}\n", end="")
            print("\rVous : ", end="", flush=True)

async def receive_message(reader, stop_event):
    while True:
        data = await reader.read(1024)
        if not data:
            print("\nConnexion fermée par le serveur.")
            stop_event.set()
            break
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

        stop_event = asyncio.Event()

        send_task = asyncio.create_task(send_message(writer))
        receive_task = asyncio.create_task(receive_message(reader, stop_event))

        await stop_event.wait()

        send_task.cancel()
        receive_task.cancel()

        await asyncio.gather(send_task, receive_task, return_exceptions=True)

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
