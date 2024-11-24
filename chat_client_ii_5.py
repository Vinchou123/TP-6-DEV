import asyncio
from aioconsole import ainput

async def send_message(writer):
    while True:
        message = await ainput("Vous : ")
        if message.strip():
            writer.write(message.encode())
            await writer.drain()

async def receive_message(reader):
    while True:
        try:
            data = await reader.read(1024)
            if not data:
                print("Connexion fermée par le serveur.")
                break
            print(f"\n{data.decode()}")
        except asyncio.CancelledError:
            break

async def main():
    server_host = "10.2.2.2"
    server_port = 8888

    print(f"Connexion au serveur {server_host}:{server_port}...")
    reader, writer = await asyncio.open_connection(server_host, server_port)

    pseudo = input("Entrez votre pseudo : ").strip()
    if not pseudo:
        print("Il vous faut un pseudo'.")
        pseudo = "Anonyme"
    writer.write(f"Hello|{pseudo}".encode())
    await writer.drain()

    print(f"Vous êtes connecté en tant que '{pseudo}'. Tapez vos messages !")

    send_task = asyncio.create_task(send_message(writer))
    receive_task = asyncio.create_task(receive_message(reader))

    try:
        await asyncio.gather(send_task, receive_task)
    except KeyboardInterrupt:
        print("\nDéconnexion...")
    finally:
        writer.close()
        await writer.wait_closed()

if __name__ == '__main__':
    asyncio.run(main())
