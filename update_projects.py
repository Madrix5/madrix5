import requests
import re
import sys

USERNAME = "Madrix5"
TOPIC_TO_SHOW = "mostrar"
README_PATH = "README.md"

# Asegúrate de que estas etiquetas coinciden con tus "topics" en GitHub
TECH_BADGES = {
    "c": "![C](https://img.shields.io/badge/c-%2300599C.svg?style=for-the-badge&logo=c&logoColor=white)",
    "clion": "![CLion](https://img.shields.io/badge/CLion-black?style=for-the-badge&logo=clion&logoColor=white)",
    "python": "![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)"
}

def update_readme():
    print(f"Buscando repositorios para el usuario: {USERNAME}...")
    url = f"https://api.github.com/users/{USERNAME}/repos?per_page=100"
    response = requests.get(url)
    
    if response.status_code != 200:
        print(f"Error en la API de GitHub: {response.status_code}")
        sys.exit(1)
        
    repos = response.json()
    featured = [r for r in repos if TOPIC_TO_SHOW in r.get('topics', [])]
    
    print(f"Repositorios encontrados con la etiqueta '{TOPIC_TO_SHOW}': {len(featured)}")

    table = "| 📂 Project | 📝 Description | 🛠️ Tech Stack |\n| :--- | :--- | :--- |\n"
    
    if not featured:
        table += "| --- | Todavía no hay proyectos con la etiqueta 'mostrar' | --- |\n"
    else:
        for r in featured:
            name = r['name']
            url = r['html_url']
            desc = r['description'] or "Sin descripción."
            topics = r.get('topics', [])
            badges = [TECH_BADGES[t.lower()] for t in topics if t.lower() in TECH_BADGES]
            stack = " ".join(badges) if badges else "---"
            table += f"| **[{name}]({url})** | {desc} | {stack} |\n"

    # LEER README
    with open(README_PATH, "r", encoding="utf-8") as f:
        content = f.read()

    # IMPORTANTE: Esta es la parte que suele fallar
    pattern = r".*?"
    
    if "" not in content:
        print("ERROR CRÍTICO: No se encuentra la etiqueta en el README.md")
        print(f"Contenido del README leído:\n{content}") # Esto nos dirá qué está viendo el script
        sys.exit(1)

    replacement = f"\n{table}\n"
    new_content = re.sub(pattern, replacement, content, flags=re.DOTALL)

    with open(README_PATH, "w", encoding="utf-8") as f:
        f.write(new_content)
    
    print("¡README actualizado con éxito!")

if __name__ == "__main__":
    update_readme()
