import asyncio
from aioconsole import ainput



async def async_input(writer):
    try:
        while True:
            user_input = await ainput("Vous : ")
            if user_input.strip():
                writer.write(user_input.encode())
                await writer.drain()
    except asyncio.CancelledError:
        print("Arrêt de la saisie utilisateur.")

async def async_receive(reader):
    try:
        while True:
            data = await reader.read(1024)
            if not data:
                print("Connexion avec le serveur fermée.")
                break
            print(f"\nServeur : {data.decode()}\nVous : ", end="")
    except asyncio.CancelledError:
        print("Arrêt de la réception des messages.")

async def main():
    host = "10.2.2.2"
    port = 8888

    try:
        reader, writer = await asyncio.open_connection(host, port)
        print(f"Connecté au serveur {host}:{port}")

        tasks = [
            asyncio.create_task(async_input(writer)),
            asyncio.create_task(async_receive(reader))
        ]

        await asyncio.gather(*tasks)
    except ConnectionRefusedError:
        print(f"Impossible de se connecter au serveur {host}:{port}")
    except asyncio.CancelledError:
        print("\nClient arrêté par l'utilisateur.")
    finally:
        print("Fermeture de la connexion.")
        writer.close()
        await writer.wait_closed()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nArrêt du client (CTRL + C).")
