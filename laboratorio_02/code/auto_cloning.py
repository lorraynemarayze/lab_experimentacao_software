import os
import csv
import re

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

def count_comment_lines(repo_name: str) -> int:
    """
    Conta o total de linhas de comentário em todos os arquivos .java do repositório.
    Inclui comentários de linha única (//) e comentários de bloco (/* */).
    """
    repo_path = os.path.join(JAVA_REPOS_PATH, repo_name)
    total_comment_lines = 0
    
    if not os.path.exists(repo_path):
        print(f"Repositório {repo_name} não encontrado em {repo_path}")
        return 0
    
    # Percorre recursivamente todos os arquivos .java
    for root, dirs, files in os.walk(repo_path):
        for file in files:
            if file.endswith('.java'):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                        total_comment_lines += count_comments_in_content(content)
                except Exception as e:
                    # Continua mesmo se houver erro ao ler um arquivo
                    continue
    
    print(f"Total de linhas de comentário em {repo_name}: {total_comment_lines}")
    return total_comment_lines

def count_comments_in_content(content: str) -> int:
    """
    Conta linhas de comentário em um conteúdo Java específico.
    """
    comment_lines = 0
    lines = content.split('\n')
    in_block_comment = False
    
    for line in lines:
        stripped_line = line.strip()
        
        # Verifica comentário de bloco
        if '/*' in stripped_line:
            in_block_comment = True
            comment_lines += 1
            # Verifica se o comentário termina na mesma linha
            if '*/' in stripped_line:
                in_block_comment = False
        elif in_block_comment:
            comment_lines += 1
            if '*/' in stripped_line:
                in_block_comment = False
        # Verifica comentário de linha única
        elif stripped_line.startswith('//'):
            comment_lines += 1
        # Verifica comentário inline (após código)
        elif '//' in stripped_line:
            # Verifica se o // não está dentro de uma string
            if not is_in_string(stripped_line, stripped_line.find('//')):
                comment_lines += 1
    
    return comment_lines

def is_in_string(line: str, position: int) -> bool:
    """
    Verifica se uma posição na linha está dentro de uma string literal.
    """
    before_position = line[:position]
    # Conta aspas não escapadas antes da posição
    quote_count = 0
    i = 0
    while i < len(before_position):
        if before_position[i] == '"' and (i == 0 or before_position[i-1] != '\\'):
            quote_count += 1
        i += 1
    
    # Se o número de aspas for ímpar, estamos dentro de uma string
    return quote_count % 2 == 1