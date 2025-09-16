import os
import csv

BASE_PATH = pasta_atual = os.getcwd() + '/laboratorio_02/code'

JAVA_REPOS_PATH = os.path.join(BASE_PATH, 'java_repositories')
CK_TARGET_PATH = os.path.join(BASE_PATH, 'ck')

DEFAULT_JAVA_RESULTS_PATH = os.path.join(BASE_PATH, 'java_repositories_results')

def filter_class_csv(repo_name: str) -> None:
    """
    Filtra o arquivo class.csv para manter apenas as colunas CBO, DIT, LCOM e LOC.
    Remove os outros arquivos CSV gerados pelo CK.
    """
    output_path = os.path.join(DEFAULT_JAVA_RESULTS_PATH, repo_name)
    class_csv_path = os.path.join(output_path, 'class.csv')
    
    if os.path.exists(class_csv_path):
        # Lê o CSV original
        with open(class_csv_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            rows = list(reader)
        
        # Filtra apenas as colunas desejadas
        filtered_rows = []
        for row in rows:
            filtered_row = {
                'class': row.get('class', ''),
                'cbo': row.get('cbo', ''),
                'dit': row.get('dit', ''),
                'lcom': row.get('lcom', ''),
                'loc': row.get('loc', '')
            }
            filtered_rows.append(filtered_row)
        
        # Sobrescreve o arquivo com apenas as colunas filtradas
        with open(class_csv_path, 'w', newline='', encoding='utf-8') as file:
            fieldnames = ['class', 'cbo', 'dit', 'lcom', 'loc']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(filtered_rows)
        
        print(f"Arquivo class.csv filtrado para {repo_name} (mantendo apenas class, cbo, dit, lcom, loc)")
    
    # Remove os outros arquivos CSV desnecessários
    files_to_remove = ['method.csv', 'variable.csv', 'field.csv']
    for file_name in files_to_remove:
        file_path = os.path.join(output_path, file_name)
        if os.path.exists(file_path):
            os.remove(file_path)
            print(f"Arquivo {file_name} removido para {repo_name}")

def clone_repo(url: str) -> None:
    """
    Clona um repositório Git na URL especificada para o caminho local fornecido.
    """
    os.chdir(JAVA_REPOS_PATH)
    os.system(f'git clone {url}')
    os.chdir(BASE_PATH)
    
    

def run_metrics(repo_name: str) -> None:
    """
    Executa a ferramenta CK para calcular métricas de código no repositório especificado.
    Filtra o resultado para manter apenas class.csv com as colunas CBO, DIT, LCOM e LOC.
    """
    os.chdir(BASE_PATH)
    repo_path = JAVA_REPOS_PATH + '/' + repo_name
    output_path = DEFAULT_JAVA_RESULTS_PATH + '/' + repo_name + '/'

    # os.chdir(CK_TARGET_PATH)
    os.makedirs(output_path, exist_ok=True)
    
    # Executa o CK com variáveis e campos desabilitados (false) para reduzir o output
    os.system(f'java -jar ck-0.7.1-SNAPSHOT-jar-with-dependencies.jar {repo_path} true 0 false {output_path}')
    
    # Filtra o class.csv e remove arquivos desnecessários
    # filter_class_csv(repo_name)

# java -jar ` 
# target/ck-0.7.1-SNAPSHOT-jar-with-dependencies.jar `
# C:\MinhasCoisas\Programacao\Workspace\puc\lab_experimentacao_software\laboratorio_02\code\java_repositories\api `
# true `
# 0 `
# True `
# C:\MinhasCoisas\Programacao\Workspace\puc\lab_experimentacao_software\laboratorio_02\code\java_repositories_results