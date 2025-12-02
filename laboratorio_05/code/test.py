import requests
import time
import sys

GITHUB_API_GRAPHQL = "https://api.github.com/graphql"
GITHUB_API_REST = "https://api.github.com"
TOKEN = '{COLOQUE_SEU_TOKEN_AQUI}'


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
    
run_rest_query("/repos/freeCodeCamp/freeCodeCamp", TOKEN)


# repoNameWithOwnerList = [
#     "freeCodeCamp/freeCodeCamp",
#     "sindresorhus/awesome",
#     "EbookFoundation/free-programming-books",
#     "public-apis/public-apis",
#     "kamranahmedse/developer-roadmap",
#     "jwasham/coding-interview-university",
#     "donnemartin/system-design-primer",
#     "996icu/996.ICU",