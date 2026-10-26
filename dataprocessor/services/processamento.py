from ..core.metricas import media_idade, ticket_medio_aprovado, total_aprovado
from ..core.transformador import transformar_clientes, transformar_transacoes
from ..core.validador import separar_registros, validar_cliente, validar_transacao
from ..infra.arquivos import carregar_clientes, carregar_config, carregar_transacoes


def executar_processamento(appconfig):
    clientes_raw = carregar_clientes(appconfig.caminho_clientes)
    transacoes_raw = carregar_transacoes(appconfig.caminho_transacoes)
    config = carregar_config(appconfig.caminho_config)

    clientes_validos, clientes_invalidos = separar_registros(
        clientes_raw, validar_cliente
    )
    ids_validos = {c.id for c in clientes_validos}

    transacoes_validas, transacoes_invalidas = separar_registros(
        transacoes_raw,
        validar_transacao,
        ids_clientes=ids_validos,
        config=config,
    )

    clientes = transformar_clientes(clientes_validos)
    transacoes = transformar_transacoes(transacoes_validas)

    return {
        "clientes": clientes,
        "transacoes": transacoes,
        "clientes_invalidos": clientes_invalidos,
        "transacoes_invalidas": transacoes_invalidas,
        "metricas": {
            "media_idade": media_idade(clientes),
            "total_aprovado": total_aprovado(transacoes),
            "ticket_medio_aprovado": (ticket_medio_aprovado(transacoes)),
        },
    }
