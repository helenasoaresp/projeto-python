# validador.py
from datetime import date


def email_valido(email):
    if not email or not email.strip():
        return False
    if "@" not in email:
        return False
    partes = email.strip().split("@")  # split(separa em duas partes)
    return not (len(partes) != 2 or "." not in partes[1])


def idade_valida(idade):
    if idade is None:
        return False
    return 0 < idade < 150


def data_valida(texto):
    if not texto:
        return False
    try:
        date.fromisoformat(texto)  # date.fromisoformat converte a string para data
        return True
    except ValueError:
        return False


def valor_valido(valor, minimo=0):
    if valor is None:
        return False
    return valor > minimo


def validar_cliente(cliente):
    erros = []
    if cliente.id is None:
        erros.append("id inválido")
    if not cliente.nome or not cliente.nome.strip():
        erros.append("nome vazio")
    if not email_valido(cliente.email):
        erros.append(f"email inválido: '{cliente.email}'")
    if not idade_valida(cliente.idade):
        erros.append(f"idade inválida: {cliente.idade}")
    if not data_valida(cliente.data_cadastro):
        erros.append(f"data inválida: '{cliente.data_cadastro}'")
    return erros


def validar_transacao(transacao, ids_clientes, config):
    erros = []

    if transacao.id is None:
        erros.append("id inválido")

    if transacao.cliente_id not in ids_clientes:
        erros.append(f"cliente_id inexistente: {transacao.cliente_id}")

    if not valor_valido(transacao.valor, config.get("valor_minimo", 0)):
        erros.append(f"valor inválido: {transacao.valor}")

    categorias = config.get("categorias_validas", [])
    if transacao.categoria not in categorias:
        erros.append(f"categoria inválida: '{transacao.categoria}'")

    status_validos = config.get("status_validos", [])
    if transacao.status not in status_validos:
        erros.append(f"status inválido: '{transacao.status}'")

    return erros


def separar_registros(
    registros, funcao_validar, **kwargs
):  # **kwargs coisas extras (ids, config)
    validos = []
    invalidos = []
    for registro in registros:
        erros = funcao_validar(registro, **kwargs)
        if erros:
            invalidos.append({"registro": registro, "erros": erros})
        else:
            validos.append(registro)
    return validos, invalidos
