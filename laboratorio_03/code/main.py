"""
    Script para coletar os 1000 repositórios em Java com mais estrelas do GitHub
    e exportar os dados para CSV
"""

import csv  #importação para exportar CSV
import json
from github_api import run_query
from data import build_repo_query, build_pr_query, processar_dados_repositorio

token = '{COLOQUE_SEU_TOKEN_AQUI}'

result = [] #Lista que irá armazenar todos os prs coletados da API
repoNameWithOwnerList = [] #Lista que irá armazenar os 'nameWithOwner' dos repositórios coletados
after = None #Cursor de paginação que será usado para navegar entre as páginas de resultados. Começa com None (primeira página), depois vai receber o endCursor da página anterior

repo_num_pages = 25
repo_ammount_per_page = 10

pr_num_pages = 1
pr_ammount_per_page = 2

filtered_repo_names_with_owner = []

#Ajustado para coletar 1000 repositórios - API autoriza 10 repositórios por consulta
print(f"Os {repo_num_pages * repo_ammount_per_page} repositórios serão coletados em {repo_num_pages} páginas diferentes, cada uma com {repo_ammount_per_page} repositórios.")


for i in range(repo_num_pages): #Loop de paginação: irá executar 100 vezes para obter 100 páginas
    query = build_repo_query(after_cursor=after, first=repo_ammount_per_page)  #Constrói a query GraphQL com o cursor atual e quantidade definida
    print(f'Coletando repositórios da página {i + 1}')
    
    try:
        query_result = run_query(query, token) #Executa a query GraphQL usando o token de autenticação
        
        #Verifica se a resposta contém erros
        if 'errors' in query_result:
            print(f"Erro na consulta: {query_result['errors']}")
            break
        
    except Exception as e:
        print(f"Erro ao fazer consulta: {e}")
        break

    nodes = query_result['data']['search']['nodes'] #Extrai os dados dos repositórios da resposta JSON
    repoNameWithOwnerList.extend([repo['nameWithOwner'] for repo in nodes]) # Adiciona apenas o atributo nameWithOwner de cada repositório à lista principal
    
    print(f"Coletados {len(nodes)} repositórios. Total até agora: {len(repoNameWithOwnerList)}")

    page_info = query_result['data']['search']['pageInfo']
    if not page_info['hasNextPage']:   # Verifica se há próxima página disponível
        print("Não há mais páginas disponíveis.") 
        break
    after = page_info['endCursor']
    
# Agora coleta PRs de cada repositório
for repo in repoNameWithOwnerList:
    owner, name = repo.split("/")
    prs = []
    current_page = 1
    print(f"\nColetando PRs do repositório {repo}")

    pr_after = None
    while current_page <= 10:
        print(f"repositório {repo}: coletando página {current_page} de PRs")
        current_page += 1
        pr_query = build_pr_query(owner, name, after_cursor=pr_after, first=10)
        pr_result = run_query(pr_query, token)

        if "errors" in pr_result:
            print(f"Erro nos PRs de {repo}: {pr_result['errors']}")
            break

        prs.extend(pr_result["data"]["repository"]["pullRequests"]["nodes"])

        pr_page_info = pr_result["data"]["repository"]["pullRequests"]["pageInfo"]
        if pr_page_info["hasNextPage"]:
            pr_after = pr_page_info["endCursor"]
        else:
            break

    if len(prs) >= 100:
        filtered_repo_names_with_owner.append(repo)
        
    result.append({"name": repo, "pullRequests": prs})

print("\n\nRepositórios coletados com Sucesso\n\n")

print(f"Total de repositórios coletados: {len(result)}")

processados = [processar_dados_repositorio(repo) for repo in result]

print("\n\n\n")
print(f"Repositórios processados: {len(processados)}")

csv_filename = 'repositorios_github_dados.csv'

# Função para salvar CSV
def salvar_csv(dados, filename):
    print(f"\nSalvando dados em {csv_filename}...")
    with open(filename, "w", newline="") as csvfile:
        campos = dados[0].keys()  # usa as chaves como cabeçalho
        writer = csv.DictWriter(csvfile, fieldnames=campos)
        writer.writeheader()
        writer.writerows(dados)
        
def salvar_json(dados, filename):
    print(f"\nSalvando dados em {filename}...")
    with open(filename, "w") as jsonfile:
        json.dump(dados, jsonfile, indent=4)
        
def salvar_lista_em_arquivo(lista, nome_arquivo):
    with open(nome_arquivo, 'w', encoding='utf-8') as f:
        for item in lista:
            f.write(str(item) + '\n')

salvar_csv(processados, csv_filename)
salvar_json(processados, 'repositorios_github_dados.json')
salvar_lista_em_arquivo(filtered_repo_names_with_owner, 'repositorios_filtrados.txt')
print(processados)
