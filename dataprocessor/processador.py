# processador.py

def media_idade(clientes):
    """Calcula a média de idade ignorando valores inválidos."""
    idades_validas = [c["idade"] for c in clientes if c["idade"] > 0]
    if not idades_validas:
        return None
    return sum(idades_validas) / len(idades_validas)


def extremos_idade(clientes):
    """Retorna (minimo, maximo) das idades válidas."""
    idades_validas = [c["idade"] for c in clientes if c["idade"] > 0]
    if not idades_validas:
        return None, None
    return min(idades_validas), max(idades_validas)


def contar_por_cidade(clientes):
    """Retorna dicionário com contagem de clientes por cidade."""
    contagem = {}
    for cliente in clientes:
        cidade = cliente["cidade"]
        contagem[cidade] = contagem.get(cidade, 0) + 1
    return contagem


def total_aprovado(transacoes):
    """Soma os valores das transações aprovadas com valor positivo."""
    return sum(
        t["valor"]
        for t in transacoes
        if t["status"] == "aprovado" and t["valor"] > 0
    )