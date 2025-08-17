from github_api import run_query
from data import build_query

token = '{COLOQUE_SEU_TOKEN_AQUI}'

result = run_query(build_query(), token)

print(result)