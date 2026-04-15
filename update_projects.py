import requests
import re
import sys

# 1. Configuración
USERNAME = "Madrix5"
TOPIC_TO_SHOW = "mostrar"
README_PATH = "README.md"

TECH_BADGES = {
    "c": "![C](https://img.shields.io/badge/c-%2300599C.svg?style=for-the-badge&logo=c&logoColor=white)",
    "clion": "![CLion](https://img.shields.io/badge/CLion-black?style=for-the-badge&logo=clion&logoColor=white)",
    "javascript": "![JavaScript](https://img.shields.io/badge/javascript-%23323330.svg?style=for-the-badge&logo=javascript&logoColor=%23F7DF1E)",
    "vsc": "![Visual Studio Code](https://img.shields.io/badge/Visual%20Studio%20Code-0078d7.svg?style=for-the-badge&logo=visual-studio-code&logoColor=white)"
}

def update_readme():
    # Obtener repos
    url = f"https://api.github.com/users/{USERNAME}/repos?per_page=100"
    response = requests.get(url)
    
    if response.status_code != 200:
        print(f"Error API: {response.status_code}")
        sys.exit(1)
        
    repos = response.json()
    featured = [r for r in repos if TOPIC_TO_SHOW in r.get('topics', [])]
    
    if not featured:
        print("No se encontraron repositorios con la etiqueta 'mostrar'")
        # No salimos con error para que la Action no se ponga roja si simplemente no hay nada
        table = "Todavía no hay proyectos destacados."
    else:
        # Generar tabla
        table = "| 📂 Project | 📝 Description | 🛠️ Tech Stack |\n| :--- | :--- | :--- |\n"
        for r in featured:
            name = r['name']
            url = r['html_url']
            desc = r['description'] or "Sin descripción."
            topics = r.get('topics', [])
            badges = [TECH_BADGES[t.lower()] for t in topics if t.lower() in TECH_BADGES]
            stack = " ".join(badges) if badges else "---"
            table += f"| **[{name}]({url})** | {desc} | {stack} |\n"

    # Leer y actualizar README
    with open(README_PATH, "r", encoding="utf-8") as f:
        content = f.read()

    pattern = r".*?"
    if not re.search(pattern, content, flags=re.DOTALL):
        print("ERROR: No se han encontrado las marcas y ")
        sys.exit(1)

    replacement = f"\n{table}\n"
    new_content = re.sub(pattern, replacement, content, flags=re.DOTALL)

    with open(README_PATH, "w", encoding="utf-8") as f:
        f.write(new_content)
    print("README actualizado con éxito.")

if __name__ == "__main__":
    update_readme()
