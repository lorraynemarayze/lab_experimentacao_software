import requests

GITHUB_API_URL = "https://api.github.com/graphql"

def run_query(query: str, token: str) -> dict:
    """
    Executa uma consulta GraphQL na API do GitHub.
    """
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.post(GITHUB_API_URL, json={"query": query}, headers=headers)

    if response.status_code != 200:
        raise Exception(f"Query failed: {response.status_code} {response.text}")

    return response.json()


