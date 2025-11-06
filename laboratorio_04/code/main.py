import os
import csv

competition_dir = "competition"
notebooks_dir = "notebooks"

# Garante que a pasta notebooks existe
os.makedirs(notebooks_dir, exist_ok=True)

# Lista todas as subpastas de competition
for subfolder in os.listdir(competition_dir):
    subfolder_path = os.path.join(competition_dir, subfolder)
    if os.path.isdir(subfolder_path):
        csv_path = os.path.join(subfolder_path, "page1.csv")
        if os.path.exists(csv_path):
            with open(csv_path, newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    ref = row["ref"]
                    title = row["title"]
                    # Remove caracteres problemáticos do nome
                    safe_title = "".join(c if c.isalnum() or c in " _-" else "_" for c in title)
                    dest_path = f"./notebooks/{safe_title}/"
                    cmd = f'kaggle kernels pull {ref} -p "{dest_path}"'
                    print(f"Executando: {cmd}")
                    os.system(cmd)