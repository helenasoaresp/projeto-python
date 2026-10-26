import csv
import json

from ..core.entidades import Cliente, Transacao


def _para_int(valor, padrao=None):
    try:
        return int(valor)
    except (ValueError, TypeError):
        return padrao


def _para_float(valor, padrao=None):
    try:
        return float(valor)
    except (ValueError, TypeError):
        return padrao


def carregar_clientes(caminho):
    clientes = []
    with open(caminho, encoding="utf-8") as arquivo:
        leitor = csv.DictReader(arquivo)
        for linha in leitor:
            cliente = Cliente(
                id=_para_int(linha["id"]),
                nome=(linha["nome"] or "").strip(),
                email=(linha["email"] or "").strip(),
                idade=_para_int(linha["idade"]),
                cidade=(linha["cidade"] or "").strip(),
                data_cadastro=(linha["data_cadastro"] or "").strip(),
            )
            clientes.append(cliente)
    return clientes


def carregar_transacoes(caminho):
    transacoes = []
    with open(caminho, encoding="utf-8") as arquivo:
        leitor = csv.DictReader(arquivo)

        for linha in leitor:
            transacao = Transacao(
                id=_para_int(linha["id"]),
                cliente_id=_para_int(linha["cliente_id"]),
                valor=_para_float(linha["valor"]),
                categoria=(linha["categoria"] or "").strip(),
                data=(linha["data"] or "").strip(),
                status=(linha["status"] or "").strip(),
            )
            transacoes.append(transacao)

    return transacoes


def carregar_config(caminho):
    with open(caminho, encoding="utf-8") as arquivo:
        config = json.load(arquivo)
    if not isinstance(config, dict):
        raise ValueError("A configuração deve ser um objeto JSON.")
    return config