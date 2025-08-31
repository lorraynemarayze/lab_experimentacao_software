from datetime import datetime, timezone

def calcular_tempo_repositorio(created_at: datetime) -> float:
    """Calcula e retorna a idade do repositório em anos, usando para o cálculo a data de criação e o ano atual."""
    agora = datetime.now(timezone.utc)
    return (agora - created_at).days / 365 #created_at: datetime da criação do repositório