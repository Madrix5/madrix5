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
    # 1. Obtener datos de GitHub
    print(f"🔍 Actualizando proyectos para {USERNAME}...")
    url = f"https://api.github.com/users/{USERNAME}/repos?per_page=100&sort=updated"
    response = requests.get(url)
    if response.status_code != 200:
        sys.exit(1)
        
    repos = response.json()
    featured = [r for r in repos if TOPIC_TO_SHOW in (t.lower() for t in r.get('topics', []))]
    
    # 2. Crear la tabla (Solo una vez)
    table_content = "\n| 📂 Project | 📝 Description | 🛠️ Tech Stack |\n| :--- | :--- | :--- |\n"
    
    if not featured:
        table_content += "| --- | No hay proyectos con la etiqueta 'mostrar' | --- |\n"
    else:
        for r in featured:
            badges = [TECH_BADGES[t.lower()] for t in r.get('topics', []) if t.lower() in TECH_BADGES]
            stack = " ".join(badges) if badges else "---"
            table_content += f"| **[{r['name']}]({r['html_url']})** | {r['description'] or 'Sin descripción.'} | {stack} |\n"

    # 3. Leer README
    with open(README_PATH, "r", encoding="utf-8") as f:
        content = f.read()

    # 4. Sustitución con Regex (Busca el bloque completo y lo reemplaza)
    pattern = r".*?"
    replacement = f"{table_content}"
    
    if not re.search(pattern, content, flags=re.DOTALL):
        print("❌ Error: No se encuentran las marcas de inicio/fin.")
        sys.exit(1)

    new_content = re.sub(pattern, replacement, content, flags=re.DOTALL)

    # 5. Guardar
    with open(README_PATH, "w", encoding="utf-8") as f:
        f.write(new_content)
    
    print("✅ ¡README saneado y actualizado!")

if __name__ == "__main__":
    update_readme()
