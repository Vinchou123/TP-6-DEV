import requests
import sys
import os

def get_content(url):
    
    try:
        response = requests.get(url)
        # Lève une exception pour les codes d'erreur HTTP
        response.raise_for_status()  
        return response.text
    except requests.RequestException as e:
        print(f"Erreur lors de la récupération de l'URL {url} : {e}")
        sys.exit(1)

def write_content(content, file):
  
    try:
        with open(file, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Le contenu a été écrit dans {file}")
    except OSError as e:
        print(f"Erreur lors de l'écriture dans le fichier {file} : {e}")
        sys.exit(1)

def main():
    if len(sys.argv) != 2:
        print("Usage: python web_sync.py <URL>")
        sys.exit(1)

    url = sys.argv[1]
    output_dir = os.path.join(os.sep, "tmp", "web_page")
    # Crée le dossier s'il n'existe pas
    os.makedirs(output_dir, exist_ok=True)  
    output_file = os.path.join(output_dir, "page.html")

    content = get_content(url)
    write_content(content, output_file)

if __name__ == "__main__":
    main()
