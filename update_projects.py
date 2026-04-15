import requests
import re

# 1. Configuración básica
USERNAME = "Madrix5"
TOPIC_TO_SHOW = "mostrar"
README_PATH = "README.md"

# 2. Diccionario de Badges (Basado en Ileriayo/markdown-badges)
# Aquí puedes añadir todos los que necesites siguiendo el repo que me pasaste
TECH_BADGES = {
    "c": "![C](https://img.shields.io/badge/c-%2300599C.svg?style=for-the-badge&logo=c&logoColor=white)",
    "clion": "![CLion](https://img.shields.io/badge/CLion-black?style=for-the-badge&logo=clion&logoColor=white)",
    "javascript": "![JavaScript](https://img.shields.io/badge/javascript-%23323330.svg?style=for-the-badge&logo=javascript&logoColor=%23F7DF1E)",
    "vsc": "![Visual Studio Code](https://img.shields.io/badge/Visual%20Studio%20Code-0078d7.svg?style=for-the-badge&logo=visual-studio-code&logoColor=white)",
    "python": "![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)",
    "html": "![HTML5](https://img.shields.io/badge/html5-%23E34F26.svg?style=for-the-badge&logo=html5&logoColor=white)",
    "css": "![CSS3](https://img.shields.io/badge/css3-%231572B6.svg?style=for-the-badge&logo=css3&logoColor=white)",
    "cpp": "![C++](https://img.shields.io/badge/c++-%2300599C.svg?style=for-the-badge&logo=c%2B%2B&logoColor=white)"
}

def get_repos():
    url = f"https://api.github.com/users/{USERNAME}/repos?per_page=100"
    response = requests.get(url)
    if response.status_code != 200:
        return []
    
    all_repos = response.json()
    # Solo los que tienen la etiqueta 'mostrar'
    featured = [r for r in all_repos if TOPIC_TO_SHOW in r.get('topics', [])]
    return featured

def generate_table(repos):
    table = "| 📂 Project | 📝 Description | 🛠️ Tech Stack |\n| :--- | :--- | :--- |\n"
    
    for r in repos:
        name = r['name']
        url = r['html_url']
        desc = r['description'] or "Sin descripción."
        
        # Generar los badges buscando en los topics del repo
        topics = r.get('topics', [])
        badges_list = []
        for t in topics:
            t_lower = t.lower()
            if t_lower in TECH_BADGES:
                badges_list.append(TECH_BADGES[t_lower])
        
        stack = " ".join(badges_list) if badges_list else "---"
        
        table += f"| **[{name}]({url})** | {desc} | {stack} |\n"
    
    return table

def update_readme():
    repos = get_repos()
    new_table = generate_table(repos)

    with open(README_PATH, "r", encoding="utf-8") as f:
        content = f.read()

    # Reemplazo con regex entre las marcas y pattern = r".*?"
    replacement = f"\n{new_table}\n"
    
    if not re.search(pattern, content, flags=re.DOTALL):
        print("Error: No se han encontrado las marcas en el README.md")
        return

    new_content = re.sub(pattern, replacement, content, flags=re.DOTALL)

    with open(README_PATH, "w", encoding="utf-8") as f:
        f.write(new_content)

if __name__ == "__main__":
    update_readme()
