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
 


def processar_dados_repositorio(repo: dict) -> dict:
  return repo
