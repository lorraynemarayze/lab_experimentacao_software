from datetime import datetime
from calculos import calcular_atualizacao_repositorio, calcular_tempo_repositorio

    
def build_repo_query(after_cursor, first):
  """
  Retorna a query para coletar os repositórios mais populares (apenas nome).
  - first: quantos repositórios por vez
  - after_cursor: cursor da paginação
  """
  after_str = f', after: "{after_cursor}"' if after_cursor else ""
  return f"""
  {{
    search(query: "stars:>1 sort:stars-desc", type: REPOSITORY, first: {first}{after_str}) {{
      pageInfo {{
        endCursor
        hasNextPage
      }}
      nodes {{
        ... on Repository {{
          nameWithOwner
        }}
      }}
    }}
  }}
  """


def build_pr_query(owner, name, after_cursor=None, first=100):
  """
  Retorna a query para coletar PRs (paginados) de um repositório específico.
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
 


def processar_dados_repositorio(repo: list) -> list:
  """
  Recebe uma lista de repositórios e retorna uma lista única de PRs,
  convertendo atributos objetos em atributos numéricos.
  """
  prs = []
  for pr in repo.get('pullRequests', []):
    # Tamanho
    numero_arquivos = pr.get('changedFiles', 0)
    linhas_adicionadas = pr.get('additions', 0)
    linhas_removidas = pr.get('deletions', 0)

    # Tempo de análise
    created = pr.get('createdAt', '')
    closed = pr.get('closedAt', '')
    intervalo_analise = None
    dt_created = datetime.fromisoformat(created.replace('Z', '+00:00'))
    dt_closed = datetime.fromisoformat(closed.replace('Z', '+00:00'))
    intervalo_analise = (dt_closed - dt_created).total_seconds() / 3600.0 

    # Descrição
    body = pr.get('body', '')
    num_caracteres_body = len(body) if body else 0

    # Interações
    num_participantes = pr.get('participants', {}).get('totalCount', 0)
    num_comentarios = pr.get('comments', {}).get('totalCount', 0)

    # A e B
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