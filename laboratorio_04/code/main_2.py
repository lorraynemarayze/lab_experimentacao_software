# Esse script é o responsável pela obtenção
# dos notbooks que são usados como base por
# todo esse trabalho. 


# Dados Tabulares
# House Prices - Advanced Regression Techniques | house-prices-advanced-regression-techniques
# Titanic - Machine Learning from Disaster | titanic
# Santander Customer Transaction Prediction | santander-customer-transaction-prediction


# Visão Computacional (CV)
# Digit Recognizer | digit-recognizer
# Cassava Leaf Disease Classification | cassava-leaf-disease-classification
# HuBMAP - Kidney Segmentation | hubmap-kidney-segmentation


# Processamento de Linguagem Natural (NLP)
# Natural Language Processing with Disaster Tweets | nlp-getting-started
# Jigsaw Unintended Bias in Toxicity Classification | jigsaw-unintended-bias-in-toxicity-classification
# CommonLit Readability Prize | commonlitreadabilityprize


# house-prices-advanced-regression-techniques
# titanic
# santander-customer-transaction-prediction
# digit-recognizer
# cassava-leaf-disease-classification
# hubmap-kidney-segmentation
# nlp-getting-started
# jigsaw-unintended-bias-in-toxicity-classification
# commonlitreadabilityprize

# kaggle kernels list --competition titanic

import os
import subprocess
import csv
import json
import time

competition_dir = "competition"
notebooks_dir = "notebooks"

competitions = [
    {
        "name": "house-prices-advanced-regression-techniques",
        "domain": "Dados Tabulares"
    },
    {
        "name": "titanic",
        "domain": "Dados Tabulares"
    },
    {
        "name": "santander-customer-transaction-prediction",
        "domain": "Dados Tabulares"
    },
    {
        "name": "digit-recognizer",
        "domain": "Visão Computacional"
    },
    {
        "name": "cassava-leaf-disease-classification",
        "domain": "Visão Computacional"
    },
    {
        "name": "hubmap-kidney-segmentation",
        "domain": "Visão Computacional"
    },
    {
        "name": "nlp-getting-started",
        "domain": "NLP"
    },
    {
        "name": "jigsaw-unintended-bias-in-toxicity-classification",
        "domain": "NLP"
    },
    {
        "name": "commonlitreadabilityprize",
        "domain": "NLP"
    }
]

os.makedirs(competition_dir, exist_ok=True)
os.makedirs(notebooks_dir, exist_ok=True)

# Lista para armazenar todos os notebooks seguindo o plain_schema
all_notebooks_data = []

# ETAPA 1: Buscar e processar CSVs de todas as competições
print("\n" + "="*80)
print("ETAPA 1: BUSCANDO E PROCESSANDO CSVs DAS COMPETIÇÕES")
print("="*80)

for competition in competitions:
    competition_name = competition['name']
    domain = competition['domain']

    print(f"\n{'='*80}")
    print(f"Competition: {competition_name} | domain: {domain}")
    print(f"{'='*80}\n")
    
    # Criar pasta para a competição
    competition_path = os.path.join(competition_dir, competition_name)
    os.makedirs(competition_path, exist_ok=True)
    
    # Buscar 4 páginas de notebooks (100 por página)
    print(f"Buscando notebooks para {competition_name}...")
    for page in range(1, 5):
        csv_filename = os.path.join(competition_path, f"page-{page}.csv")
        
        # Comando para buscar notebooks
        cmd = f"kaggle kernels list --competition {competition_name} --sort-by voteCount --page-size 100 -p {page} --csv > {csv_filename}"
        
        print(f"  Página {page}: Executando busca...")
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"  Página {page}: ✓ Salvo em {csv_filename}")
        else:
            print(f"  Página {page}: ✗ Erro ao buscar notebooks")
            print(f"    Erro: {result.stderr}")
            print(f"Tentando novamente em 30 segundos...")
            time.sleep(30)
            page -= 1 
    
    # Coletar dados dos CSVs e criar lista seguindo o plain_schema
    print(f"\nProcessando CSVs para {competition_name}...")
    
    for page in range(1, 5):
        csv_filename = os.path.join(competition_path, f"page-{page}.csv")
        
        if not os.path.exists(csv_filename):
            continue
            
        try:
            with open(csv_filename, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    notebook_data = {
                        "ref": row.get('ref', ''),
                        "title": row.get('title', ''),
                        "author": row.get('author', ''),
                        "lastRunTime": row.get('lastRunTime', ''),
                        "totalVotes": int(row.get('totalVotes', 0)),
                        "competition": competition_name,
                        "domain": domain,
                        "dataDependency": 0,
                        "codeDependency": 0,
                        "awareness": 0,
                        "modularity": 0,
                        "configurableOptions": 0,
                        "scalability": 0,
                        "readability": 0,
                        "performance": 0,
                        "duplicateCodeElimination": 0
                    }
                    all_notebooks_data.append(notebook_data)
            
            print(f"  Página {page}: Processada com sucesso")
        except Exception as e:
            print(f"  Erro ao processar {csv_filename}: {e}")

    amount_notebooks = sum(1 for n in all_notebooks_data if n['competition'] == competition_name)
    print(f"✓ Total de notebooks coletados para {competition_name}: {amount_notebooks}")
    
    
# ETAPA 2: Salvar todos os dados coletados em arquivo csv
print("\n" + "="*80)
print("ETAPA 2: SALVANDO DADOS COLETADOS EM ARQUIVO CSV")
print("="*80)

# Criar diretório para salvar os CSVs
os.makedirs("output", exist_ok=True)

# Salvar dados em arquivo CSV
csv_filename = f"output/all_notebooks_data.csv"
with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = all_notebooks_data[0].keys()
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    for notebook in all_notebooks_data:
        writer.writerow(notebook)

print(f"✓ Dados salvos em: {csv_filename}")

# ETAPA 3: Clonar todos os notebooks
print("\n" + "="*80)
print("ETAPA 3: CLONANDO NOTEBOOKS")
print("="*80)

for competition in competitions:
    competition_name = competition['name']
    domain = competition['domain']
    
    print(f"\n{'='*80}")
    print(f"Clonando notebooks de: {competition_name}")
    print(f"{'='*80}\n")
    
    # Filtrar notebooks desta competição
    competition_notebooks = [n for n in all_notebooks_data if competition_name == n['competition']]
    
    if not competition_notebooks:
        print(f"  ⚠ Nenhum notebook encontrado para clonar")
        continue
    
    # Criar diretório para clonagem
    clone_dir = os.path.join(notebooks_dir, domain.replace(" ", "_"), competition_name)
    os.makedirs(clone_dir, exist_ok=True)
    
    # Clonar cada notebook com sistema de retry
    for i, notebook in enumerate(competition_notebooks):
        ref = notebook['ref']
        if not ref:
            continue
            
        print(f"  Clonando {i+1}/{len(competition_notebooks)}: {ref}")
        clone_cmd = f"kaggle kernels pull {ref} -p {clone_dir}/{ref.split('/')[-1]}"

        while True:
            result = subprocess.run(clone_cmd, shell=True, capture_output=True, text=True)
            
            if result.returncode == 0:
                print(f"    ✓ Clonado com sucesso")
                break
            else:
                print(f"    ✗ Erro: {result.stderr[:80]}")
                print(f"    ⏳ Aguardando 30 segundos antes de tentar novamente...")
                time.sleep(30)


print(f"\n{'='*80}")
print(f"Processo concluído!")
print(f"Total de notebooks coletados: {len(all_notebooks_data)}")
print(f"{'='*80}")