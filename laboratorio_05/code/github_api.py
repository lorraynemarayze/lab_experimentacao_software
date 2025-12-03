import requests
import time
import sys

GITHUB_API_GRAPHQL = "https://api.github.com/graphql"
GITHUB_API_REST = "https://api.github.com"

# Configurações de retry
MAX_RETRIES = 5
RETRY_DELAY = 2  # segundos iniciais
RETRYABLE_STATUS_CODES = [500, 502, 503, 504, 429]  # Códigos que justificam retry

def run_graphql_query(query: str, token: str, max_retries: int = MAX_RETRIES) -> dict:
    """
    Executa uma consulta GraphQL na API do GitHub e retorna dados + métricas.
    Implementa retry com backoff exponencial para erros temporários.
    
    Retorna: {
        'data': dados_resposta,
        'time': tempo_em_segundos,
        'size': tamanho_em_bytes
    }
    """
    headers = {"Authorization": f"Bearer {token}"}
    
    total_time = 0
    
    for attempt in range(max_retries):
        try:
            start_time = time.time()
            response = requests.post(GITHUB_API_GRAPHQL, json={"query": query}, headers=headers, timeout=30)
            elapsed_time = time.time() - start_time
            total_time += elapsed_time
            
            if response.status_code == 200:
                response_data = response.json()
                response_size = len(response.content)
                
                return {
                    'data': response_data,
                    'time': total_time,
                    'size': response_size
                }
            
            # Se o erro é retryável, tenta novamente
            if response.status_code in RETRYABLE_STATUS_CODES:
                delay = RETRY_DELAY * (2 ** attempt)  # Backoff exponencial
                print(f"    ⚠ Tentativa {attempt + 1}/{max_retries} falhou (HTTP {response.status_code}). Aguardando {delay}s...")
                time.sleep(delay)
                continue
            else:
                # Erro não retryável, lança exceção imediatamente
                raise Exception(f"GraphQL Query failed: {response.status_code} {response.text[:200]}")
                
        except requests.exceptions.Timeout:
            delay = RETRY_DELAY * (2 ** attempt)
            print(f"    ⚠ Timeout na tentativa {attempt + 1}/{max_retries}. Aguardando {delay}s...")
            if attempt < max_retries - 1:
                time.sleep(delay)
            else:
                raise Exception("GraphQL Query failed: Timeout após todas as tentativas")
                
        except requests.exceptions.RequestException as e:
            if attempt < max_retries - 1:
                delay = RETRY_DELAY * (2 ** attempt)
                print(f"    ⚠ Erro de conexão na tentativa {attempt + 1}/{max_retries}. Aguardando {delay}s...")
                time.sleep(delay)
            else:
                raise Exception(f"GraphQL Query failed: {str(e)}")
    
    raise Exception(f"GraphQL Query failed: Máximo de {max_retries} tentativas excedido")


def run_rest_query(endpoint: str, token: str, params: dict = None, max_retries: int = MAX_RETRIES) -> dict:
    """
    Executa uma consulta REST na API do GitHub e retorna dados + métricas.
    Implementa retry com backoff exponencial para erros temporários.
    
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
    total_time = 0
    
    for attempt in range(max_retries):
        try:
            start_time = time.time()
            response = requests.get(url, headers=headers, params=params, timeout=30)
            elapsed_time = time.time() - start_time
            total_time += elapsed_time
            
            if response.status_code == 200:
                response_data = response.json()
                response_size = len(response.content)
                
                return {
                    'data': response_data,
                    'time': total_time,
                    'size': response_size
                }
            
            # Se o erro é retryável, tenta novamente
            if response.status_code in RETRYABLE_STATUS_CODES:
                delay = RETRY_DELAY * (2 ** attempt)  # Backoff exponencial
                print(f"    ⚠ Tentativa {attempt + 1}/{max_retries} falhou (HTTP {response.status_code}). Aguardando {delay}s...")
                time.sleep(delay)
                continue
            else:
                # Erro não retryável
                raise Exception(f"REST Query failed: {response.status_code} {response.text[:200]}")
                
        except requests.exceptions.Timeout:
            delay = RETRY_DELAY * (2 ** attempt)
            print(f"    ⚠ Timeout na tentativa {attempt + 1}/{max_retries}. Aguardando {delay}s...")
            if attempt < max_retries - 1:
                time.sleep(delay)
            else:
                raise Exception("REST Query failed: Timeout após todas as tentativas")
                
        except requests.exceptions.RequestException as e:
            if attempt < max_retries - 1:
                delay = RETRY_DELAY * (2 ** attempt)
                print(f"    ⚠ Erro de conexão na tentativa {attempt + 1}/{max_retries}. Aguardando {delay}s...")
                time.sleep(delay)
            else:
                raise Exception(f"REST Query failed: {str(e)}")
    
    raise Exception(f"REST Query failed: Máximo de {max_retries} tentativas excedido")


def fetch_repo_rest_simple(owner: str, name: str, token: str) -> dict:
    """
    Busca dados básicos de um repositório via REST API.
    Retorna métricas agregadas.
    """
    endpoint = f"/repos/{owner}/{name}"
    result = run_rest_query(endpoint, token)
    
    return {
        'data': result['data'],
        'time': result['time'],
        'size': result['size'],
        'requests': 1
    }


def fetch_prs_rest_multiple(owner: str, name: str, token: str, per_page: int = 100, max_pages: int = 1) -> dict:
    """
    Busca PRs via REST API (pode fazer múltiplas requisições para paginação).
    Para cada PR, busca dados adicionais (participantes) para equiparar ao GraphQL.
    Retorna todas as métricas agregadas.
    """
    all_prs = []
    total_time = 0
    total_size = 0
    total_requests = 0
    page = 1
    
    # Busca a lista de PRs
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
        total_requests += 1
        
        # Se retornou menos que per_page, não há mais páginas
        if len(result['data']) < per_page:
            break
        
        page += 1
    
    # Para cada PR, busca os participantes (para equiparar ao GraphQL)
    print(f"  Buscando dados detalhados de {len(all_prs)} PRs...")
    for pr in all_prs:
        pr_number = pr['number']
        
        # Busca participantes (equivalente ao participants.totalCount do GraphQL)
        try:
            endpoint = f"/repos/{owner}/{name}/issues/{pr_number}/events"
            events_result = run_rest_query(endpoint, token)
            
            # Conta participantes únicos dos eventos
            participants = set()
            for event in events_result['data']:
                if event.get('actor'):
                    participants.add(event['actor']['login'])
            
            pr['_participants_count'] = len(participants)
            
            total_time += events_result['time']
            total_size += events_result['size']
            total_requests += 1
            
        except Exception as e:
            print(f"    Aviso: Erro ao buscar participantes do PR #{pr_number}: {e}")
            pr['_participants_count'] = 0
    
    return {
        'data': all_prs,
        'time': total_time,
        'size': total_size,
        'requests': total_requests
    }
