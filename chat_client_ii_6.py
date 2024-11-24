import asyncio
import aioconsole

async def send_messages(writer):
    try:
        while True:
            message = await aioconsole.ainput("Vous : ")
            if message.strip():
                if writer.is_closing():
                    print("\nConnexion déjà fermée, impossible d'envoyer le message.")
                    break
                writer.write(message.encode())
                await writer.drain()
    except (asyncio.CancelledError, ConnectionResetError) as e:
        print("\nErreur de connexion ou arrêt de la saisie utilisateur :", e)

async def receive_messages(reader):
    try:
        while True:
            data = await reader.read(1024)
            if not data:
                print("Serveur déconnecté. Fermeture du client.")
                break
            print(f"\r{data.decode()}\n", end="")
            print("\rVous : ", end="", flush=True)
    except asyncio.CancelledError:
        print("\nArrêt de la réception des messages.")
    except Exception as e:
        print(f"Erreur de réception des messages : {e}")
        return

async def main():
    server_host = "10.2.2.2"
    server_port = 8888

    print(f"Connexion au serveur {server_host}:{server_port}...")
    try:
        reader, writer = await asyncio.open_connection(server_host, server_port)
    except (ConnectionRefusedError, asyncio.TimeoutError) as e:
        print(f"Impossible de se connecter au serveur : {e}")
        return

    pseudo = input("Entrez votre pseudo : ").strip()
    if not pseudo:
        pseudo = "Anonyme"
    writer.write(f"Hello|{pseudo}".encode())
    await writer.drain()

    print(f"Vous êtes connecté en tant que '{pseudo}'. Tapez votre message !")
    
    send_task = asyncio.create_task(send_messages(writer))
    receive_task = asyncio.create_task(receive_messages(reader))

    try:
        await asyncio.gather(send_task, receive_task)
    except asyncio.CancelledError:
        pass
    finally:
        send_task.cancel()
        receive_task.cancel()
        await send_task
        await receive_task
        print("\nArrêt de la réception des messages.")

    print("Client arrêté manuellement.")
    
    if not writer.is_closing():
        writer.close()
        await writer.wait_closed()

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nFermeture de la connexion.")
