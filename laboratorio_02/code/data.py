from datetime import datetime
from calculos import calcular_tempo_repositorio

    
def build_query(after_cursor, first):
  """
  Retorna a query do GraphQL para coletar os repositórios de forma paginada.
  first indica quantos vão ser pegos por vez, e after_cursor indica a partir
  de quando eles vão ser pegos
  """
  after_str = f', after: "{after_cursor}"' if after_cursor else ""
  return f"""
  {{
    search(query: "stars:>1 sort:stars-desc language:Java", type: REPOSITORY, first: {first}{after_str}) {{
      pageInfo {{
        endCursor
        hasNextPage
      }}
      nodes {{
        ... on Repository {{
          name
          stargazerCount
          releases {{ totalCount }}
          createdAt
          primaryLanguage {{ name }}
          url
        }}
      }}
    }}
  }}
  """



def processar_dados_repositorio(repo: dict) -> dict:
    """
    Processa os dados de um repositório encontrado e retorna métricas para as RQs serem respondidas.
    """
    
    repository_age = datetime.fromisoformat(repo["createdAt"].replace("Z", "+00:00"))

    return {
        "name": repo["name"],
        "stars": repo["stargazerCount"], 
        "releases": repo["releases"]["totalCount"],
        "age_years": calcular_tempo_repositorio(repository_age),
        "language": repo["primaryLanguage"]["name"] if repo["primaryLanguage"] else "Unknown",
        "url": repo["url"] + '.git'
    }
