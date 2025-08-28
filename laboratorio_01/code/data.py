from datetime import datetime
from calculos import calcular_atualizacao_repositorio, calcular_tempo_repositorio

    
def build_query(after_cursor, first):
  """
  Retorna a query do GraphQL para coletar os repositórios de forma paginada.
  first indica quantos vão ser pegos por vez, e after_cursor indica a partir
  de quando eles vão ser pegos
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
          name
          owner {{ login }}
          createdAt
          updatedAt
          stargazerCount
          primaryLanguage {{ name }}
          releases {{ totalCount }}
          pullRequests(states: MERGED) {{ totalCount }}
          issues(states: [OPEN, CLOSED]) {{ totalCount }}
          closedIssues: issues(states: CLOSED) {{ totalCount }}
          mentionableUsers {{ totalCount }}
        }}
      }}
    }}
  }}
  """



def processar_dados_repositorio(repo: dict) -> dict:
    """
    Processa os dados de um repositório encontrado e retorna métricas para as RQs serem respondidas.
    """
    created_at = datetime.fromisoformat(repo["createdAt"])
    updated_at = datetime.fromisoformat(repo["updatedAt"])

    return {
        "name": repo["name"],
        "owner": repo["owner"]["login"],
        "language": repo["primaryLanguage"]["name"] if repo["primaryLanguage"] else "Unknown",
        "age_years": calcular_tempo_repositorio(created_at),
        "pull_requests": repo["pullRequests"]["totalCount"],
        "releases": repo["releases"]["totalCount"],
        "last_update_days": calcular_atualizacao_repositorio(updated_at),
        "issues_total": repo["issues"]["totalCount"],
        "issues_closed": repo["closedIssues"]["totalCount"],
        "issues_ratio": (
            repo["closedIssues"]["totalCount"] / repo["issues"]["totalCount"]
            if repo["issues"]["totalCount"] > 0 else 0
        ),
        "stars": repo["stargazerCount"], 
        "contributors": repo["mentionableUsers"]["totalCount"],
    }
