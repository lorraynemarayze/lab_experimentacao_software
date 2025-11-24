from datetime import datetime

def build_pr_query_graphql(owner: str, name: str, after_cursor=None, first: int = 100):
    """
    Retorna a query GraphQL para coletar PRs de um repositório específico.
    - owner: dono do repositório
    - name: nome do repositório
    - first: número de PRs por requisição (máx 100)
    - after_cursor: cursor da paginação de PRs
    """
    after_str = f', after: "{after_cursor}"' if after_cursor else ""
    return f"""
    {{
      repository(owner: "{owner}", name: "{name}") {{
        nameWithOwner
        pullRequests(states: [CLOSED, MERGED], first: {first}{after_str}) {{
          pageInfo {{
            endCursor
            hasNextPage
          }}
          nodes {{
            body
            state
            createdAt
            closedAt              
            additions
            deletions
            changedFiles
            participants {{
              totalCount
            }}
            comments {{
              totalCount
            }}
            reviews {{
              totalCount
            }}
          }}
          totalCount
        }}
      }}
    }}
    """


def processar_prs_graphql(response_data: dict) -> list:
    """
    Processa a resposta GraphQL e extrai os dados dos PRs.
    """
    prs = []
    
    if 'data' not in response_data or 'repository' not in response_data['data']:
        return prs
    
    repo = response_data['data']['repository']
    if not repo or 'pullRequests' not in repo:
        return prs
    
    pull_requests = repo['pullRequests'].get('nodes', [])
    
    for pr in pull_requests:
        # Tamanho
        numero_arquivos = pr.get('changedFiles', 0)
        linhas_adicionadas = pr.get('additions', 0)
        linhas_removidas = pr.get('deletions', 0)

        # Tempo de análise
        created = pr.get('createdAt', '')
        closed = pr.get('closedAt', '')
        intervalo_analise = None
        if created and closed:
            dt_created = datetime.fromisoformat(created.replace('Z', '+00:00'))
            dt_closed = datetime.fromisoformat(closed.replace('Z', '+00:00'))
            intervalo_analise = (dt_closed - dt_created).total_seconds() / 3600.0 

        # Descrição
        body = pr.get('body', '')
        num_caracteres_body = len(body) if body else 0

        # Interações
        num_participantes = pr.get('participants', {}).get('totalCount', 0)
        num_comentarios = pr.get('comments', {}).get('totalCount', 0)

        # Revisões e status
        num_revisoes = pr.get('reviews', {}).get('totalCount', 0)
        status = pr.get('state', '')

        prs.append({
            'numero_arquivos': numero_arquivos,
            'linhas_adicionadas': linhas_adicionadas,
            'linhas_removidas': linhas_removidas,
            'intervalo_analise_horas': intervalo_analise,
            'num_caracteres_body': num_caracteres_body,
            'num_participantes': num_participantes,
            'num_comentarios': num_comentarios,
            'num_revisoes': num_revisoes,
            'status': status
        })
    
    return prs


def processar_prs_rest(prs_data: list) -> list:
    """
    Processa a resposta REST e extrai os dados dos PRs.
    Nota: REST API não retorna todos os campos em uma única requisição,
    então alguns campos podem não estar disponíveis.
    """
    prs = []
    
    for pr in prs_data:
        # Tamanho
        numero_arquivos = pr.get('changed_files', 0)
        linhas_adicionadas = pr.get('additions', 0)
        linhas_removidas = pr.get('deletions', 0)

        # Tempo de análise
        created = pr.get('created_at', '')
        closed = pr.get('closed_at', '')
        intervalo_analise = None
        if created and closed:
            dt_created = datetime.fromisoformat(created.replace('Z', '+00:00'))
            dt_closed = datetime.fromisoformat(closed.replace('Z', '+00:00'))
            intervalo_analise = (dt_closed - dt_created).total_seconds() / 3600.0 

        # Descrição
        body = pr.get('body', '')
        num_caracteres_body = len(body) if body else 0

        # Interações - REST não fornece alguns desses dados diretamente
        # Seria necessário fazer requisições adicionais
        num_participantes = 0  # Não disponível diretamente
        num_comentarios = pr.get('comments', 0)
        num_revisoes = pr.get('review_comments', 0)
        status = pr.get('state', '')

        prs.append({
            'numero_arquivos': numero_arquivos,
            'linhas_adicionadas': linhas_adicionadas,
            'linhas_removidas': linhas_removidas,
            'intervalo_analise_horas': intervalo_analise,
            'num_caracteres_body': num_caracteres_body,
            'num_participantes': num_participantes,
            'num_comentarios': num_comentarios,
            'num_revisoes': num_revisoes,
            'status': status
        })
    
    return prs
