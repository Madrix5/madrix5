import requests
import re
import sys
import os

# --- CONFIGURACIÓN BÁSICA ---
USERNAME = "Madrix5"
TOPIC_TO_SHOW = "mostrar"

# Ruta absoluta al README (A prueba de fallos de GitHub Actions)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
README_PATH = os.path.join(BASE_DIR, "README.md")

# Diccionario de Badges (Formato exacto de Ileriayo)
TECH_BADGES = {
    "c": "![C](https://img.shields.io/badge/c-%2300599C.svg?style=for-the-badge&logo=c&logoColor=white)",
    "cpp": "![C++](https://img.shields.io/badge/c++-%2300599C.svg?style=for-the-badge&logo=c%2B%2B&logoColor=white)",
    "clion": "![CLion](https://img.shields.io/badge/CLion-black?style=for-the-badge&logo=clion&logoColor=white)",
    "python": "![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)",
    "javascript": "![JavaScript](https://img.shields.io/badge/javascript-%23323330.svg?style=for-the-badge&logo=javascript&logoColor=%23F7DF1E)",
    "html": "![HTML5](https://img.shields.io/badge/html5-%23E34F26.svg?style=for-the-badge&logo=html5&logoColor=white)",
    "css": "![CSS3](https://img.shields.io/badge/css3-%231572B6.svg?style=for-the-badge&logo=css3&logoColor=white)",
    "react": "![React](https://img.shields.io/badge/react-%2320232a.svg?style=for-the-badge&logo=react&logoColor=%2361DAFB)",
    "java": "![Java](https://img.shields.io/badge/java-%23ED8B00.svg?style=for-the-badge&logo=openjdk&logoColor=white)"
}

def update_readme():
    print(f"🔍 Buscando repositorios para: {USERNAME}...")
    url = f"https://api.github.com/users/{USERNAME}/repos?per_page=100&sort=updated"
    response = requests.get(url)
    
    if response.status_code != 200:
        print(f"❌ ERROR: Fallo al conectar con GitHub API. Código: {response.status_code}")
        sys.exit(1)
        
    repos = response.json()
    featured = [r for r in repos if TOPIC_TO_SHOW in (t.lower() for t in r.get('topics', []))]
    
    print(f"✅ Repositorios encontrados con la etiqueta '{TOPIC_TO_SHOW}': {len(featured)}")

    # Generar la tabla Markdown
    table = "| 📂 Project | 📝 Description | 🛠️ Tech Stack |\n| :--- | :--- | :--- |\n"
    
    if not featured:
        table += "| --- | Todavía no hay proyectos con la etiqueta 'mostrar' | --- |\n"
    else:
        for r in featured:
            name = r['name']
            url = r['html_url']
            desc = r['description'] or "Sin descripción."
            
            # Extraer y emparejar los topics con los badges
            topics = r.get('topics', [])
            badges = [TECH_BADGES[t.lower()] for t in topics if t.lower() in TECH_BADGES]
            stack = " ".join(badges) if badges else "---"
            
            table += f"| **[{name}]({url})** | {desc} | {stack} |\n"

    # Leer el archivo README
    print(f"📖 Leyendo archivo: {README_PATH}")
    try:
        with open(README_PATH, "r", encoding="utf-8") as f:
            content = f.read()
    except FileNotFoundError:
        print(f"❌ ERROR CRÍTICO: No se encontró el archivo {README_PATH}")
        sys.exit(1)

    # Validar que existan las marcas
    if "" not in content or "" not in content:
        print("❌ ERROR CRÍTICO: No se encuentran las etiquetas exactas y en el README.")
        sys.exit(1)

    # Reemplazar contenido
    pattern = r".*?"
    replacement = f"\n{table}\n"
    new_content = re.sub(pattern, replacement, content, flags=re.DOTALL)

    # Escribir los
