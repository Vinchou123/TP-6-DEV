import asyncio

async def handle_client(reader, writer):
    addr = writer.get_extra_info('peername')
    client_ip, client_port = addr

    data = await reader.read(1024)
    message = data.decode()

    print(f"Message du client ({client_ip}:{client_port}): {message}")

    response = f"Hello {client_ip}:{client_port}"
    writer.write(response.encode())
    await writer.drain()

    print(f"Réponse envoyée à {client_ip}:{client_port}")
    writer.close()

async def main():
    server = await asyncio.start_server(
        handle_client, '10.2.2.2', 8888)  

    addr = server.sockets[0].getsockname()
    print(f'Serving on {addr}')

    async with server:
        await server.serve_forever()

if __name__ == '__main__':
    asyncio.run(main())
