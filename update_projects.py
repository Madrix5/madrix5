import requests
import re
import sys
import os

# --- CONFIGURACIÓN ---
USERNAME = "Madrix5"
TOPIC_TO_SHOW = "mostrar"
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
README_PATH = os.path.join(BASE_DIR, "README.md")

TECH_BADGES = {
    "c": "![C](https://img.shields.io/badge/c-%2300599C.svg?style=for-the-badge&logo=c&logoColor=white)",
    "cpp": "![C++](https://img.shields.io/badge/c++-%2300599C.svg?style=for-the-badge&logo=c%2B%2B&logoColor=white)",
    "clion": "![CLion](https://img.shields.io/badge/CLion-black?style=for-the-badge&logo=clion&logoColor=white)",
    "python": "![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)",
    "javascript": "![JavaScript](https://img.shields.io/badge/javascript-%23323330.svg?style=for-the-badge&logo=javascript&logoColor=%23F7DF1E)"
}

def update_readme():
    print(f"🔍 Buscando repositorios para: {USERNAME}...")
    url = f"https://api.github.com/users/{USERNAME}/repos?per_page=100&sort=updated"
    response = requests.get(url)
    
    if response.status_code != 200:
        print(f"❌ ERROR API: {response.status_code}")
        sys.exit(1)
        
    repos = response.json()
    featured = [r for r in repos if TOPIC_TO_SHOW in (t.lower() for t in r.get('topics', []))]
    
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

    # Leer el archivo
    with open(README_PATH, "r", encoding="utf-8") as f:
        content = f.read()

    # DEFINIMOS EL PATRÓN ANTES DE USARLO (Aquí estaba el fallo)
    pattern = r".*?"

    if "" not in content:
        print("❌ ERROR: No se encuentran las etiquetas en el README.")
        sys.exit(1)

    # Reemplazar
    replacement = f"\n{table}\n"
    new_content = re.sub(pattern, replacement, content, flags=re.DOTALL)

    with open(README_PATH, "w", encoding="utf-8") as f:
        f.write(new_content)
    
    print("🎉 ¡Éxito! README actualizado.")

if __name__ == "__main__":
    update_readme()
