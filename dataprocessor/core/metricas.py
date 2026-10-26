# metricas.py

def media_idade(clientes):
    """Calcula a média de idade ignorando valores inválidos."""
    idades_validas = [
        cliente.idade
        for cliente in clientes
        if cliente.idade is not None and cliente.idade > 0
    ]
    if not idades_validas:
        return None
    return round(sum(idades_validas) / len(idades_validas), 2) # sum(soma) len(tamanho da lista)


def extremos_idade(clientes):
    """Retorna (minimo, maximo) das idades válidas."""
    idades_validas = [
        cliente.idade
        for cliente in clientes
        if cliente.idade is not None and cliente.idade > 0
    ]
    if not idades_validas:
        return None, None
    return min(idades_validas), max(idades_validas)


def contar_por_cidade(clientes):
    """Retorna dicionário com contagem de clientes por cidade."""
    contagem = {}
    for cliente in clientes:
        cidade = cliente.cidade
        contagem[cidade] = contagem.get(cidade, 0) + 1 # se a cidade não existir, retorna 0 e soma 1, se existir, soma 1
    return contagem

def transacoes_aprovadas(transacoes):
    """Retorna lista de transações aprovadas com valor positivo."""
    return [
        transacao
        for transacao in transacoes
        if transacao.status == "aprovado"
        and transacao.valor is not None
        and transacao.valor > 0
    ]

def total_aprovado(transacoes):
    """Soma os valores das transações aprovadas com valor positivo."""
    return sum(t.valor for t in transacoes_aprovadas(transacoes))


def ticket_medio_aprovado(transacoes):
    """Calcula o ticket médio das transações aprovadas com valor positivo."""
    aprovadas = transacoes_aprovadas(transacoes)
    if not aprovadas:
        return None
    return sum(transacao.valor for transacao in aprovadas) / len(aprovadas)
