from datetime import datetime
from calculos import calcular_tempo_repositorio, calcular_atualizacao_repositorio

def build_query():
    """
    Retorna a query do GraphQL para coletar os 100 repositórios com mais estrelas do Github.
    """
    query = """
    {
      search(query: "stars:>1 sort:stars-desc", type: REPOSITORY, first: 100) {
        nodes {
          ... on Repository {
            name
            owner { login }
            createdAt
            updatedAt
            stargazerCount
            primaryLanguage { name }
            releases { totalCount }
            pullRequests(states: MERGED) { totalCount }
            issues(states: [OPEN, CLOSED]) { totalCount }
            closedIssues: issues(states: CLOSED) { totalCount }
          }
        }
      }
    }
    """
    
    return query



def processar_dados_repositorio(repo: dict) -> dict:
    """
    Processa os dados de um repositório encontrado e retorna métricas para as RQs serem respondidas.
    """
    created_at = datetime.fromisoformat(repo["createdAt"][:-1])
    updated_at = datetime.fromisoformat(repo["updatedAt"][:-1])

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
    }
