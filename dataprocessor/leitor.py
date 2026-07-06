import csv
import json
import os


def _para_int(valor, padrao=None): # converte o valor para inteiro, se não for possível, retorna o valor padrão 
    try:
        return int(valor)
    except (ValueError, TypeError):
        return padrao


def _para_float(valor, padrao=None): # converte o valor para decimal, se não for possível, retorna o valor padrão
    try:
        return float(valor)
    except (ValueError, TypeError):
        return padrao


def carregar_clientes(caminho): # le o arquivo csv de clientes e retorna uma lista de dicionários   
    if not os.path.exists(caminho): # verifica se existe, se não existir, retorna lista vazia
        print(f"[ERRO] Arquivo não encontrado: {caminho}")
        return []

    clientes = []
    with open(caminho, encoding="utf-8") as arquivo: 
        leitor = csv.DictReader(arquivo) # dictReader lê o arquivo csv 
        for linha in leitor:
            clientes.append({ # append coloca mais um item dentro da lista
                "id": _para_int(linha["id"]),
                "nome": linha["nome"].strip(), #strip remove espaços 
                "email": linha["email"].strip(),
                "idade": _para_int(linha["idade"]),
                "cidade": linha["cidade"].strip(),
                "data_cadastro": linha["data_cadastro"].strip(),
            })
    return clientes


def carregar_transacoes(caminho):
    if not os.path.exists(caminho):
        print(f"[ERRO] Arquivo não encontrado: {caminho}")
        return []

    transacoes = []
    with open(caminho, encoding="utf-8") as arquivo:
        leitor = csv.DictReader(arquivo)
        for linha in leitor:
            transacoes.append({
                "id": _para_int(linha["id"]),
                "cliente_id": _para_int(linha["cliente_id"]),
                "valor": _para_float(linha["valor"]),
                "categoria": linha["categoria"].strip(), 
                "data": linha["data"].strip(),
                "status": linha["status"].strip(),
            })
    return transacoes


def carregar_config(caminho):
    if not os.path.exists(caminho):
        print(f"[ERRO] Arquivo não encontrado: {caminho}")
        return {}

    with open(caminho, encoding="utf-8") as arquivo:
        return json.load(arquivo) 