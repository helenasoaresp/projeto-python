# transformador.py
import unicodedata
from dataclasses import replace


def _remover_acentos(texto):
    nfkd = unicodedata.normalize("NFKD", texto) # unicodedata.normalize normaliza o texto para remover acentos e outros caracteres especiais
    return "".join(c for c in nfkd if not unicodedata.combining(c)) # separa os acentos  e retorna apenas os caracteres base


def normalizar_nome(nome):
    if not nome:
        return ""
    return nome.strip().title() # title(primeira letra maiuscula)


def normalizar_email(email):
    if not email:
        return ""
    return email.strip().lower() # lower(deixa tudo em minusculo)


def normalizar_cidade(cidade):
    if not cidade:
        return ""
    return _remover_acentos(cidade.strip()).title()


def transformar_cliente(cliente):
    return replace(
        cliente,
        nome=normalizar_nome(cliente.nome),
        email=normalizar_email(cliente.email),
        cidade=normalizar_cidade(cliente.cidade),
        data_cadastro=cliente.data_cadastro.strip(),
    )


def transformar_transacao(transacao):
    return replace(
        transacao,
        categoria=(transacao.categoria or "").strip().lower(),
        data=(transacao.data or "").strip(),
        status=(transacao.status or "").strip().lower(),
    )


def transformar_clientes(clientes):
    return [transformar_cliente(c) for c in clientes]


def transformar_transacoes(transacoes):
    return [transformar_transacao(t) for t in transacoes]