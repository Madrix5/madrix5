import requests
import re
import sys
import os

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
    print("🔍 Obteniendo proyectos de la API...")
    url = f"https://api.github.com/users/{USERNAME}/repos?per_page=100&sort=updated"
    r_api = requests.get(url)
    if r_api.status_code != 200:
        sys.exit(1)
        
    repos = r_api.json()
    featured = [r for r in repos if TOPIC_TO_SHOW in (t.lower() for t in r.get('topics', []))]
    
    # Construimos la tabla
    table = "\n| 📂 Project | 📝 Description | 🛠️ Tech Stack |\n| :--- | :--- | :--- |\n"
    if not featured:
        table += "| --- | No hay proyectos con la etiqueta 'mostrar' | --- |\n"
    else:
        for r in featured:
            badges = [TECH_BADGES[t.lower()] for t in r.get('topics', []) if t.lower() in TECH_BADGES]
            stack = " ".join(badges) if badges else "---"
            table += f"| **[{r['name']}]({r['html_url']})** | {r['description'] or 'Sin descripción.'} | {stack} |\n"

    # LEER EL README COMPLETO
    if not os.path.exists(README_PATH):
        print("❌ El archivo README.md no existe.")
        sys.exit(1)

    with open(README_PATH, "r", encoding="utf-8") as f:
        full_content = f.read()

    start_tag = "<!-- START_PROJECTS -->"
    end_tag = "<!-- END_PROJECTS -->"
    
    if start_tag not in full_content or end_tag not in full_content:
        print("❌ No se encontraron las marcas.")
        sys.exit(1)

    # Dividimos el archivo en 3 partes: antes de la marca, la tabla, y después de la marca
    before = full_content.split(start_tag)[0]
    after = full_content.split(end_tag)[1]
    
    new_readme = f"{before}{start_tag}{table}{end_tag}{after}"

    with open(README_PATH, "w", encoding="utf-8") as f:
        f.write(new_readme)
    
    print("✅ ¡README actualizado respetando tu contenido!")

if __name__ == "__main__":
    update_readme()
