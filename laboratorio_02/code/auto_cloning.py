import os

JAVA_REPOS_PATH = 'C:\MinhasCoisas\Programacao\Workspace\puc\lab_experimentacao_software\laboratorio_02\code\java_repositories'
CK_TARGET_PATH = 'C:\MinhasCoisas\Programacao\Workspace\puc\lab_experimentacao_software\laboratorio_02\code\ck'

DEFAULT_JAVA_RESULTS_PATH = 'C:\MinhasCoisas\Programacao\Workspace\puc\lab_experimentacao_software\laboratorio_02\code\java_repositories_results'

def clone_repo(url: str) -> None:
    """
    Clona um repositório Git na URL especificada para o caminho local fornecido.
    """
    os.chdir(JAVA_REPOS_PATH)
    os.system(f'git clone {url}')
    

def run_metrics(repo_name: str) -> None:
    """
    Executa a ferramenta CK para calcular métricas de código no repositório especificado.
    """
    repo_path = JAVA_REPOS_PATH + '/' + repo_name
    output_path = DEFAULT_JAVA_RESULTS_PATH + '/' + repo_name + '/'

    os.chdir(CK_TARGET_PATH)
    os.makedirs(output_path, exist_ok=True)
    os.system(f'java -jar target/ck-0.7.1-SNAPSHOT-jar-with-dependencies.jar {repo_path} true 0 True {output_path}')
    

# java -jar ` 
# target/ck-0.7.1-SNAPSHOT-jar-with-dependencies.jar `
# C:\MinhasCoisas\Programacao\Workspace\puc\lab_experimentacao_software\laboratorio_02\code\java_repositories\api `
# true `
# 0 `
# True `
# C:\MinhasCoisas\Programacao\Workspace\puc\lab_experimentacao_software\laboratorio_02\code\java_repositories_results