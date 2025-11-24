import requests
import time
import sys

GITHUB_API_GRAPHQL = "https://api.github.com/graphql"
GITHUB_API_REST = "https://api.github.com"

def run_graphql_query(query: str, token: str) -> dict:
    """
    Executa uma consulta GraphQL na API do GitHub e retorna dados + métricas.
    Retorna: {
        'data': dados_resposta,
        'time': tempo_em_segundos,
        'size': tamanho_em_bytes
    }
    """
    headers = {"Authorization": f"Bearer {token}"}
    
    start_time = time.time()
    response = requests.post(GITHUB_API_GRAPHQL, json={"query": query}, headers=headers)
    elapsed_time = time.time() - start_time
    
    if response.status_code != 200:
        raise Exception(f"GraphQL Query failed: {response.status_code} {response.text}")
    
    response_data = response.json()
    response_size = len(response.content)
    
    return {
        'data': response_data,
        'time': elapsed_time,
        'size': response_size
    }


def run_rest_query(endpoint: str, token: str, params: dict = None) -> dict:
    """
    Executa uma consulta REST na API do GitHub e retorna dados + métricas.
    Retorna: {
        'data': dados_resposta,
        'time': tempo_em_segundos,
        'size': tamanho_em_bytes
    }
    """
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    url = f"{GITHUB_API_REST}{endpoint}"
    
    start_time = time.time()
    response = requests.get(url, headers=headers, params=params)
    elapsed_time = time.time() - start_time
    
    if response.status_code != 200:
        raise Exception(f"REST Query failed: {response.status_code} {response.text}")
    
    response_data = response.json()
    response_size = len(response.content)
    
    return {
        'data': response_data,
        'time': elapsed_time,
        'size': response_size
    }


def fetch_prs_rest_multiple(owner: str, name: str, token: str, per_page: int = 100, max_pages: int = 1) -> dict:
    """
    Busca PRs via REST API (pode fazer múltiplas requisições para paginação).
    Retorna todas as métricas agregadas.
    """
    all_prs = []
    total_time = 0
    total_size = 0
    page = 1
    
    while page <= max_pages:
        endpoint = f"/repos/{owner}/{name}/pulls"
        params = {
            'state': 'closed',
            'per_page': per_page,
            'page': page
        }
        
        result = run_rest_query(endpoint, token, params)
        
        all_prs.extend(result['data'])
        total_time += result['time']
        total_size += result['size']
        
        # Se retornou menos que per_page, não há mais páginas
        if len(result['data']) < per_page:
            break
        
        page += 1
    
    return {
        'data': all_prs,
        'time': total_time,
        'size': total_size,
        'requests': page
    }
