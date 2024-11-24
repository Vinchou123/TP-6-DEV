import asyncio
import os

PSEUDO_FILE = "/tmp/chat_pseudo.txt"


async def main():
    """
    Client de chat qui se connecte au serveur et permet d'envoyer des messages.
    """
    server_ip = "10.2.2.2"
    server_port = 8888

    try:
        reader, writer = await asyncio.open_connection(server_ip, server_port)
        print(f"Connexion au serveur {server_ip}:{server_port}...")

        if os.path.exists(PSEUDO_FILE):
            with open(PSEUDO_FILE, "r") as f:
                pseudo = f.read().strip()
        else:
            pseudo = input("Entrez votre pseudo : ").strip()
            with open(PSEUDO_FILE, "w") as f:
                f.write(pseudo)

        writer.write(f"{pseudo}\n".encode())
        await writer.drain()
        print(f"Vous êtes connecté en tant que '{pseudo}'. Tapez votre message !")

        async def send_messages():
            while True:
                message = input("Vous : ").strip()
                if message.lower() == "exit":
                    print("Déconnexion...")
                    break
                writer.write(f"{message}\n".encode())
                await writer.drain()

        async def read_messages():
            while True:
                data = await reader.read(1024)
                if not data:
                    break
                print(data.decode(), end="")

        await asyncio.gather(send_messages(), read_messages())

    except ConnectionRefusedError:
        print("Connexion refusée. Vérifiez que le serveur est actif.")
    except KeyboardInterrupt:
        print("\nDéconnexion...")
    finally:
        if writer:
            writer.close()
            await writer.wait_closed()
        print("Client arrêté.")


if __name__ == "__main__":
    asyncio.run(main())
