import asyncio
import sys
import os
import aiohttp # type: ignore
import aiofiles # type: ignore

async def get_content(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            resp.raise_for_status()
            return await resp.text()
            


async def write_content(content, file):
    async with aiofiles.open(file, "w") as out:
        await out.write(content)
        await out.flush()

def main():
    if len(sys.argv) != 2:
        print("Usage: python web_sync.py <URL>")
        sys.exit(1)

    url = sys.argv[1]
    output_dir = os.path.join(os.sep, "tmp", "web_page")
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, "page.html")

    
    content = asyncio.run(get_content(url))
    asyncio.run(write_content(content, output_file)) 

#
if __name__ == "__main__":
    main()
