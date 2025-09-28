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
          pullRequests(first: 5, states: [CLOSED, MERGED]) {{
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

            }}
            
            totalCount
          }}
        }}
      }}
    }}
  }}
  """

def processar_dados_repositorio(repo: dict) -> dict:
  return repo['pullRequests']
