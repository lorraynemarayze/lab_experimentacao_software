"""
    Script para rodar a consulta dos 100 primeiros repositórios
"""


from github_api import run_query
from data import build_query

token = '{COLOQUE_SEU_TOKEN_AQUI}'

result = []
after = None

print("Os primeiros 100 repositorios serão coletados em 10 páginas diferentes, cada uma com 10 repositórios.")

for i in range(10): 
    query = build_query(after_cursor=after, first=10)
    print(f'Coletando repositorios da pagina {i + 1}')
    query_result = run_query(query, token)

    nodes = query_result['data']['search']['nodes']
    result.extend(nodes)

    page_info = query_result['data']['search']['pageInfo']
    if not page_info['hasNextPage']:
        break
    after = page_info['endCursor']

print("\n\nRepositorios coletados com Sucesso\n\n")

print(result)