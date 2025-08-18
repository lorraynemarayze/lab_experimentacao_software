"""
    Script para coletar os 1000 repositórios com mais estrelas do GitHub
    e exportar os dados para CSV
"""

import csv  #importação para exportar CSV
from github_api import run_query
from data import build_query, processar_dados_repositorio

token = '{COLOQUE_SEU_TOKEN_AQUI}'

result = [] #Lista que irá armazenar todos os repositórios coletados da API
after = None #Cursor de paginação que será usado para navegar entre as páginas de resultados. Começa com None (primeira página), depois vai receber o endCursor da página anterior

#Ajustado para coletar 1000 repositórios - API autoriza 100 repositórios por consulta
print("Os 1000 repositórios serão coletados em 10 páginas diferentes, cada uma com 100 repositórios.")


for i in range(10): #Loop de paginação: irá executar 10 vezes para obter 10 páginas
    query = build_query(after_cursor=after, first=100)  #Constrói a query GraphQL com o cursor atual e quantidade definida
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
print(f"\nSalvando dados em {csv_filename}...")

# Fnção para salvar CSV
def salvar_csv(dados, filename):
    """
    Salva os dados processados em um arquivo CSV
    """
    # TODO: função salvar CSV

#salvar_csv()
#print(f"\nProcesso concluído! {len(processados)} repositórios salvos em {csv_filename}")