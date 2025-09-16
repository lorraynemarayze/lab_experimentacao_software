"""
    Script para coletar os 1000 repositórios com mais estrelas do GitHub
    e exportar os dados para CSV
"""
# 

import csv  #importação para exportar CSV
from github_api import run_query
from data import build_query, processar_dados_repositorio
from auto_cloning import clone_repo, run_metrics


token = '{COLOQUE_SEU_TOKEN_AQUI}'

result = [] #Lista que irá armazenar todos os repositórios coletados da API
after = None #Cursor de paginação que será usado para navegar entre as páginas de resultados. Começa com None (primeira página), depois vai receber o endCursor da página anterior

num_pages = 100
ammount_per_page = 10

#Ajustado para coletar 1000 repositórios - API autoriza 10 repositórios por consulta
print(f"Os {num_pages * ammount_per_page} repositórios serão coletados em {num_pages} páginas diferentes, cada uma com {ammount_per_page} repositórios.")


for i in range(num_pages): #Loop de paginação: irá executar 100 vezes para obter 100 páginas
    query = build_query(after_cursor=after, first=ammount_per_page)  #Constrói a query GraphQL com o cursor atual e quantidade definida
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
    result.extend(nodes) # Adiciona os novos repositórios à lista principal
    
    print(f"Coletados {len(nodes)} repositórios. Total até agora: {len(result)}")

    page_info = query_result['data']['search']['pageInfo']
    if not page_info['hasNextPage']:   # Verifica se há próxima página disponível
        print("Não há mais páginas disponíveis.") 
        break
    after = page_info['endCursor']

print("\n\nRepositórios coletados com Sucesso\n\n")

print(f"Total de repositórios coletados: {len(result)}")

processados = [processar_dados_repositorio(repo) for repo in result]

print("\n\n\n")
print(f"Repositórios processados: {len(processados)}")

csv_filename = 'repositorios_github_dados.csv'

# Fnção para salvar CSV
def salvar_csv(dados, filename):
    print(f"\nSalvando dados em {csv_filename}...")
    with open(filename, "w", newline="") as csvfile:
        campos = dados[0].keys()  # usa as chaves como cabeçalho
        writer = csv.DictWriter(csvfile, fieldnames=campos)
        writer.writeheader()
        writer.writerows(dados)

salvar_csv(processados, csv_filename)
# print(f"\nProcesso concluído! {len(processados)} repositórios salvos em {csv_filename}")

print(processados)

for index, repo in enumerate(processados):
    print(f"\n\nProcessando repositório {index + 1}/{len(processados)}: {repo['name']}")
    clone_repo(repo['url'])
    run_metrics(repo['name'])
    print(f"Repositório {repo['name']} processado com sucesso.\n\n")
    
    
for index, repo in enumerate(processados):
    print(f"\n\nProcessando repositório {index + 1}/{len(processados)}: {repo['name']}")
    clone_repo(repo['url'])
    run_metrics(repo['name'])
    print(f"Repositório {repo['name']} processado com sucesso.\n\n")

# Processamento final - geração do resultado_final.csv
print("\n\nGerando arquivo resultado_final.csv com métricas agregadas...")

import os
from auto_cloning import DEFAULT_JAVA_RESULTS_PATH, BASE_PATH

# 1. Remover atributos desnecessários
for repo in processados:
    repo.pop('language', None)
    repo.pop('url', None)

# 2. Processar métricas de cada repositório
resultados_finais = []

for repo in processados:
    nome_repo = repo['name']
    
    # 3. Buscar pasta do repositório
    pasta_repo = os.path.join(DEFAULT_JAVA_RESULTS_PATH, nome_repo)
    class_csv_path = os.path.join(pasta_repo, 'class.csv')
    
    # 4. Ler class.csv e calcular métricas
    if os.path.exists(class_csv_path):
        cbo_values = []
        dit_values = []
        lcom_values = []
        loc_total = 0
        
        try:
            with open(class_csv_path, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    try:
                        cbo_values.append(int(row['cbo']))
                        dit_values.append(int(row['dit']))
                        lcom_values.append(int(row['lcom']))
                        loc_total += int(row['loc'])
                    except ValueError:
                        continue  # Pular linhas com dados inválidos
        except Exception as e:
            print(f"Erro ao ler class.csv para {nome_repo}: {e}")
            continue
        
        # 5. Calcular médias
        if len(cbo_values) > 0:
            cbo_media = sum(cbo_values) / len(cbo_values)
            dit_media = sum(dit_values) / len(dit_values)
            lcom_media = sum(lcom_values) / len(lcom_values)
        else:
            cbo_media = dit_media = lcom_media = 0
            print(f"Nenhum dado válido encontrado para {nome_repo}")
        
        # 6. Criar objeto resultado com apenas os campos necessários
        resultado = {
            'name': repo['name'],
            'stars': repo['stars'],
            'releases': repo['releases'],
            'age_years': repo['age_years'],
            'cbo_media': round(cbo_media, 2),
            'dit_media': round(dit_media, 2),
            'lcom_media': round(lcom_media, 2),
            'loc_total': loc_total
        }
        
        resultados_finais.append(resultado)

    else:
        print(f"Arquivo class.csv não encontrado para {nome_repo}")

# 7. Criar arquivo resultado_final.csv
resultado_csv_path = os.path.join(BASE_PATH, 'resultado_final.csv')
if resultados_finais:
    with open(resultado_csv_path, 'w', newline='', encoding='utf-8') as file:
        fieldnames = ['name', 'stars', 'releases', 'age_years', 'cbo_media', 'dit_media', 'lcom_media', 'loc_total']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(resultados_finais)
    
    print(f"\n✅ Arquivo resultado_final.csv criado com sucesso!")
    print(f"📊 {len(resultados_finais)} repositórios processados com métricas válidas")
    print(f"📁 Arquivo salvo em: {resultado_csv_path}")
else:
    print("❌ Nenhum repositório com dados válidos encontrado")

print("\n\nProcesso concluído! Todos os repositórios foram clonados e as métricas foram calculadas.")
print('Os resultados das métricas estão na pasta java_repositories_results')
print('O arquivo consolidado resultado_final.csv foi gerado na pasta code')
    
    