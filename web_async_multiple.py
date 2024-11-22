import asyncio
import sys
import os
import aiohttp
import aiofiles
import time

async def get_content(url):
    """Récupère le contenu d'une page Web de manière asynchrone."""
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                resp.raise_for_status()
                return await resp.text()
    except aiohttp.ClientError as e:
        print(f"Erreur lors de la récupération de {url}: {e}")
        return None

async def write_content(content, file):
    """Écrit le contenu dans un fichier de manière asynchrone."""
    async with aiofiles.open(file, "w", encoding="utf-8") as out:
        await out.write(content)

async def download_page(url, output_dir):
    """Télécharge le contenu de la page et l'écrit dans un fichier de manière asynchrone."""
    content = await get_content(url)
    if content:
        file_name = url.replace("https://", "").replace("http://", "").replace("/", "_")
        output_file = os.path.join(output_dir, f"web_{file_name}.html")
        await write_content(content, output_file)
        print(f"Page téléchargée : {url} -> {output_file}")
    
    await asyncio.sleep(0,5)

async def main():
    if len(sys.argv) != 2:
        print("Usage: python web_async_multiple.py <fichier_urls>")
        sys.exit(1)

    file_path = sys.argv[1]
    
    # Vérifier si le fichier existe
    if not os.path.isfile(file_path):
        print(f"Le fichier {file_path} n'existe pas.")
        sys.exit(1)

    output_dir = os.path.join(os.sep, "tmp", "web_pages")
    os.makedirs(output_dir, exist_ok=True)
    
    # Lire le fichier d'URLs
    with open(file_path, "r") as f:
        urls = f.readlines()
    
    # Supprimer les retours à la ligne et espaces
    urls = [url.strip() for url in urls if url.strip()]

    # Pour calculer le temps d'éxecution
    start_time = time.time()

    tasks = [download_page(url, output_dir) for url in urls]

    await asyncio.gather(*tasks)

    end_time = time.time()
    print(f"Temps d'exécution asynchrone: {end_time - start_time:.2f} secondes")

if __name__ == "__main__":
    asyncio.run(main())
