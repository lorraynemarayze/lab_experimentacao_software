"""
Comparação entre GraphQL e REST API do GitHub
Mede tempo de resposta e tamanho dos dados retornados
"""

import csv
import sys
from github_api import run_graphql_query, fetch_prs_rest_multiple
from data import build_pr_query_graphql, processar_prs_graphql, processar_prs_rest

# Configure seu token do GitHub aqui
TOKEN = '{COLOQUE_SEU_TOKEN_AQUI}'

# Repositórios para testar (pode adicionar mais)
# TODO: Colocar os respositorios corretos
REPOSITORIES = [
    {"owner": "facebook", "name": "react"},
    {"owner": "microsoft", "name": "vscode"},
    {"owner": "tensorflow", "name": "tensorflow"},
    {"owner": "vuejs", "name": "vue"},
    {"owner": "angular", "name": "angular"},
]

def comparar_apis(owner: str, name: str, token: str, num_prs: int = 100):
    """
    Compara GraphQL vs REST para buscar PRs de um repositório.
    Retorna dicionário com métricas de comparação.
    """

    print(f"Analisando: {owner}/{name}")
    
    resultado = {
        'repositorio': f"{owner}/{name}",
        'num_prs_solicitados': num_prs,
    }
    
    print("\n[GraphQL] Executando query...")
    try:
        query = build_pr_query_graphql(owner, name, first=num_prs)
        graphql_result = run_graphql_query(query, token)
        
        prs_graphql = processar_prs_graphql(graphql_result['data'])
        
        resultado['graphql_tempo_segundos'] = round(graphql_result['time'], 3)
        resultado['graphql_tamanho_bytes'] = graphql_result['size']
        resultado['graphql_tamanho_kb'] = round(graphql_result['size'] / 1024, 2)
        resultado['graphql_num_prs'] = len(prs_graphql)
        resultado['graphql_requisicoes'] = 1
        
    except Exception as e:
        print(f"  ✗ Erro no GraphQL: {e}")
    
    
    print("\n[REST] Executando queries...")
    try:
        # Calcular quantas páginas precisamos (REST limita 100 por página)
        max_pages = (num_prs + 99) // 100  # arredonda para cima
        
        rest_result = fetch_prs_rest_multiple(owner, name, token, per_page=100, max_pages=max_pages)
        
        prs_rest = processar_prs_rest(rest_result['data'])
        
        resultado['rest_tempo_segundos'] = round(rest_result['time'], 3)
        resultado['rest_tamanho_bytes'] = rest_result['size']
        resultado['rest_tamanho_kb'] = round(rest_result['size'] / 1024, 2)
        resultado['rest_num_prs'] = len(prs_rest)
        resultado['rest_requisicoes'] = rest_result['requests']
        
    except Exception as e:
        print(f"  ✗ Erro no REST: {e}")
    
    # TODO: preencher difenreca

    
    return resultado


def exportar_csv(resultados: list, filename: str = "comparacao_graphql_rest.csv"):
    """
    Exporta os resultados para CSV.
    """
    if not resultados:
        print("Nenhum resultado para exportar.")
        return
    
    fieldnames = [
        'repositorio',
        'num_prs_solicitados',
        'graphql_tempo_segundos',
        'graphql_tamanho_bytes',
        'graphql_tamanho_kb',
        'graphql_num_prs',
        'graphql_requisicoes',
        'rest_tempo_segundos',
        'rest_tamanho_bytes',
        'rest_tamanho_kb',
        'rest_num_prs',
        'rest_requisicoes',
        'diferenca_tempo_segundos',
        'diferenca_tempo_percentual',
        'diferenca_tamanho_bytes',
        'diferenca_tamanho_kb',
        'diferenca_tamanho_percentual',
    ]
    
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, extrasaction='ignore')
        writer.writeheader()
        writer.writerows(resultados)
    
    print(f"\nResultados exportados para: {filename}")


def main():
    """
    Função principal que executa a comparação para todos os repositórios.
    """
    if TOKEN == '{COLOQUE_SEU_TOKEN_AQUI}':
        print("ERRO: Configure seu token do GitHub na variável TOKEN")
        print("Gere um token em: https://github.com/settings/tokens")
        sys.exit(1)
    
    print(f"Total de repositórios para analisar: {len(REPOSITORIES)}")
    print(f"PRs por repositório: 100")
    
    resultados = []
    
    for repo in REPOSITORIES:
        try:
            resultado = comparar_apis(
                owner=repo['owner'],
                name=repo['name'],
                token=TOKEN,
                num_prs=100
            )
            resultados.append(resultado)
        except Exception as e:
            print(f"\nErro ao processar {repo['owner']}/{repo['name']}: {e}")
            continue
    
    # Exportar resultados
    exportar_csv(resultados)
    

if __name__ == "__main__":
    main()
