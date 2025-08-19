from datetime import datetime

def calcular_tempo_repositorio(created_at: datetime) -> float:
    """Calcula e retorna a idade do repositório em anos, usando para o cálculo a data de criação e o ano atual."""
    return (datetime.now() - created_at).days / 365 #created_at: datetime da criação do repositório

def calcular_atualizacao_repositorio(updated_at: datetime) -> int:
    """Calcula e retorna quantos dias desde a última atualização do repositório."""
    return (datetime.now() - updated_at).days #updated_at: datetime da última atualização do repositório

def calcular_razao_issues_fechadas(issues_fechadas: int, issues_total: int) -> float:
    # TODO
    
    return issues_fechadas / issues_total