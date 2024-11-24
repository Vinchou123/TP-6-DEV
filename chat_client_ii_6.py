import asyncio
import aioconsole

async def send_messages(writer):
    while True:
            message = await aioconsole.ainput("Vous : ")
            if message.strip():
                writer.write(message.encode())
                await writer.drain()
        

async def receive_messages(reader):
    try:
        while True:
            data = await reader.read(1024)
            if not data:
                print("Serveur déconnecté. Fermeture du client.")
                break
            print(data.decode().strip())
    except asyncio.CancelledError:
        pass

async def main():
    server_host = "10.2.2.2"
    server_port = 8888

    try:
        reader, writer = await asyncio.open_connection(server_host, server_port)
    except Exception as e:
        print(f"Impossible de se connecter au serveur : {e}")
        return

    pseudo = input("Entrez votre pseudo : ").strip()
    if not pseudo:
        pseudo = "Anonyme"
    writer.write(f"Hello|{pseudo}".encode())
    await writer.drain()

    print(f"Connecté au serveur en tant que '{pseudo}'. Tapez votre message !")

    try:
        send_task = asyncio.create_task(send_messages(writer))
        receive_task = asyncio.create_task(receive_messages(reader))
        await asyncio.gather(send_task, receive_task)
    except asyncio.CancelledError:
        print("Client arrêté manuellement.")
    finally:
        writer.close()
        await writer.wait_closed()

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nFermeture de la connexion.")
